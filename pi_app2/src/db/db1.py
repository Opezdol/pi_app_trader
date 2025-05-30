from datetime import datetime
from enum import Enum

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


## maybe route is more ideal
class Route(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    instId: str = Field(index=True, unique=True)
    created_at: datetime = Field(default=datetime.now())
    name: str | None = Field(default=None)

    ## Back populations
    deals: list["Deal"] = Relationship(back_populates="route")


class Trade_db(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime = Field(index=True)
    sz: float
    sz_mean: float
    sz_std: float
    sz_median: float
    base_vol: float
    side: Side

    ## Foreigh keys
    instrument_id: int = Field(index=True, foreign_key="route.id")


class Deal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime = Field(index=True)
    instAmount: float
    baseAmount: float
    side: Side

    ## Foreigh keys
    # to Trade table
    trade_ts: datetime | None = Field(index=True, foreign_key="trade_db.ts")
    # to instrument table
    route_id: int = Field(index=True, foreign_key="route.id")
    route: Route | None = Relationship(back_populates="deals")


sqlite_filename = "my_database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_instruments():
    btc = Route(instId="BTC-USDT", name="Bitcoin", created_at=datetime.now())
    eth = Route(instId="ETH-USDT", name="Etherium", created_at=datetime.now())
    ltc = Route(instId="LTC-USDT", name="Litecoin", created_at=datetime.now())
    ## we use Session to interact with db
    with Session(engine) as sess:
        # we build batch for commit
        try:
            sess.add(btc)
            sess.add(eth)
            sess.add(ltc)
            # and commit
            sess.commit()
            sess.refresh(btc)
            sess.refresh(ltc)
            sess.refresh(eth)
        except IntegrityError:
            print("INTERGITY ERROR!!!!!!!!: Already presented @ database")


def add_instrument(route: str) -> int | None:
    inst = Route(instId=route)
    with Session(engine) as sess:
        # get id if it is present
        statement = select(Route).where(Route.instId == route)
        ## .first returns None if not found.
        ## .one raises err
        res = sess.exec(statement).first()
        if res:
            return res.id
        else:
            try:
                sess.add(inst)
                sess.commit()
                sess.refresh(inst)
                return inst.id
            except IntegrityError:
                print(
                    f" INTERGITY ERROR MABOY!!!! Review your code. Somehow already presented @ database {res}"
                )


def get_routes() -> dict[str, Route]:
    with Session(engine) as s:
        statement = select(Route)
        res = s.exec(statement)
        d_res = {}
        for route in res:
            d_res[route.instId] = route
        return d_res


def main():
    create_db_and_tables()
    # create_instruments()
    ltc_id = add_instrument("LTC-USDT")
    btc_id = add_instrument("BTC-USDT")
    atom_id = add_instrument("ATOM-USDT")
    print(ltc_id, btc_id, atom_id)


if __name__ == "__main__":
    main()
