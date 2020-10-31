import json

import requests

from TwitterAPIv2.Tweet import Tweet


class TwitterAPI:
    def __init__(self, bearer_token: str) -> None:
        self.__BEARER_TOKEN: str = bearer_token
        self.__REQUEST_HEADERS: dict = {
            'Authorization': f'Bearer {self.__BEARER_TOKEN}'
        }
        self.__REQUEST_PARAMATERS: dict = {
            'tweet.fields': 'author_id,created_at,id,lang,possibly_sensitive,source,text'
        }

        self.__API_URL: str = 'https://api.twitter.com/2/tweets'

    def get_tweet(self, id: str) -> Tweet:
        response = requests.get(url=f'{self.__API_URL}/{id}', params=self.__REQUEST_PARAMATERS, headers=self.__REQUEST_HEADERS)
        res_json = json.loads(response.text)
        return Tweet(**res_json['data'])
