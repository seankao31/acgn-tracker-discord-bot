# ACGN Tracker
A "virtual bookmark" service to keep track of where you left off!
This simple discord chatbot helps track your reading/watching progress for animes/comics/novels/drama/TV shows (all referred to as *acgn* in this project)

# Get Started

## 1. Install packages
``` bash
$ pip install -r requirements.txt
```

## 2. Setup bot token
``` bash
$ echo {your_bot_token} > BOT_TOKEN.txt
```

## 3. Run
``` bash
$ python bot.py
```

# Usage
## How to Use
Let's assume you decide to watch a TV show named *Very Interesting Series* which currently has 10 episodes, and to read a comic named *Awesome Comic* which has 100 chapters.
You can add them to the database:
![](https://i.imgur.com/1IWU946.png)

List all acgn's (stands for anime, comic, game, and novel) in the database:
![](https://i.imgur.com/6CQkEfm.png)

Say, you watched 5 episodes of *Very Interesting Series* and read 20 chapters of *Awesome Comic*.
Track them in the database:
![](https://i.imgur.com/tW90nJf.png)

You can also update the number of episodes for an acgn when new episodes come out.
For example, if 20 new chapters of *Awesome Comic* came out, making it 120 episodes in total, since you last checked, you could:
![](https://i.imgur.com/babiL4b.png)

## Command help
Help messages are provided through the following:
- `!track help acgn`: check info on `acgn` commands
    - `!track help acgn list`
    - `!track help acgn update`
- `!track help progress`: check info on `progress` commands
    - `!track help progress list`
    - `!track help progress list-all`
    - `!track help progress update`
