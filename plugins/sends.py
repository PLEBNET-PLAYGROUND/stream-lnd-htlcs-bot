#                  __       __   __
#   _______  __ __/ /____ _/ /  / /__   ___ ___  ___ ________
#  / __/ _ \/ // / __/ _ `/ _ \/ / -_) (_-</ _ \/ _ `/ __/ -_)
# /_/  \___/\_,_/\__/\_,_/_.__/_/\__(_)___/ .__/\_,_/\__/\__/
#                                        /_/
# We route payments.
# Provided as is. Use at own risk of being awesome.
#

from telegram import Update
from telegram.ext import CallbackContext
import pandas as pd
import matplotlib as mpl
import traceback

mpl.use("Agg")

"""
Example stream-lnd-htlcs-bot plugin that:

- reads the db via Pandas
- filters for SEND events
- splits into forwards, and failed forwards
- creates a new dataframe
- counts
- generates pretty bar chart
- saves as png
- sends it as a response to the user
"""


def main(update: Update, context: CallbackContext) -> None:
    """
    Generate a bar chart of SEND forward and fail events, and send.
    """
    try:
        update.message.reply_text("Generating pretty report")
        df = pd.read_sql_table("htlcs", "sqlite:///stream-lnd-htlcs-bot.db")
        sends = df[df["event_type"] == "SEND"]
        forward_event = sends[sends["event_outcome"] == "forward_event"]
        forward_fail_event = sends[sends["event_outcome"] == "forward_fail_event"]
        forward_counts = forward_event["outgoing_channel"].value_counts()
        forward_fail_counts = forward_fail_event["outgoing_channel"].value_counts()
        df = pd.DataFrame(
            {
                "forward_event": forward_counts,
                "forward_fail_event": forward_fail_counts,
            },
            index=forward_fail_counts.index,
        )
        if len(df):
            fig = df.plot.barh(rot=0, title="event_type: SEND").get_figure()
            fig.tight_layout()
            fig.savefig("failed_events.png")
            update.message.reply_photo(photo=open("failed_events.png", "rb"))
        else:
            update.message.reply_text("Not enough data")
    except:
        update.message.reply_text(str(traceback.format_exc()))
