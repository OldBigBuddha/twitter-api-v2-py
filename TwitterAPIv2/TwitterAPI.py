import json
from typing import Dict, List, Optional

import requests

from TwitterAPIv2 import Tweet


class TwitterAPI:
    def __init__(self, bearer_token: str) -> None:
        self.__BEARER_TOKEN: str = bearer_token
        self.__REQUEST_HEADERS: Dict = {
            'Authorization': f'Bearer {self.__BEARER_TOKEN}'
        }

        self.__API_URL: str = 'https://api.twitter.com/2/tweets'

    def get_tweet(self, id: str, fields: List[Tweet.Field] = []) -> Tweet.Tweet:
        params: Optional[Dict[str, str]] = None
        if fields:
            params_str: List[str] = list(map(str, fields))
            params = {
                'tweet.fields': ','.join(params_str)
            }
        response = requests.get(url=f'{self.__API_URL}/{id}', params=params, headers=self.__REQUEST_HEADERS)
        res_json = json.loads(response.text)
        return Tweet.Tweet(**res_json['data'])
