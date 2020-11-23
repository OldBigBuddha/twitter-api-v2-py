import json
import logging
from logging import Logger
from typing import Dict, List, Optional

import requests
from requests.models import Response

from twitter_api_v2 import Media, Poll, Tweet, User

logger: Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TwitterAPI:
    def __init__(self, bearer_token: str) -> None:
        self.__BEARER_TOKEN: str = bearer_token
        self.__REQUEST_HEADERS: Dict = {
            "Authorization": f"Bearer {self.__BEARER_TOKEN}"
        }

        self.__API_URL: str = "https://api.twitter.com/2"

    def get_tweet(
        self,
        id: str,
        expansions: List[Tweet.Expantion] = [],
        tweet_fields: List[Tweet.Field] = [],
        media_fields: List[Media.Field] = [],
        poll_fields: List[Poll.Field] = [],
    ) -> Tweet.Tweet:

        params: Optional[Dict[str, str]] = self._make_params(
            expansions, tweet_fields, media_fields, poll_fields
        )
        logger.debug(params)
        response: Response = requests.get(
            url=f"{self.__API_URL}/tweets/{id}",
            params=params,
            headers=self.__REQUEST_HEADERS,
        )

        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )

        res_json = json.loads(response.text)
        logger.debug(res_json)
        if "includes" in res_json.keys():
            return Tweet.Tweet(**res_json["data"], **res_json["includes"])
        else:
            return Tweet.Tweet(**res_json["data"])

    def get_user(self, id: str, user_fields: List[User.Field] = []) -> User.User:
        params: Optional[Dict[str, str]] = None
        if user_fields:
            params = {}
            params["user.fields"] = ",".join(list(map(str, user_fields)))

        response: Response = requests.get(
            f"{self.__API_URL}/users/{id}",
            params=params,
            headers=self.__REQUEST_HEADERS,
        )

        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )

        res_json = json.loads(response.text)
        logger.debug(res_json)

        return User.User(**res_json["data"])

    def _make_params(
        self,
        expansions: List[Tweet.Expantion],
        tweet_fields: List[Tweet.Field],
        media_fields: List[Media.Field],
        poll_fields: List[Poll.Field],
    ) -> Optional[Dict[str, str]]:

        if (
            (not expansions)
            and (not tweet_fields)
            and (not media_fields)
            and (not poll_fields)
        ):
            return None

        params: Dict[str, str] = {}
        if expansions:
            params["expansions"] = ",".join(list(map(str, expansions)))
        if tweet_fields:
            params["tweet.fields"] = ",".join(list(map(str, tweet_fields)))
        if media_fields:
            params["media.fields"] = ",".join(list(map(str, media_fields)))
        if poll_fields:
            params["poll.fields"] = ",".join(list(map(str, poll_fields)))

        return params
