#!/usr/bin/env python3

#                  __       __   __
#   _______  __ __/ /____ _/ /  / /__   ___ ___  ___ ________
#  / __/ _ \/ // / __/ _ `/ _ \/ / -_) (_-</ _ \/ _ `/ __/ -_)
# /_/  \___/\_,_/\__/\_,_/_.__/_/\__(_)___/ .__/\_,_/\__/\__/
#                                        /_/
# We route payments.
# Provided as is. Use at own risk of being awesome.
#

import argparse
import json
import traceback

from simple_chalk import white, blue, red
import pandas as pd
import threading

from htlc import Htlc
from lnd import Lnd
from database import engine
import schemas
from tgbot import main as bot_main, update_logic


def flatten(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten(value).items():
                    yield key + "_" + subkey, subvalue
            else:
                yield key, value

    return dict(items())


def thread_function(lnd, args):
    for response in lnd.get_htlc_events():
        htlc = Htlc(lnd, response)
        print(htlc.__dict__)
        update_logic.update(htlc)
        obj = schemas.HTLC.parse_obj(flatten(htlc.__dict__))
        df = pd.DataFrame(data=[obj.dict()])
        df.to_sql("htlcs", if_exists="append", con=engine)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--lnd-dir",
        default="~/.lnd",
        dest="lnddir",
        help="lnd directory; default ~/.lnd",
    )
    arg_parser.add_argument(
        "--tg-token",
        dest="tg_token",
        help="Telegram bot token",
    )
    args = arg_parser.parse_args()

    print(red("Starting stream-lnd-htlcs-bot:"))
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
