import os
from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

if not os.environ.get("APIFY_API_TOKEN"):
    raise SystemExit("Set APIFY_API_TOKEN before running this example")
client = YouTubeChannelAnalyzerClient()
print(client.run_one({'targets': ['@MrBeast'], 'historyDays': '28', 'fastMode': True}))
