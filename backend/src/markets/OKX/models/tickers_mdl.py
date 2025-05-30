from pydantic import BaseModel, Field


class FilteredSpot(BaseModel):
    # This model includes only the desired fields.
    instId: str = Field(..., description="The instrument ID")
    last: float = Field(..., description="The latest price")
    bidPx: float = Field(..., description="The bid price")
    bidSz: float = Field(..., description="The bid size")
    askPx: float = Field(..., description="The ask price")
    askSz: float = Field(..., description="The ask size")
    ts: int = Field(..., description="The timestamp")


class Arg(BaseModel):
    channel: str
    instId: str


class SpotData(BaseModel):

    instType: str = Field(..., description="The instrument type")
    instId: str = Field(..., description="The instrument ID")
    last: str = Field(..., description="The latest price")
    lastSz: str = Field(..., description="The size of the latest price")
    bidPx: float = Field(..., description="The bid price")
    bidSz: float = Field(..., description="The bid size")
    askPx: float = Field(..., description="The ask price")
    askSz: float = Field(..., description="The ask size")
    open24h: str = Field(..., description="The opening price in the last 24 hours")
    high24h: str = Field(..., description="The highest price in the last 24 hours")
    low24h: str = Field(..., description="The lowest price in the last 24 hours")
    volCcy24h: str = Field(
        ..., description="The volume in currency in the last 24 hours"
    )
    vol24h: str = Field(..., description="The volume in units in the last 24 hours")
    sodUtc0: str = Field(..., description="The start of day price at UTC0")
    sodUtc8: str = Field(..., description="The start of day price at UTC8")
    ts: int = Field(..., description="The timestamp")


class Response(BaseModel):
    arg: Arg
    data: list[SpotData] = Field(
        ..., min_length=1, max_length=1, description="it has len of 1"
    )

    def get_filtered_data(self) -> FilteredSpot:
        # This custom method returns instances of `FilteredSpotData`.
        return FilteredSpot(**self.data[0].model_dump())


if __name__ == "__main__":
    example_data = {
        "arg": {"channel": "tickers", "instId": "BTC-USDT"},
        "data": [
            {
                "instType": "SPOT",
                "instId": "BTC-USDT",
                "last": "9999.99",
                "lastSz": "0.1",
                "askPx": "9999.99",
                "askSz": "11",
                "bidPx": "8888.88",
                "bidSz": "5",
                "open24h": "9000",
                "high24h": "10000",
                "low24h": "8888.88",
                "volCcy24h": "2222",
                "vol24h": "2222",
                "sodUtc0": "2222",
                "sodUtc8": "2222",
                "ts": "1597026383085",
            }
        ],
    }
    response = Response(**example_data)
    filtered_data = response.get_filtered_data()
    print(filtered_data.model_dump_json())  # This prints the filtered attributes
