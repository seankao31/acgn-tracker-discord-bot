# ACGN Tracker
A "virtual bookmark" service to keep track of where you left off!
This simple discord chatbot helps track your reading/watching progress for animes/comics/novels/drama/TV shows (all referred to as *acgn* in this project)

# Project Structure
```
acgn-tracker-discord-bot
├── .gitignore
├── LICENSE
├── README.md
└── acgn_tracker_discord_bot
    ├── backend
    │   ├── package-lock.json
    │   ├── package.json
    │   └── src
    │       ├── acgn_controller.js
    │       ├── acgn_model.js
    │       ├── api_routes.js
    │       ├── index.js
    │       ├── progress_controller.js
    │       ├── progress_model.js
    │       ├── user_controller.js
    │       └── user_model.js
    └── bot
        ├── bot.py
        ├── requirements.txt
        └── src
            ├── __init__.py
            └── discord_bot.py
```

# Get Started

## Backend Service
Change to the `acgn_tracker_discord_bot/backend` directory.

### 1. Setup MongoDB Service
You need a mongodb service running.
In `package.json`, change the start script: (replace <your_mongodb_uri> with your mongodb uri)
```
"script": {
    "start": "MONGODB_URI=<your_mongodb_uri> node src/index"
}
```

### 2. Install packages
``` bash
$ npm install
```

### 3. Run
``` bash
$ npm start
```

## Discord Bot
Change to the `acgn_tracker_discord_bot/bot` directory.

## 1. Install packages
``` bash
$ pip install -r requirements.txt
```

## 2. Setup bot token
Replace {your_bot_token} with your bot token
``` bash
$ echo {your_bot_token} > BOT_TOKEN.txt
```

## 3. Setup backend service url
Replace {your_service_url} with your service url. By default it should be http://127.0.0.1:8080/api
``` bash
$ echo '[TEST]' > .ini
$ echo SERVICE_URL = {your_service_url} >> .ini
```

## 4. Run
``` bash
$ python bot.py
```

# Command Help Message
Help messages are provided through the following:
- `!track help acgn`: check info on `acgn` commands
    - `!track help acgn list`
    - `!track help acgn search`
    - `!track help acgn add`
    - `!track help acgn update`
- `!track help progress`: check info on `progress` commands
    - `!track help progress list`
    - `!track help progress list-all`
    - `!track help progress add`
    - `!track help progress update`
