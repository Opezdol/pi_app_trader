from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError

from .db_models import (
    Route_DB,
    Route_Public,
    Transaction,
    Transaction_Create,
    Transaction_Public,
)

from sqlmodel import SQLModel, Session, create_engine, select

from markets.OKX.public import PublicClient

# _________________________________
#  Database connection && Session
# ----------------------------------
sqlite_file_name = "transactions.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
## we need publicClient to subscribe @ init and during update
pubAPI = PublicClient.get_instance()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

sqlite_filename = "my_database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = create_engine(sqlite_url, echo=True)


# __________ END______________


# _________________________________
# Internal function
# _________________________________


async def add_route(route: str) -> Route_DB:
    try:
        with Session(engine) as sess:
            inst = Route_DB(instId=route)
            sess.add(inst)
            sess.commit()
            sess.refresh(inst)
            ## And also subscribe
            await pubAPI.subscribe(inst.name)
            return inst
    except IntegrityError:
        print("IntegrityError")
        raise KeyError


async def get_route(route: str) -> Route_DB:
    # get id if it is present
    with Session(engine) as sess:
        statement = select(Route_DB).where(Route_DB.name == route)
        # .first returns None if not found.
        # .one raises err
        res = sess.exec(statement).first()
        if not res:
            res = await add_route(route=route)
        return res


def get_routes() -> list[str]:
    """We return list if target names to pass it to subscribe fucntion directly"""
    with Session(engine) as sess:
        statement = select(Route_DB)
        res = sess.exec(statement).all()
        return [target.name for target in res]


@asynccontextmanager
async def lifespan(app: APIRouter) -> AsyncGenerator[None, None]:
    ## Create my_database
    create_db_and_tables()

    ## subscribe to already set routes.
    await pubAPI.subscribe_many(get_routes())
    ## add my fucntions to run cocurently with FastAPI
    yield
    # logger.info("Shutting down db...")


router = APIRouter(prefix="/db", lifespan=lifespan)


# _________________________________
# DB routes definitions
# _________________________________


@router.get("/route/{id}", tags=["routes"], response_model=Route_Public)
def get_route_by_id(id: int, sess: SessionDep):
    res = sess.get(Route_DB, id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Route_DB with id: {id} not found")
    return res


@router.get("/trans", tags=["transactions"], response_model=list[Transaction_Public])
def read_all_transaction(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=25, le=25),
    # limit: Annotated[int, Query(le=100)] = 100
):
    transactions = session.exec(select(Transaction).offset(offset).limit(limit)).all()
    print("________TransactionsALL_________")
    print(transactions)
    return transactions


@router.post("/trans", tags=["transactions"], response_model=Transaction_Public)
async def create_transaction(*, sess: SessionDep, deal: Transaction_Create):
    # get || create Route_DB
    rt_obj = await get_route(route=deal.route)
    # update model via dict.
    obj = deal.model_dump()
    # update at this stage gives an ERROR WHYYYYYYYY>>>
    print("------" * 10)
    print(obj)
    # obj.update(route=rt_obj)
    # print(obj)
    tr = Transaction.model_validate(obj)
    ## UPdate here  - OK WHYYYYYYYYY
    tr.route = rt_obj
    # print(tr)
    sess.add(tr)
    sess.commit()
    sess.refresh(tr)
    return tr


@router.delete("/trans/{id}", tags=["transactions"])
def delete_transaction(id: int, sess: SessionDep):
    res = sess.get(Transaction, id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Route_DB with id: {id} not found")
    sess.delete(res)
    sess.commit()
    return {"ok": True}


@router.get("/trans/{id}", tags=["transactions"], response_model=Transaction_Public)
def read_transaction(*, sess: SessionDep, id: int):
    trans = sess.get(Transaction, id)
    if not trans:
        raise HTTPException(
            status_code=404, detail=f"Transaction with id: {id} not found"
        )
    return trans


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
