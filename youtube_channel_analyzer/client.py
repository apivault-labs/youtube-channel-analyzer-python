"""Thin synchronous client for the YouTube Channel Analyzer Apify Actor."""
from __future__ import annotations

import os
import time
from typing import Any, Mapping

import requests

from .exceptions import ActorRunError, ActorTimeoutError, AuthenticationError, YouTubeChannelAnalyzerError

ACTOR_ID = "apivault_labs~youtube-channel-stats"
APIFY_API_BASE = "https://api.apify.com/v2"
TERMINAL_FAIL = {"FAILED", "TIMED-OUT", "ABORTED"}


class YouTubeChannelAnalyzerClient:
    """Run the hosted Actor and download its Dataset results."""

    def __init__(self, api_token: str | None = None, timeout: int = 600,
                 poll_interval: float = 3.0, base_url: str = APIFY_API_BASE):
        token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not token:
            raise AuthenticationError(
                "Pass api_token or set APIFY_API_TOKEN. Create a token at "
                "https://console.apify.com/account/integrations"
            )
        self.timeout = int(timeout)
        self.poll_interval = float(poll_interval)
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "youtube-channel-analyzer-python/0.1.0",
        })

    def run(self, actor_input: Mapping[str, Any], *, actor_timeout_secs: int = 300) -> list[dict[str, Any]]:
        """Start one Actor run, wait for completion and return clean Dataset items."""
        if not isinstance(actor_input, Mapping):
            raise TypeError("actor_input must be a mapping")
        run_id = self._start(dict(actor_input), actor_timeout_secs)
        run = self._wait(run_id)
        dataset_id = run.get("defaultDatasetId")
        if not dataset_id:
            raise ActorRunError("Successful run did not expose a Dataset ID")
        return self._dataset(dataset_id)

    def run_one(self, actor_input: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
        """Return the first Dataset row, raising when no result was produced."""
        rows = self.run(actor_input, **kwargs)
        if not rows:
            raise ActorRunError("Actor completed but returned no Dataset rows")
        return rows[0]

    @staticmethod
    def estimate_cost(result_count: int, price_per_1000: float = 1.0) -> float:
        """Estimate result charges; actual tier pricing and platform usage may vary."""
        if result_count < 0:
            raise ValueError("result_count cannot be negative")
        return round(result_count * price_per_1000 / 1000, 6)

    def _start(self, payload: dict[str, Any], timeout_secs: int) -> str:
        try:
            response = self.session.post(
                f"{self.base_url}/acts/{ACTOR_ID}/runs",
                params={"timeout": int(timeout_secs)}, json=payload, timeout=30,
            )
        except requests.RequestException as exc:
            raise YouTubeChannelAnalyzerError(f"Could not start Actor run: {exc}") from exc
        if response.status_code == 401:
            raise AuthenticationError("Apify rejected the API token")
        if response.status_code >= 400:
            raise ActorRunError(f"Run start failed with HTTP {response.status_code}: {response.text[:300]}")
        run_id = (response.json().get("data") or {}).get("id")
        if not run_id:
            raise ActorRunError("Apify response did not contain a run ID")
        return run_id

    def _wait(self, run_id: str) -> dict[str, Any]:
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                response = self.session.get(f"{self.base_url}/actor-runs/{run_id}", timeout=30)
            except requests.RequestException as exc:
                raise YouTubeChannelAnalyzerError(f"Could not poll Actor run: {exc}") from exc
            if response.status_code >= 400:
                raise ActorRunError(f"Run poll failed with HTTP {response.status_code}: {response.text[:300]}")
            run = response.json().get("data") or {}
            status = run.get("status")
            if status == "SUCCEEDED":
                return run
            if status in TERMINAL_FAIL:
                raise ActorRunError(f"Actor run ended with {status}: {run.get('statusMessage') or 'no details'}")
            if time.monotonic() >= deadline:
                raise ActorTimeoutError(f"Actor run {run_id} did not finish within {self.timeout} seconds")
            time.sleep(self.poll_interval)

    def _dataset(self, dataset_id: str) -> list[dict[str, Any]]:
        try:
            response = self.session.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params={"clean": "true", "format": "json"}, timeout=120,
            )
        except requests.RequestException as exc:
            raise YouTubeChannelAnalyzerError(f"Could not download Dataset: {exc}") from exc
        if response.status_code >= 400:
            raise ActorRunError(f"Dataset fetch failed with HTTP {response.status_code}: {response.text[:300]}")
        data = response.json()
        if not isinstance(data, list):
            raise ActorRunError("Unexpected Dataset response type")
        return data
