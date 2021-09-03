#!/usr/bin/env python3

import argparse
from lnd import Lnd
from htlc import Htlc
import json
import threading
from simple_chalk import chalk, green, white, blue, red
from tgbot import main as bot_main, shared_data
import jq
import traceback


def thread_function(lnd, args):
    for response in lnd.get_htlc_events():
        htlc = Htlc(lnd, response, args.humandates)
        if args.silent == "false":
            print(htlc.__dict__)
            if shared_data["update"]:
                if shared_data["filter"]:
                    try:
                        txt = (
                            jq.compile(shared_data["filter"])
                            .input(htlc.__dict__)
                            .text()
                        )
                    except:
                        txt = str(traceback.format_exc())
                else:
                    txt = str(htlc.__dict__)
                if txt:
                    shared_data["update"].message.reply_text(txt)
        if args.streammode == "false":
            with open(args.outfile, "a") as f:
                print(htlc.__dict__, file=f)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--lnd-dir",
        default="~/.lnd",
        dest="lnddir",
        help="lnd directory; default ~/.lnd",
    )
    arg_parser.add_argument(
        "--output-file",
        default="htlc-stream.json",
        dest="outfile",
        help="HTLC stream output file; default htlc-stream.json",
    )
    arg_parser.add_argument(
        "--stream-mode",
        default="false",
        dest="streammode",
        help="Stream output to stdout only; default false",
    )
    arg_parser.add_argument(
        "--silent",
        default="false",
        dest="silent",
        help="Disable stdout output; default false",
    )
    arg_parser.add_argument(
        "--human-dates",
        default="false",
        dest="humandates",
        help="Human friendly datetime; default false",
    )
    arg_parser.add_argument(
        "--tg-token",
        dest="tg_token",
        help="Telegram bot token",
    )
    args = arg_parser.parse_args()

    print(red("Starting stream-lnd-htlcs:"))
    for k, v in args.__dict__.items():
        print(f"{blue(k):<20}: {white(v)}")

    lnd = Lnd(args.lnddir)

    x = threading.Thread(
        target=thread_function,
        args=(lnd, args),
        daemon=bool(args.tg_token),
    )
    x.start()

    if args.tg_token is not None:
        bot_main(args.tg_token)


if __name__ == "__main__":
    main()
