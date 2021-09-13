from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import pandas as pd

"""
Example stream-lnd-htlcs-bot plugin that:

- reads the db via Pandas
- exports the datafarme to a .xlsx file
- sends it as a response to the user
"""


def main(update: Update, context: CallbackContext) -> None:
    """
    Export HTLCs as excel file and send.
    """
    update.message.reply_text("Generating pretty report")
    pd.read_sql_table("htlcs", "sqlite:///stream-lnd-htlcs-bot.db").to_excel(
        "output.xlsx"
    )
    update.message.reply_document(document=open("output.xlsx", "rb"))
