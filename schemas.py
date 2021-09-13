from typing import List, Optional, Any, Union
from pydantic import BaseModel
from datetime import datetime


class HTLC(BaseModel):

    # Incoming
    incoming_channel: Optional[str]
    incoming_channel_id: Optional[str]
    incoming_channel_capacity: Optional[int]
    incoming_channel_remote_balance: Optional[int]
    incoming_channel_local_balance: Optional[int]

    # Outoging
    outgoing_channel: Optional[str]
    outoming_channel_id: Optional[str]
    outgoing_channel_capacity: Optional[int]
    outgoing_channel_remote_balance: Optional[int]
    outgoing_channel_local_balance: Optional[int]

    timestamp: Optional[datetime]
    event_type: Optional[str]

    # Outcome
    wire_failure: Optional[str]
    failure_detail: Optional[str]
    failure_string: Optional[str]
    event_outcome: Optional[str]
    event_outcome_info_incoming_timelock: Optional[int]
    event_outcome_info_outgoing_timelock: Optional[int]
    event_outcome_info_incoming_amt_msat: Optional[int]
    event_outcome_info_outgoing_amt_msat: Optional[int]
