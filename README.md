# Twitter APIv2 for Python

![alpha-1.7.0](https://img.shields.io/badge/version-alpha%201.7.0-red)
![Python 3.9.0](https://img.shields.io/badge/python-3.9.0-blue)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

[![Lint](https://github.com/OldBigBuddha/twitter-api-v2-py/workflows/Lint/badge.svg)](https://github.com/OldBigBuddha/twitter-api-v2-py/actions?query=workflow%3ALint)
[![pytest](https://github.com/OldBigBuddha/twitter-api-v2-py/workflows/pytest/badge.svg)](https://github.com/OldBigBuddha/twitter-api-v2-py/actions?query=workflow%3Apytest)

Twitter APIv2: [Document](https://developer.twitter.com/en/docs/twitter-api/early-access)

## Goal

Full support Twitter API v2.

## Development

Read [HOW_TO_DEVELOP](./HOW_TO_DEVELOP.md).

## Features

- [x] Bearer Token
- [ ] OAuth 1.1
- [ ] Tweet lookup
  - [x] Get Tweet(specified field by Enum)
  - [x] With Context Annotation
  - [x] With Entity
  - [x] With Media
  - [x] With Public Metric
  - [x] With Poll
  - [ ] With Place
  - [ ] Multi Tweets
- [x] User lookup
  - [x] Get User
    - [x] By ID
    - [x] By ID
  - [x] With Entities
  - [ ] Multi Users
- [ ] Recent Search
- [ ] Filtered stream
- [ ] Sampled stream
- [ ] Hide replies

## Sample code

```py
import os
from typing import List

from twitter_api_v2 import Tweet, TwitterAPI, User

BEARER_TOKEN: str = os.environ["TWITTER_BEARER_TOKEN"]


def main():
    twitter: TwitterAPI.TwitterAPI = TwitterAPI.TwitterAPI(BEARER_TOKEN)

    # Lookup Tweet
    # If you'd like to know what you can specify,
    # Please read Tweet.Field class and Twitter API Document
    # FYI: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet#component-wrapper:~:text=.%20Use%20the%20expansion%20with%20the,additional%20fields%20to%20complete%20the%20object.
    tweet_fields: List[Tweet.Field] = [
        Tweet.Field.AUTHOR_ID,
        Tweet.Field.CREATED_AT,
        Tweet.Field.POSSIBLY_SENSITIVE,
        Tweet.Field.SOURCE,
    ]

    tweet: Tweet.Tweet = twitter.get_tweet(
        "1331553700058329088", tweet_fields=tweet_fields
    )

    print(tweet.author_id)
    print(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    print(tweet.lang)
    print(tweet.possibly_sensitive)

    # Lookup User by ID
    user_by_id: User.User = twitter.get_user_by_id("859754215748419584")
    print(user_by_id.id)
    print(user_by_id.username)

    # Lookup User by username(trim @ from username like @OldBigBuddha)
    # If you'd like to know what you can specify,
    # Please read User.Field class and Twitter API Document
    # FYI: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user#component-wrapper:~:text=.%20Use%20the%20expansion%20with%20the,additional%20fields%20to%20complete%20the%20object.
    user_fields: List[User.User] = [
        User.Field.DESCRIPTION,
        User.Field.LOCATION,
        User.Field.URL,
    ]

    user_by_username: User.User = twitter.get_user_by_username(
        "OldBigBuddha", user_fields=user_fields
    )
    print(user_by_username.description.text)
    print(user_by_username.url)


if __name__ == "__main__":
    main()

```

## Dependencies

[requirements.txt](./requirements.txt)

## VS Code configuration

```json
  "[python]": {
      "editor.tabSize": 4,
      "editor.formatOnSave": true,
      "editor.formatOnPaste": false,
      "editor.formatOnType": false,
      "editor.insertSpaces": true,
      "editor.codeActionsOnSave": {
          "source.organizeImports": true
      }
  },
  "python.pythonPath": "${workspaceFolder}/.venv/bin/python",
  "python.envFile": "${workspaceFolder}/.env",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.pycodestyleEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
  "python.sortImports.path": "${workspaceFolder}/.venv/bin/isort",
  "python.linting.mypyEnabled": true,
  "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
      "-vv",
      "--show-capture=all",
      "tests"
  ],
  "autoDocstring.docstringFormat": "numpy",
  "python.languageServer": "Pylance",
  "workbench.editorAssociations": [
      {
          "viewType": "jupyter.notebook.ipynb",
          "filenamePattern": "*.ipynb"
      }
  ]
```
