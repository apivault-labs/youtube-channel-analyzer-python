from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

client = YouTubeChannelAnalyzerClient()
rows = client.run({'targets': ['@MrBeast'], 'historyDays': '28', 'fastMode': True})
print(rows[0] if rows else "No results")
