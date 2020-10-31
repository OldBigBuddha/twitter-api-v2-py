# Twitter APIv2 for Python

![alpha-1.0.0](https://img.shields.io/badge/version-alpha%201.0.0-red)
![Python 3.9.0](https://img.shields.io/badge/python-3.9.0-blue)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

Twitter APIv2: [Document](https://developer.twitter.com/en/docs/twitter-api/early-access)

## 目標

Twitter API v2 をラップした感じのものを作りたい。

## 今できること

- Tweet ID を指定して Tweet 情報の一部を取得すること。

```py
twitter: TwitterAPI = TwitterAPI(BEARER_TOKEN)

tweet: Tweet = twitter.get_tweet(TWEET_ID)
tweet.tweet_id
tweet.text
tweet.author_id
tweet.source
tweet.possibly_sensitive
tweet.lang
tweet.created_at
```

## Dependencies

[requirements.txt](./requirements.txt)
