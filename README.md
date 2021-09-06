# HTLC Telegram Bot

This bot sends your lightning node's live [HTLC](https://en.bitcoin.it/wiki/Hash_Time_Locked_Contracts) events as they occur. By default it sends everything, which can get noisy, so it has a `/filter` command, to selectively filter the events you are interested in.

It also stores your HTLCs in a [database file](https://www.sqlite.org/index.html), so that it can send you reports. It is easy to use, and thus accessible to non-developers.

## Why is monitoring HTLCs important

As a good node operator, you'll want to keep an eye on failed HTLC events (`link_fail_event`). These take place when your node fails to route. Minimizing those via the proper use of balanced channels, or the proper use of fees does two things, with two broad consequences:

- It increases the likelihood of the network routing via your node.
	- Thus boosts your chances to earn sats.
- It increases the overall health of the network.
	- Thus increases the chances of lightning growing healthily, and ultimately succeeding.

> "It appears that even after 25 retries, temporary errors are still the most
common".
> 
> Exerpt from 'Understanding the Lightning Network capability to route
payments' [(pdf)](http://essay.utwente.nl/82015/1/Satcs_BA_EEMCS.pdf).

The first step to solving a problem is identifying it. This bot does that for you.

## Bot commands

### `/connect`

Run this so the bot can initiate chats with you.

### `/start`

Start receiving events.

### `/stop`

Stop receiving events.

### `/filter <filter>`

Filter the events to only the ones you're interested in.

### `/help`

List available commands, and get help on using them.

## JQ filtering

The `/filter` command takes a [jq](https://stedolan.github.io/jq/) string. Examples are provided by running the `/help` command.

## Plugins

The bot has a 'plugin' ability, so other devs and technical users can write their own commands by just copying an existing plugin and modifying it. Current plugins are:

### `/export_csv` 

Export HTLCs as csv file and send.

### `/export_excel` 

Export HTLCs as excel file and send.

### `/fails` 

Generate plots of incoming and outgoing link fail event channels

### `/sends` 

Generate a bar chart of SEND forward and fail events, and send.



## Installation

In Telegram, make sure you first create a bot with Bot Father, and take note of your Bot's token. Secondly, have a quick glance at the code or ask a developer to quickly audit the code before running it on your node. Don't trust, verify.

```
# ssh into your lightning node
ssh me@node_ip_address

# create a src directory
mkdir -p src

# enter the src directory
cd src

# clone this repo
git clone https://github.com/routablespace/stream-lnd-htlcs-bot.git

# enter the cloned repo
cd stream-lnd-htlcs-bot

# install the dependencies
pip3 install -r requirements.txt

# run the bot
./stream-lnd-htlcs-bot.py --tg-token <Bot's TG TOKEN>

# same command but for umbrel users:
./stream-lnd-htlcs-bot.py --tg-token <Bot's TG TOKEN> --lnd-dir /home/umbrel/umbrel/lnd 
```

In telegram, you should now be able to run the `/connect` command, followed by the `/start` command.

If you get a response, you should be good.

## Deployment

If the bot is responding to you, the final step is making sure the process keeps on running in the background, even after your `ssh` session ends. The most standard (but somewhat hacky) way of doing this:

```
nohup ./stream-lnd-htlcs-bot.py --lnd-dir /home/umbrel/umbrel/lnd --tg-token MY_TG_TOKEN > /dev/null 2>&1 & disown
```

If you ever need to kill the process, you can safely do so:

```
pkill -f stream-lnd-htlcs-bot.py
```
