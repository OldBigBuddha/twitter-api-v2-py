# Twitter APIv2 for Python

![alpha-1.4.0](https://img.shields.io/badge/version-alpha%201.4.0-red)
![Python 3.9.0](https://img.shields.io/badge/python-3.9.0-blue)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

[![Lint](https://github.com/OldBigBuddha/twitter-api-v2-py/workflows/Lint/badge.svg)](https://github.com/OldBigBuddha/twitter-api-v2-py/actions?query=workflow%3ALint)
[![pytest](https://github.com/OldBigBuddha/twitter-api-v2-py/workflows/pytest/badge.svg)](https://github.com/OldBigBuddha/twitter-api-v2-py/actions?query=workflow%3Apytest)

Twitter APIv2: [Document](https://developer.twitter.com/en/docs/twitter-api/early-access)

## 目標

Twitter API v2 をラップした感じのものを作りたい。

## Features

- [x] Bearer Token
- [ ] OAuth 1.1
- [ ] Tweet lookup
  - [x] Simple Tweet
  - [x] With Media
  - [x] With Public Metric
  - [x] With Poll
  - [ ] With Place
  - [ ] multi tweets lookup
- [ ] User lookup
- [ ] Recent Search
- [ ] Filtered stream
- [ ] Sampled stream
- [ ] Hide replies

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
