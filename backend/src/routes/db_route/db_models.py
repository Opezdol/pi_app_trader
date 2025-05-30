from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship


# ----------------------------------
## DB SQLModel classes definitions
# ----------------------------------
class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Route_Base(SQLModel):
    name: str = Field(index=True, unique=True, alias="instId")


## maybe route is more ideal
class Route_DB(Route_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ## Back populations
    transactions: list["Transaction"] = Relationship(back_populates="route")


class Transaction_Base(SQLModel):
    side: Side = Field(index=True)
    instAmount: float
    baseAmount: float


class Transaction(Transaction_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime = Field(default=datetime.now())
    # ts: datetime = Field(index=True)
    ## Foreigh keys
    # to Route_DB table
    route_id: int | None = Field(default=None, foreign_key="route_db.id")
    route: Route_DB = Relationship(back_populates="transactions")
    # route_id: int = Field(index=True, foreign_key="Route_DB.id")
    # trade_ts: datetime | None = Field(index=True, foreign_key="trade_db.ts")
    #


class Transaction_Create(Transaction_Base):
    """When created we will have string here
    Before commit we will change it to Route_DB instance"""

    route: str


class Transaction_Public(Transaction_Base):
    id: int
    route: Route_DB


class Transaction_Less(Transaction_Base):
    id: int


class Route_Public(Route_Base):
    transactions: list[Transaction_Less]


"""

class Transaction_Resp(BaseModel):
    id: int
    route: str
    instAmount: float
    baseAmount: float
    side: str


class Subscription_DB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ## Foreigh keys
    instrument_id: int = Field(index=True, foreign_key="route_db.id")


class Trade_DB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime = Field(index=True)
    sz: float
    sz_mean: float
    sz_std: float
    sz_median: float
    base_vol: float
    side: Side
    ## Foreigh keys
    instrument_id: int = Field(index=True, foreign_key="Route_DB.id")

"""


# __________ END______________
