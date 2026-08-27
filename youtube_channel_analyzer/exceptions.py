"""Public exception hierarchy for the YouTube Channel Analyzer SDK."""

class YouTubeChannelAnalyzerError(Exception):
    """Base SDK error."""

class AuthenticationError(YouTubeChannelAnalyzerError):
    """The Apify token is missing or rejected."""

class ActorRunError(YouTubeChannelAnalyzerError):
    """The Actor run or Dataset request failed."""

class ActorTimeoutError(YouTubeChannelAnalyzerError):
    """The client stopped waiting before the Actor completed."""
