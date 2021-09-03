# stream-lnd-htlcs

Stream all HTLC events from an `lnd` node. Includes information about event type, event fate, incoming/outgoing peers, incoming/outgoing channel balance, and additional information depending on the event type. Basically, it's the default HTLC stream provided by the gRPC API but with a little spice.

## Installation

You'll need an active `lnd`, version 0.9.0+ (https://github.com/lightningnetwork/lnd), with routerrpc built in, Python 3 and the requirements.

Get the Repository in the directory where you want to install
```
git clone https://github.com/routablespace/stream-lnd-htlcs-bot.git
```
Change Directory
```
cd stream-lnd-htlcs-bot
```
Install

```
pip3 install -r requirements.txt
```

## Usage

- Create a Telegram bot via Bot Father.
- Copy the access token.
- Run the script with `stream-lnd-htlcs.py --tg-token <TG TOKEN>`
- Running the script will output HTLC event information both to the screen and to a file.

### Command line arguments

```
usage: stream-lnd-htlcs.py [-h] [--lnd-dir LNDDIR] [--output-file OUTFILE] [--stream-mode STREAMMODE] [--silent SILENT]
                           [--human-dates HUMANDATES] [--tg-token TG_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  --lnd-dir LNDDIR      lnd directory; default ~/.lnd
  --output-file OUTFILE
                        HTLC stream output file; default htlc-stream.json
  --stream-mode STREAMMODE
                        Stream output to stdout only; default false
  --silent SILENT       Disable stdout output; default false
  --human-dates HUMANDATES
                        Human friendly datetime; default false
  --tg-token TG_TOKEN   Telegram bot token
```

### Example output

```
{'incoming_channel': 'LN-node1-alias', 'outgoing_channel': 'LN-node2-alias', 'outgoing_channel_capacity': 5000000, 'outgoing_channel_remote_balance': 2500000, 'outgoing_channel_local_balance': 2500000, 'timestamp': 1626750720, 'event_type': 'SEND', 'event_outcome': 'forward_fail_event'}
...
{'incoming_channel': 'LN-nodeX-alias', 'incoming_channel_capacity': 5000000, 'incoming_channel_remote_balance': 2500000, 'incoming_channel_local_balance': 7500000, 'outgoing_channel': 'LN-nodeY-alias', 'outgoing_channel_capacity': 10000000, 'outgoing_channel_remote_balance': 5000000, 'outgoing_channel_local_balance': 5000000, 'timestamp': 1626751932, 'event_type': 'FORWARD', 'event_outcome': 'settle_event'}
```


## Deployment

If you want to deploy this to your node, you can use the fabric file. This is typically done from your dev machine, and not run directly on your node:

```
$ pip3 install fabric3

KEYPEM=~/.path/to/key.pem
USER=<user>
HOST=<ip>

$ alias fab='/usr/local/bin/fab -i ${KEYPEM} -H ${USER}@${HOST} ${*}'

e.g

$ fab --list

Available tasks:

  clear-logs                 Clear the logs
  install                    Clone or pull latest changes from the repo
  install-supervisord        Install supervisord
  install-supervisord-conf   Install supervisord config
  restart                    Restart the app
  start                      Start the app
  stop                       Stop the app
  sync                       Perform an rsync to test latest changes

$ fab install-supervisord-conf --help

Usage: fab [--core-opts] install-supervisord-conf [--options] [other tasks here ...]

Docstring:
  Install supervisord config

Options:
  -t STRING, --tg-token=STRING

$ fab <command> # e.g fab install

# please note fabric commands can be chained, e.g

$ fab stop clear-logs start logs

```