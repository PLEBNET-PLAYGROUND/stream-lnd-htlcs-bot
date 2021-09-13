from telegram import Update
from telegram.ext import CallbackContext
import pandas as pd
import matplotlib as mpl
import traceback
from plugins.lib.utils import TempImage
import numpy as np
import matplotlib.pyplot as plt

mpl.use("Agg")


def main(update: Update, context: CallbackContext) -> None:
    """
    Generate plots of incoming and outgoing link fail event channels
    """
    try:
        # ask user to be patient
        update.message.reply_text("Generating pretty fail report")

        # load dataframe from db
        df = pd.read_sql_table("htlcs", "sqlite:///stream-lnd-htlcs-bot.db").set_index(
            "timestamp"
        )

        # load x as temporal
        df.index = pd.to_datetime(df.index)

        def get_fail_table(df, direction, debug=False):
            """
            Generate the failure table for incoming / outgoing channels.
            Probably a pandaesque way of doing this.
            """
            # Filter for failed link events with insufficient balance (naughty naughty!)
            # then select the (incoming|outgoing)_channel
            channel = link_fail_events = df[
                (df["event_outcome"] == "link_fail_event")
                & (df["failure_detail"] == "INSUFFICIENT_BALANCE")
            ][f"{direction}_channel"]
            # Create a dataframe, with channel names as columns, and times as indices
            # columns are sorted for consistency in channel colouring
            table = pd.DataFrame(
                columns=set(sorted(channel.values)), index=channel.index
            ).fillna(0)
            # Looping is not the pandas way, there must be a built-in for this
            for v in set(channel.index):
                table.loc[v, channel[v]] = 1
            # worth experimenting with resampling with either .sum() or .mean()
            table = table.resample("10min").sum()

            # let's use an exponential 6 hour half-life moving window
            # table = (
            #     table.ewm(halflife="6 hours", times=table.index)
            #     .mean()
            #     .fillna(0)  # replace NaNs with 0s
            # )
            if debug:
                table.to_csv(f"link_fail_events_{direction}.csv")
            return table

        fig, axes = plt.subplots(nrows=2, ncols=1)

        for i, direction in enumerate(("incoming", "outgoing")):
            get_fail_table(df, direction).plot.line(
                ax=axes[i],
                rot=0,
                title=f"{direction} link_fail_event channel(s)",
                figsize=(8, 7),
            )
        fig.tight_layout()
        with TempImage() as f:
            fig.savefig(f.name)
            update.message.reply_photo(photo=open(f.name, "rb"))
    except:
        update.message.reply_text(str(traceback.format_exc()))
