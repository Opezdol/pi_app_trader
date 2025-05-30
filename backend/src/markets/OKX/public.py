import asyncio
import json
import requests

## logger
import logging
import websockets

## Websockets && logging
from websockets.exceptions import ConnectionClosed

from .models.tickers_mdl import SpotData
from .models.trades_mdl import Trade
from .models.point_mdl import Route, RecvMdl
from .models.subscribe_mdl import Subscribe_msg, Ticker_Subscribe_Message


logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


class PublicClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PublicClient()  # instanciate Public class
        # now we can use it as dependency
        return cls._instance

    def __init__(self):
        self.url: str = "wss://ws.okx.com:8443/ws/v5/public"
        self.routes_url: str = (
            "https://www.okx.com/api/v5/public/instruments?instType=SPOT"
        )
        self.ws = None
        # Here we trace subscriptions to channel and subs confirmations
        self.subscribtion_status = {}
        # _______________
        # Zone not connected to websocket connection. Just data storing and sorting
        ## dict of tickers
        self.tickers: dict[str, SpotData] = {}
        ## list of trades raw dump  for future sorting
        self.trades: list[Trade] = []
        # _______________
        ## Points Zone
        # Once we started, we make REST API call, to get list of all available instruments
        self.routes: RecvMdl | None = None
        # we start app, we already should know what points we can select.
        self.get_routes()
        # Error bool for watchdig stop
        self.internal_error: bool = False

    def get_routes(self, market: str = "USDT") -> list[Route] | None:
        if not self.routes:
            self.update_points()

        return (
            [pnt for pnt in self.routes.data if pnt.quoteCcy == market]
            if self.routes
            else None
        )

    def update_points(self) -> None:
        """Update via RestAPI call to public point.
        save result into self.points
        Not async.
        """
        try:
            with requests.Session() as s:
                resp = s.get(self.routes_url)
                if resp.status_code != 200:
                    raise ConnectionRefusedError(f"Responce Error: {resp.status_code}")
                # self.points = [
                #    itm for itm in resp.json()["data"] if itm["quoteCcy"] == "USDT"
                # ]
                self.routes = RecvMdl(**resp.json())

        except Exception as e:
            log.error(f"update_points: Error happened: {e}")

    def get_state(self) -> tuple[dict[str, SpotData], list[Trade]]:
        """
        You get it, you lose it.
        Denull after you run this method
        """
        state = (self.tickers, self.trades)
        ## denull that shit
        self.trades = []
        self.tickers = {}
        return state

    async def connect(self):
        """Connects to the WebSocket server at the specified URL."""
        self.ws = await websockets.connect(self.url)
        log.info(f"Connected to {self.url}")

    async def subscribe(self, instId: str):
        """
        1. Sends subscribe message to API based on instId given.
        2. adds Key to in form self.channels_status[instId]= {'tickers': False, 'trades': False}

        """
        sub_msg = Subscribe_msg(
            op="subscribe",
            args=[
                Ticker_Subscribe_Message(instId=instId),
            ],
        )
        sub_trades = Subscribe_msg(
            op="subscribe",
            args=[
                Ticker_Subscribe_Message(channel="trades", instId=instId),
            ],
        )
        # are we connected or wha??
        if not self.ws:
            raise ConnectionError("WebSocket is not open; please call connect() first.")
        else:
            ## add key to self.channels_status
            self.subscribtion_status[instId] = {"tickers": False, "trades": False}
            await self.ws.send(sub_msg.model_dump_json())
            await self.ws.send(sub_trades.model_dump_json())

    async def subscribe_many(self, targets: list[str]):
        for item in targets:
            await self.subscribe(item)
            await asyncio.sleep(1)

    async def test_sub(self):
        """3 yield's to subscribe
        #route = self.subs_test_lst.pop()
        await self.subscribe(instId=route)
        """
        points = self.get_routes()
        if points:
            await self.subscribe(instId=points.pop(-1).instId)
            yield
            await self.subscribe(instId=points.pop(-1).instId)
            yield
            await self.subscribe(instId=points.pop(-1).instId)
            yield
        else:
            raise KeyError("No points in test_sub")

    async def receive_messages(self):
        """
        Receives messages from the WebSocket indefinitely.
        But... We have 4 kind of msgs to recv.
        1. tickers.
        2. trades.
        3. Subscription - error ( of types 1,2)
        4. Subscription - Success. (also of types 1,2)
        Ne dohuya li dlya odnoi func????!!
        """
        if not self.ws:
            raise ConnectionError("WebSocket is not open; please call connect() first.")
        else:
            while True:
                message = json.loads(await self.ws.recv())
                ## Do smth with msges
                # log.info(f" <<< {message}")
                # We need sorting some kind here
                ## TODO nahui!
                if "event" in message:
                    self.process_event(message)
                else:
                    self.process_data(message)

    def process_event(self, msg: dict):
        """Set flag to subscription status"""
        # ether we subscribed, or wwe failed to subscribe
        if msg["event"] == "error":
            log.error(f"{msg['code']} 8===) {msg['msg']}")
        elif msg["event"] == "subscribe":
            instId = msg["arg"]["instId"]
            channel = msg["arg"]["channel"]
            self.subscribtion_status[instId][channel] = True

    def process_data(self, msg: dict):
        ## Trades and ticker data flow in here
        channel = msg["arg"]["channel"]
        if channel == "trades":
            # append trades to deque
            trade = Trade(**msg["data"][0])
            self.trades.append(trade)
            log.debug(f" <<< Trades: {trade}")
        elif channel == "tickers":
            ## update tickers data
            spot = SpotData(**msg["data"][0])
            self.tickers[spot.instId] = spot
            log.debug(f" <<< Tickers: {spot}")

    async def __call__(self):
        """Run Async Client"""
        await self.connect()
        # Start receiving messages in a separate task to keep the connection open
        receive_task = asyncio.create_task(self.receive_messages())
        try:
            # Keep running and handle signals or commands as needed
            while True:
                # repoirt status every 10 sec
                await asyncio.sleep(10)
                log.info(f" PublicClient Status: {self.subscribtion_status}")

        except ConnectionClosed:
            log.info(
                f"PublicClient: DisConnected from {self.url}. Reconnecting in 5 sec..."
            )
            await asyncio.sleep(5)
            await self.__call__()

        except asyncio.CancelledError:
            log.info("RunPublicAPI(): Socket closed. Bye.")
        except Exception as e:
            log.error(f"!!!!!!!!!!!PublicClient - something strange happened:{e} ")
            self.internal_error = True
        finally:
            # Ensure the connection is closed gracefully when the client stops (e.g., due to an exception)
            receive_task.cancel()
            log.info(self.subscribtion_status)
            log.info(self.get_state())
            log.info(f"________PublicAPI:TRADES________\n\t{self.trades}")
            log.info(f"________PublicAPI:TICKERS_______\n\t{self.tickers}")
            if self.ws:
                await self.ws.close()


def testOkxPublic():
    pubAPI = PublicClient()
    print(pubAPI.get_routes())
    # asyncio.run(pubAPI(err={"pubAPI": False}))
    # test = pubAPI.get_routes(market="USDT")
    # print("_______" * 5)
    # print(f"Len: {len(test)}")
    # for i in test[:30]:
    #    print(i)


if __name__ == "__main__":
    testOkxPublic()
