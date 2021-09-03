#!/usr/bin/env python

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from textwrap import dedent

shared_data = {"update": None, "filter": None}


def help_func(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        dedent(
            """
            Use /start to start receiving events
            Use /filter <filter> a jq select
            Use /stop to stop receiving events

            Filter examples:

            # filter for failed events
            /filter select( .event_outcome | contains("link_fail_event"))

            # filter for failed events, and format to plain text
            /filter select( .event_outcome | contains("link_fail_event")) | to_entries[] | "\(.key)=\(.value)" 
            """
        )
    )


def filter_func(update: Update, context: CallbackContext) -> None:
    print(context.args)
    shared_data["filter"] = " ".join(context.args)
    update.message.reply_text("Filter set.")


def start(update: Update, context: CallbackContext) -> None:
    shared_data["update"] = update
    update.message.reply_text("Starting. You'll recieve events here as they occur.")


def stop(update: Update, context: CallbackContext) -> None:
    shared_data["update"] = None
    update.message.reply_text("Stopping.")


def main(token) -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("filter", filter_func))
    dispatcher.add_handler(CommandHandler("help", help_func))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
