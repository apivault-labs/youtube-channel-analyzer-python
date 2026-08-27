import json
from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

rows = YouTubeChannelAnalyzerClient().run({'targets': ['@MrBeast'], 'historyDays': '28', 'fastMode': True})
with open("results.json", "w", encoding="utf-8") as handle:
    json.dump(rows, handle, ensure_ascii=False, indent=2)
