class PublicMetric:
    def __init__(self, data: dict) -> None:

        self.retweet_count: int = int(data["retweet_count"])
        self.quote_count: int = int(
            data["quote_count"]
        )  # Please note: This does not include Retweets. To get the “Retweets and comments” total as displayed on the Twitter clients, simply add retweet_count and quote_count.
        self.like_count: int = int(data["like_count"])
        self.reply_count: int = int(data["reply_count"])
