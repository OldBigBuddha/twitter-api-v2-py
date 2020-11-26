# How to develop this library

I prepare two ways to make development environment.

## 1. DevContainer

You can use DevContainer. If you use this way, you need docker in your computer. Please read [here](https://code.visualstudio.com/docs/remote/containers) to know more about DevContainer.

**YOU MUST MAKE `.env` IN PROJECT ROOT AND SET `TWITTER_BEARER_TOKEN`.**

```plan
TWITTER_BEARER_TOKEN=<Bearer Token>
```

## 2. Local

This library is made with Python 3.9. You should prepare it.

**YOU MUSE SET ENVIRONMENT VARIABLE(`TWITTER_BEARER_TOKEN`) FOR DEVELOPING.**

```shell
# Clone this repository
$gh repo clone OldBigBuddha/twitter-api-v2-py

$cd twitter-api-v2-py

# Make virtual environment
$python -m venv .venv
$source .venv/bin/activate

# Install dependencies with requirements.txr
$pip3 install -r requirements.txt

# Let's try pytest to check environment is built.
# DON'T FORGET SET ENVIRONMENT VARIABLE.
$export TWITTER_BEARER_TOKEN=<Bearer Token>
$pytest
```
