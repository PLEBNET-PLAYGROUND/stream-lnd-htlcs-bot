#!/usr/bin/env python

import os
import traceback
import importlib
from glob import glob
import inspect
from textwrap import dedent
from functools import partial

import jq

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


class UpdateLogic:

    _filter = ""
    _updater = None
    _start = False
    _chat_id = None
    send_message = None

    def init(self, updater):
        self._chat_id = None
        self._updater = updater
        if os.path.exists("connect.txt"):
            with open("connect.txt") as f:
                self._chat_id = int(f.read().strip())
                self.init_funcs()
                self.greet()

    def init_funcs(self):
        self.send_message = partial(
            self._updater.bot.send_message, chat_id=self._chat_id
        )

    def connect(self, chat_id):
        with open("connect.txt", "w") as f:
            f.write(str(chat_id))
            self._chat_id = chat_id
        self.init_funcs()

    def filter(self, htlc):
        try:
            return jq.compile(self._filter).input(htlc.__dict__).text()
        except:
            return str(traceback.format_exc())

    def update(self, htlc):
        if self._start and self.send_message:
            txt = self.filter(htlc) if self._filter else str(htlc.__dict__)
            if txt:
                self.send_message(text=txt)

    def greet(self):
        if self.send_message:
            self.send_message(text="Connected")


update_logic = UpdateLogic()

plugins = []


def help_func(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        dedent(
            """
            /connect run this so the bot can initiate chats with you
            /start start receiving events
            /stop to stop receiving events
            /filter <filter> a jq select (see examples)

            Plugins:

            """
        )
        + "\n".join(plugins)
        + dedent(
            """


            Filter examples:

            # filter for failed events
            /filter select( .event_outcome | contains("link_fail_event"))

            # filter for failed events, and format to plain text
            /filter select( .event_outcome | contains("link_fail_event")) | to_entries[] | "\(.key)=\(.value)"

            # filter for failed events, but exclude probes
            /filter select( (.event_outcome | contains("link_fail_event")) and (.failure_detail | contains("UNKNOWN_INVOICE") | not) )
            """
        )
    )


def filter_func(update: Update, context: CallbackContext) -> None:
    print(context.args)
    update_logic._filter = " ".join(context.args)
    update.message.reply_text("Filter set.")


def start(update: Update, context: CallbackContext) -> None:
    update_logic._start = True
    update.message.reply_text("Starting. You'll recieve events here as they occur.")


def stop(update: Update, context: CallbackContext) -> None:
    update_logic._start = False
    update.message.reply_text("Stopping.")


def connect(update: Update, context: CallbackContext) -> None:
    update_logic.connect(update.message.chat_id)
    update.message.reply_text(f"Connected.")


def main(token) -> None:
    updater = Updater(token)
    update_logic.init(updater)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("filter", filter_func))
    dispatcher.add_handler(CommandHandler("help", help_func))
    dispatcher.add_handler(CommandHandler("connect", connect))

    for plug in glob("plugins/*.py"):
        print(f"Loading plugin: {plug}")
        try:
            main = importlib.import_module(
                os.path.splitext(plug)[0].replace("/", ".")
            ).main
            cmd = os.path.splitext(plug)[0].split("/")[-1]
            plugins.append(f"/{cmd} {inspect.getdoc(main)}")
            dispatcher.add_handler(CommandHandler(cmd, main))
            print(f"Loaded")
        except:
            print(f"Failed loading: {plug}")
            print(str(traceback.format_exc()))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
