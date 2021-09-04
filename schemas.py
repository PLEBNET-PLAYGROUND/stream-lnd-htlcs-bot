#                  __       __   __
#   _______  __ __/ /____ _/ /  / /__   ___ ___  ___ ________
#  / __/ _ \/ // / __/ _ `/ _ \/ / -_) (_-</ _ \/ _ `/ __/ -_)
# /_/  \___/\_,_/\__/\_,_/_.__/_/\__(_)___/ .__/\_,_/\__/\__/
#                                        /_/
# We route payments.
# Provided as is. Use at own risk of being awesome.
#

from typing import List, Optional, Any, Union
from pydantic import BaseModel
from datetime import datetime


class HTLC(BaseModel):
    incoming_channel: str
    incoming_channel_capacity: Optional[int]
    incoming_channel_remote_balance: Optional[int]
    incoming_channel_local_balance: Optional[int]
    outgoing_channel: str
    outgoing_channel_capacity: int
    outgoing_channel_remote_balance: int
    outgoing_channel_local_balance: int
    timestamp: datetime
    event_type: str
    event_outcome: str
    event_outcome_info_incoming_timelock: Optional[int]
    event_outcome_info_outgoing_timelock: Optional[int]
    event_outcome_info_incoming_amt_msat: Optional[int]
    event_outcome_info_outgoing_amt_msat: Optional[int]
