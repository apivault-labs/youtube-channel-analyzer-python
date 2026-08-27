# YouTube Channel Analyzer — Python SDK

Python client for the [YouTube Channel Analyzer Apify Actor](https://apify.com/apivault_labs/youtube-channel-stats). Send public Actor inputs, wait for the hosted run, and receive clean Dataset rows without maintaining scraping infrastructure.

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue)](https://apify.com/apivault_labs/youtube-channel-stats)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Results

- Channel earnings and growth estimates
- Recent videos and audience signals
- Competitor discovery
- Forecasts and historical views

The Actor uses public marketplace signals and returns estimates or ranges where a platform does not publish exact figures.

## Install

```bash
pip install git+https://github.com/apivault-labs/youtube-channel-analyzer-python.git
```

Create an Apify token at [Console → Integrations](https://console.apify.com/account/integrations), then:

```python
from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

client = YouTubeChannelAnalyzerClient(api_token="apify_api_xxxxxx")
rows = client.run({'targets': ['@MrBeast'], 'historyDays': '28', 'fastMode': True})
print(rows[0] if rows else "No results")
```

You can set `APIFY_API_TOKEN` instead of passing the token in code.

## Public input options

| Field | Type | Default | Description |
|---|---|---|---|
| `targets` | `array` | `—` | Channel @handles, channel URLs, channel IDs, or video URLs. A video URL is resolved to its channel automatically. Exact duplicate inputs are removed. |
| `historyDays` | `string` | `28` | How many days of day-by-day views / subscribers / revenue history to include per channel. '0' = summary only (no daily breakdown). |
| `fastMode` | `boolean` | `False` | Skip daily history, monetization/language probe, audience estimate, recent videos, similar channels and forecast. Returns core stats + revenue averages only. Use for large bulk run |
| `maxConcurrency` | `integer` | `10` | Number of channels processed concurrently. Keep the default for most runs and reduce it if a large full-analysis run approaches its resource limit. |
| `proxyConfiguration` | `object` | `—` | Use Apify Proxy to improve network resilience and throughput for large bulk runs. Datacenter proxy is sufficient for this Actor. |

The complete, versioned schema is also available on the [Actor page](https://apify.com/apivault_labs/youtube-channel-stats).

## Pricing

Pay per delivered result through Apify, starting around **$1/1,000 results** on paid tiers. Free-plan pricing and platform usage can differ; check the Actor page before large runs.

## Examples

- `examples/quickstart.py` — first run
- `examples/bulk_analysis.py` — expand a target list
- `examples/export_csv.py` — save flat result fields
- `examples/save_json.py` — preserve nested output
- `examples/cost_estimate.py` — estimate result-event charges
- `examples/environment_token.py` — keep credentials out of code

## Architecture and privacy

This repository is intentionally a thin API client. Collection, retries, analysis and billing run inside the hosted Apify Actor. No private implementation, credentials, scoring weights or infrastructure configuration are included.

## License

MIT. The hosted Actor is a separate paid service governed by Apify terms.
