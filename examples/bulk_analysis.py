from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

client = YouTubeChannelAnalyzerClient()
payload = {'targets': ['@MrBeast'], 'historyDays': '28', 'fastMode': True}
# Add more targets or queries to the list fields supported by this Actor.
rows = client.run(payload)
print(f"Received {len(rows)} rows")
