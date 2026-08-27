from youtube_channel_analyzer import YouTubeChannelAnalyzerClient

for count in (10, 100, 1000):
    print(count, YouTubeChannelAnalyzerClient.estimate_cost(count), "USD estimated result charges")
