from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator


class Currency(BaseModel):
    currencyCodeA: int
    currencyCodeB: int
    date: int
    rateSell: float = None
    rateBuy: float = None
    rateCross: float = None

    def utc_date(self):
        return datetime.utcfromtimestamp(self.date)


class Account(BaseModel):
    id: str
    balance: float
    credit_limit: int
    type: str
    currency_code: int
    cashback_type: str
    maskedPan: Optional[List[str]] = None
    iban: Optional[str] = None

    @validator('balance', 'credit_limit', pre=True, always=True)
    def convert_to_money(cls, value):
        return value / 100

    class Config:
        fields = {
            'credit_limit': 'creditLimit',
            'currency_code': 'currencyCode',
            'cashback_type': 'cashbackType',
        }


class ClientInfo(BaseModel):
    id: str
    name: str
    webhook_url: str
    accounts: List[Account]

    class Config:
        fields = {'id': 'clientId', 'webhook_url': 'webHookUrl'}


class StatementItem(BaseModel):
    id: str
    time: int
    description: str
    mcc: int
    hold: bool
    amount: float
    operation_amount: int
    currency_code: int
    commission_rate: int
    cashback_amount: int
    balance: float
    comment: str = None
    receipt_id: str = None
    counter_edrpou: str = None
    counter_iban: str = None

    @validator('balance', 'amount', 'operation_amount', 'commission_rate', 'cashback_amount', pre=True, always=True)
    def convert_to_money(cls, value):
        return value / 100

    class Config:
        fields = {
            'operation_amount': 'operationAmount',
            'currency_code': 'currencyCode',
            'commission_rate': 'commissionRate',
            'cashback_amount': 'cashbackAmount',
            'receipt_id': 'receiptId',
            'counter_edrpou': 'counterEdrpou',
            'counter_iban': 'counterIban',
        }
