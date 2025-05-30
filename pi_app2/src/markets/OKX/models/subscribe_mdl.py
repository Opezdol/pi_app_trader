from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class Account_Subscribe_Message(BaseModel):
    channel: Literal["account"] = "account"
    extraParams: Optional[str] = '{"updateInterval": "10"}'
    # ccy: Optional[str | None]


class Ticker_Subscribe_Message(BaseModel):
    channel: Literal["tickers", "trades"] = "tickers"
    instId: Optional[str]


class Subscribe_msg(BaseModel):
    """
    data_acc = {
        "op": "subscribe",
        "args": [
            {
                "channel": "account",
                # "ccy": "USDT",
                "extraParams": '{"updateInterval": "10"}',
            }
        ],
    }
    """

    op: str = "subscribe"
    args: list[Account_Subscribe_Message | Any] = [Account_Subscribe_Message()]


class Account_msg_recv(BaseModel):
    event: Optional[str] = Field(default=None, exclude=True)
    arg: Optional[dict] = Field(default=None, exclude=True)
    # data: Optional[list[Account_status]] = Field(default=None, exclude=False)
    channel: Optional[str] = Field(default=None, exclude=True)
