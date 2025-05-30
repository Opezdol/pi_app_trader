### Remember Biatch YOU! use SSE to update your frontend. Just because mthfcr.

# base example imports
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# my imports
from watchdog import WatchDog
from markets.OKX.public import PublicClient, Route
from routes.db_route import db
from routes import sse

## Create PublicAPI for connection && state for it
pubAPI = PublicClient.get_instance()
# dug = WatchDog(pub_client=pubAPI)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    ## add my fucntions to run cocurently with FastAPI
    public_task = asyncio.create_task(pubAPI())
    await asyncio.sleep(2)
    # watchdog_task = asyncio.create_task(dug.recursive_minute())
    yield
    # logger.info("Shutting down...")
    public_task.cancel()
    # watchdog_task.cancel()
    # logger.info("Finished shutting down.")


def get_app() -> FastAPI:
    app = FastAPI(title="PiAppBackend", lifespan=lifespan)
    origins = ["http://localhost:5173", "localhost:5173"]
    # origins = ["http://localhost:3000", "localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # ____________ROUTES ZONE_________
    app.include_router(db.router)
    app.include_router(sse.router)

    @app.get("/market_usdt", response_model=list[Route])
    async def get_usdt_market():
        return pubAPI.get_routes()

    return app


app = get_app()
