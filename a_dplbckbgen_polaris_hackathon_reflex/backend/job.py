from typing import Union
from datetime import datetime

import reflex as rx


class Job(rx.Base):
    """The job class."""
    scheduleid: str
    version: int
    date_utc: str
    direction: str
    power: float
    deliverypoint: str
