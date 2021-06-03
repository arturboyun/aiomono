from dataclasses import dataclass
from datetime import datetime


@dataclass
class Currency:
    currencyCodeA: int
    currencyCodeB: int
    date: int
    rateSell: float = None
    rateBuy: float = None
    rateCross: float = None

    def utc(self):
        return datetime.utcfromtimestamp(self.date)
