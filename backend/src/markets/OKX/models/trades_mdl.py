from typing import Optional

from pydantic import BaseModel


class Trade(BaseModel):
    instId: str
    tradeId: str
    px: float
    sz: float
    side: str
    ts: int
    count: Optional[int] = None


class TradesData(BaseModel):
    channel: str
    trades: list[Trade]


def parse_trade_data(json_data: dict) -> TradesData:
    return TradesData(**json_data)


# Example usage:
if __name__ == "__main__":

    data_json = {
        "arg": {"channel": "trades", "instId": "BTC-USDT"},
        "data": [
            {
                "instId": "BTC-USDT",
                "tradeId": "130639474",
                "px": "42219.9",
                "sz": "0.12060306",
                "side": "buy",
                "ts": "1630048897897",
                "count": "3",
            }
        ],
    }

    parsed_data = parse_trade_data(data_json)
    print(parsed_data)
