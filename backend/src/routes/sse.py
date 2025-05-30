from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import uvicorn
from asyncio import sleep
from markets.OKX.public import PublicClient
from pydantic import BaseModel
import json


class SSEResp(BaseModel):
    instId: str
    bidPx: float
    askPx: float
    ts: int


router = APIRouter(prefix="/sse")


async def price_updates(pub: PublicClient):
    tickers = pub.tickers
    data = []
    for key in tickers.keys():
        data.append(SSEResp.model_validate(tickers[key].model_dump()))
    data = [i.model_dump() for i in data]
    yield f"event: message\ndata: {json.dumps(data)}\n\n"
    await sleep(3)


@router.get("/", response_model=list[SSEResp])
async def root(pub: PublicClient = Depends(PublicClient.get_instance)):
    return StreamingResponse(price_updates(pub), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(router, host="127.0.0.1", port=8000)
