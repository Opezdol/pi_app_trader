import asyncio
import logging
import os
import statistics
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from markets.OKX.public import Trade, PublicClient

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format="%(asctime)s - %(name)s: >>>> %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


class WatchDog:
    """every minute it creates post in database with trades happened,
    TODO: also i want him to trace BIG trades every 5 sec, and make alerts
    """

    def __init__(self, pub_client: PublicClient) -> None:
        self.pub = pub_client

    def trade_sorter(
        self, data: list[Trade]
    ):  # -> dict[Literal['buy', 'sell'], dict[str, list[Trade]]]:
        # routes = get_routes()
        ## set of happend trades
        inst_ids = {trade.instId for trade in data}
        ## dict[instId: Trade]
        d_sell = {k: [] for k in inst_ids}
        d_buy = {k: [] for k in inst_ids}
        # [d_trade[trade.instId].append(trade) for trade in data]
        for trade in data:
            if trade.side == "buy":
                d_buy[trade.instId].append(trade)
            elif trade.side == "sell":
                d_sell[trade.instId].append(trade)
            else:
                raise KeyError("Trade trade_sorter.side sotring error happened")
        print(f"Sell:\n {d_sell}")
        print(f"Buy:\n {d_buy}")

    def calc_stats(self, trades: list[Trade]):
        base_vol = [trade.px * trade.sz for trade in trades]
        inst_sz = [trade.sz for trade in trades]
        inst_px = [trade.px for trade in trades]
        trades_cnt = [trade.count for trade in trades]
        print(f"Mean size { statistics.mean(inst_sz)}")
        print(f"Mean size stddev {statistics.stdev(inst_sz)}")
        print(f"Mean base_vol { statistics.mean(base_vol)}")
        print(f"Price: {statistics.mean(inst_sz)/statistics.mean(base_vol)}")

    async def recursive_minute(self):
        try:
            while True:
                if self.pub.internal_error:
                    log.error(
                        "WathcDOg:: PubAPI caught Error. Stopping Wathcdog execution"
                    )
                    break
                await asyncio.sleep(30)
                close, trades = self.pub.get_state()
                log.info(f"____________close: {close}")
                log.info(f"____________trades:{trades}")
        except asyncio.CancelledError:
            log.info("Wathcdog Cancelled. ")


def main():

    def calc_stats_numpy(route: str, ts: int, trades: list[Trade]):
        inst_sz = np.array([trade.sz for trade in trades])
        base_vol = np.array([trade.px * trade.sz for trade in trades])
        trades_cnt = np.array([trade.count for trade in trades])
        print(f"Mean size { np.mean(inst_sz)}")
        print(f"Sum USDT { np.sum(base_vol)}")
        print(f"Sum COIN { np.sum(inst_sz)}")
        print(f"total trades { np.sum(trades_cnt)}")
        print(f"Mean size stddev {np.std(inst_sz)}")
        print(f"Mean base_vol { np.mean(base_vol)}")
        print(f"Price: {np.mean(base_vol)/np.mean(inst_sz)}")

    def trade_sorter(
        data: list[Trade],
    ):  # -> dict[Literal['buy', 'sell'], dict[str, list[Trade]]]:
        ## set of happend trades
        last_ts = data[-1].ts
        inst_ids = {trade.instId for trade in data}
        ## TODO: Get DB keys from inst_ids
        # ________________
        ## dict[instId: Trade]
        d_sell = {k: [] for k in inst_ids}
        d_buy = {k: [] for k in inst_ids}
        # Sort over side
        # [d_trade[trade.instId].append(trade) for trade in data]
        for trade in data:
            if trade.side == "buy":
                d_buy[trade.instId].append(trade)
            elif trade.side == "sell":
                d_sell[trade.instId].append(trade)
            else:
                raise KeyError("Trade trade_sorter.side sotring error happened")
        # looks like we need calulator f stats.
        # Stats gonna be saved for each Route on sell && buy route

    trades = [
        Trade(
            instId="ETH-USDT",
            tradeId="550081384",
            px=1896.68,
            sz=0.088286,
            side="sell",
            ts=1743163493858,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081385",
            px=1896.68,
            sz=0.090666,
            side="sell",
            ts=1743163494863,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081388",
            px=1896.68,
            sz=0.094077,
            side="sell",
            ts=1743163494942,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081389",
            px=1896.67,
            sz=0.002885,
            side="sell",
            ts=1743163494944,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081390",
            px=1896.65,
            sz=0.005693,
            side="sell",
            ts=1743163494944,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081394",
            px=1896.6,
            sz=0.002005,
            side="sell",
            ts=1743163494944,
            count=4,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081395",
            px=1896.56,
            sz=0.000532,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081396",
            px=1896.55,
            sz=0.00105,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081397",
            px=1896.5,
            sz=0.041791,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081398",
            px=1896.48,
            sz=0.0001,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081399",
            px=1896.45,
            sz=0.005762,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081400",
            px=1896.44,
            sz=0.265286,
            side="sell",
            ts=1743163494945,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081402",
            px=1896.43,
            sz=1.730609,
            side="sell",
            ts=1743163494946,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081403",
            px=1896.42,
            sz=0.3673,
            side="sell",
            ts=1743163494947,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081406",
            px=1896.4,
            sz=0.053438,
            side="sell",
            ts=1743163494947,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081407",
            px=1896.38,
            sz=0.001744,
            side="sell",
            ts=1743163494949,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081408",
            px=1896.37,
            sz=0.207054,
            side="sell",
            ts=1743163494949,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081409",
            px=1896.36,
            sz=0.0001,
            side="sell",
            ts=1743163494962,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081411",
            px=1896.31,
            sz=0.678077,
            side="sell",
            ts=1743163494962,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081412",
            px=1896.25,
            sz=0.000531,
            side="sell",
            ts=1743163494962,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081415",
            px=1896.24,
            sz=0.1201,
            side="sell",
            ts=1743163494962,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081417",
            px=1896.23,
            sz=0.101192,
            side="sell",
            ts=1743163494962,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081419",
            px=1896.21,
            sz=0.26386,
            side="sell",
            ts=1743163494963,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081422",
            px=1896.2,
            sz=0.63614,
            side="sell",
            ts=1743163494963,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081423",
            px=1896.29,
            sz=0.011757,
            side="sell",
            ts=1743163495076,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081424",
            px=1896.3,
            sz=0.007,
            side="buy",
            ts=1743163495641,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081425",
            px=1896.3,
            sz=0.088213,
            side="buy",
            ts=1743163495685,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081426",
            px=1896.3,
            sz=0.061129,
            side="buy",
            ts=1743163496339,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081434",
            px=1896.29,
            sz=7.80858,
            side="sell",
            ts=1743163496694,
            count=8,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081435",
            px=1896.28,
            sz=0.004802,
            side="sell",
            ts=1743163496694,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081436",
            px=1896.24,
            sz=1.199043,
            side="sell",
            ts=1743163496694,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081437",
            px=1896.23,
            sz=1.729951,
            side="sell",
            ts=1743163496694,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081440",
            px=1896.2,
            sz=12.910028,
            side="sell",
            ts=1743163496694,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081443",
            px=1896.19,
            sz=1.145724,
            side="sell",
            ts=1743163496694,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081444",
            px=1896.17,
            sz=0.0001,
            side="buy",
            ts=1743163496700,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081446",
            px=1896.16,
            sz=0.006838,
            side="sell",
            ts=1743163496769,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081447",
            px=1896.15,
            sz=0.004337,
            side="sell",
            ts=1743163496769,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081448",
            px=1896.1,
            sz=0.002612,
            side="sell",
            ts=1743163496936,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081449",
            px=1896.05,
            sz=0.01,
            side="sell",
            ts=1743163496937,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081451",
            px=1896.01,
            sz=0.028946,
            side="sell",
            ts=1743163496944,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081463",
            px=1896.0,
            sz=0.509058,
            side="sell",
            ts=1743163496981,
            count=12,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081464",
            px=1896.0,
            sz=0.051045,
            side="sell",
            ts=1743163496982,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081465",
            px=1895.98,
            sz=0.081,
            side="sell",
            ts=1743163496982,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081466",
            px=1895.97,
            sz=0.002684,
            side="sell",
            ts=1743163496982,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081468",
            px=1895.91,
            sz=0.003556,
            side="sell",
            ts=1743163496982,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081470",
            px=1895.88,
            sz=1.908316,
            side="sell",
            ts=1743163496982,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081471",
            px=1895.86,
            sz=0.000531,
            side="sell",
            ts=1743163496982,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081472",
            px=1895.71,
            sz=0.088124,
            side="sell",
            ts=1743163497412,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081473",
            px=1895.72,
            sz=0.013705,
            side="buy",
            ts=1743163497647,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081479",
            px=1895.71,
            sz=8.263181,
            side="sell",
            ts=1743163498645,
            count=6,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081482",
            px=1895.7,
            sz=2.307885,
            side="sell",
            ts=1743163498645,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081483",
            px=1895.67,
            sz=1.051286,
            side="sell",
            ts=1743163498645,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081484",
            px=1895.66,
            sz=0.999988,
            side="sell",
            ts=1743163498645,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081485",
            px=1895.66,
            sz=1.2e-05,
            side="sell",
            ts=1743163498645,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081487",
            px=1895.64,
            sz=0.147925,
            side="sell",
            ts=1743163498647,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081488",
            px=1895.62,
            sz=0.000531,
            side="sell",
            ts=1743163498647,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081491",
            px=1895.6,
            sz=0.251544,
            side="sell",
            ts=1743163498647,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081492",
            px=1895.6,
            sz=2.104286,
            side="sell",
            ts=1743163498647,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081493",
            px=1895.59,
            sz=1.053,
            side="sell",
            ts=1743163498647,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081496",
            px=1895.55,
            sz=0.3679,
            side="sell",
            ts=1743163498647,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081497",
            px=1895.52,
            sz=0.0001,
            side="sell",
            ts=1743163498647,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081499",
            px=1895.5,
            sz=2.344791,
            side="sell",
            ts=1743163498647,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081500",
            px=1895.69,
            sz=0.001281,
            side="buy",
            ts=1743163498648,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081501",
            px=1895.49,
            sz=0.663546,
            side="sell",
            ts=1743163498648,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081502",
            px=1895.48,
            sz=0.086174,
            side="sell",
            ts=1743163498648,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081503",
            px=1895.48,
            sz=0.361826,
            side="sell",
            ts=1743163498649,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081504",
            px=1895.47,
            sz=0.000531,
            side="sell",
            ts=1743163498649,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081506",
            px=1895.44,
            sz=1.821322,
            side="sell",
            ts=1743163498649,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081508",
            px=1895.43,
            sz=0.529406,
            side="sell",
            ts=1743163498649,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081509",
            px=1895.41,
            sz=0.342878,
            side="sell",
            ts=1743163498650,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081510",
            px=1895.35,
            sz=2.639026,
            side="sell",
            ts=1743163498650,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081511",
            px=1895.32,
            sz=0.0001,
            side="sell",
            ts=1743163498650,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081512",
            px=1895.31,
            sz=0.000533,
            side="sell",
            ts=1743163498650,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081513",
            px=1895.29,
            sz=0.004508,
            side="sell",
            ts=1743163498650,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081515",
            px=1895.27,
            sz=0.801436,
            side="sell",
            ts=1743163498650,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081516",
            px=1895.24,
            sz=0.105,
            side="buy",
            ts=1743163498704,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081518",
            px=1895.23,
            sz=0.001377,
            side="sell",
            ts=1743163499163,
            count=2,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081519",
            px=1895.22,
            sz=0.003599,
            side="sell",
            ts=1743163499163,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081522",
            px=1895.2,
            sz=0.056146,
            side="sell",
            ts=1743163499163,
            count=3,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081523",
            px=1895.18,
            sz=0.0001,
            side="sell",
            ts=1743163499163,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081524",
            px=1895.17,
            sz=0.002316,
            side="sell",
            ts=1743163499163,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081525",
            px=1895.16,
            sz=0.000531,
            side="sell",
            ts=1743163499163,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081526",
            px=1895.14,
            sz=0.000653,
            side="sell",
            ts=1743163499163,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081527",
            px=1895.04,
            sz=0.002688,
            side="sell",
            ts=1743163499268,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081528",
            px=1895.03,
            sz=0.001605,
            side="sell",
            ts=1743163499268,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081532",
            px=1895.01,
            sz=0.520123,
            side="sell",
            ts=1743163499268,
            count=4,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081538",
            px=1895.0,
            sz=1.246584,
            side="sell",
            ts=1743163499268,
            count=6,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456051",
            px=87.98,
            sz=0.7524,
            side="sell",
            ts=1743163499313,
            count=2,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456052",
            px=87.98,
            sz=8e-06,
            side="sell",
            ts=1743163499351,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081539",
            px=1895.01,
            sz=0.088068,
            side="buy",
            ts=1743163499491,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081540",
            px=1895.0,
            sz=0.393436,
            side="sell",
            ts=1743163499566,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081541",
            px=1895.0,
            sz=0.35373,
            side="sell",
            ts=1743163499567,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081542",
            px=1895.0,
            sz=0.683456,
            side="sell",
            ts=1743163499567,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081543",
            px=1895.0,
            sz=0.359831,
            side="sell",
            ts=1743163499567,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081544",
            px=1895.0,
            sz=0.202134,
            side="sell",
            ts=1743163499567,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081555",
            px=1895.0,
            sz=6.283,
            side="sell",
            ts=1743163499567,
            count=11,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081560",
            px=1895.0,
            sz=1.856383,
            side="sell",
            ts=1743163499567,
            count=5,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081561",
            px=1894.99,
            sz=0.001012,
            side="sell",
            ts=1743163499568,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081562",
            px=1894.95,
            sz=0.009352,
            side="sell",
            ts=1743163499568,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081563",
            px=1894.9,
            sz=0.014248,
            side="sell",
            ts=1743163499568,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081564",
            px=1894.87,
            sz=0.000718,
            side="sell",
            ts=1743163499573,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081565",
            px=1894.85,
            sz=0.000532,
            side="sell",
            ts=1743163499573,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081567",
            px=1894.84,
            sz=0.059001,
            side="sell",
            ts=1743163499579,
            count=2,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456053",
            px=87.97,
            sz=0.0132,
            side="sell",
            ts=1743163499583,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081568",
            px=1894.82,
            sz=0.00105,
            side="sell",
            ts=1743163499595,
            count=1,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456054",
            px=87.97,
            sz=2.4e-05,
            side="sell",
            ts=1743163499662,
            count=1,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456055",
            px=87.96,
            sz=0.017438,
            side="sell",
            ts=1743163499662,
            count=1,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456056",
            px=87.95,
            sz=0.162539,
            side="sell",
            ts=1743163499662,
            count=1,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456058",
            px=87.94,
            sz=0.189709,
            side="sell",
            ts=1743163499662,
            count=2,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456061",
            px=87.93,
            sz=0.63029,
            side="sell",
            ts=1743163499662,
            count=3,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456062",
            px=87.95,
            sz=0.01,
            side="buy",
            ts=1743163499676,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081569",
            px=1894.81,
            sz=0.005212,
            side="buy",
            ts=1743163499713,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081570",
            px=1894.81,
            sz=0.084809,
            side="buy",
            ts=1743163500219,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081571",
            px=1894.86,
            sz=1.00683,
            side="buy",
            ts=1743163500220,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081572",
            px=1894.88,
            sz=0.0001,
            side="buy",
            ts=1743163500220,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081573",
            px=1894.9,
            sz=0.739168,
            side="buy",
            ts=1743163500220,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081574",
            px=1894.9,
            sz=0.470717,
            side="buy",
            ts=1743163500223,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081575",
            px=1895.07,
            sz=0.094985,
            side="buy",
            ts=1743163500274,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081576",
            px=1895.2,
            sz=0.0001,
            side="buy",
            ts=1743163500355,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081577",
            px=1895.26,
            sz=0.001059,
            side="sell",
            ts=1743163500544,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081578",
            px=1895.2,
            sz=0.0001,
            side="sell",
            ts=1743163500548,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081579",
            px=1895.01,
            sz=0.32,
            side="buy",
            ts=1743163500729,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081580",
            px=1895.14,
            sz=0.001221,
            side="sell",
            ts=1743163500846,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081581",
            px=1894.97,
            sz=0.000586,
            side="sell",
            ts=1743163501074,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081582",
            px=1894.88,
            sz=0.003,
            side="buy",
            ts=1743163501240,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081583",
            px=1894.88,
            sz=1.17,
            side="buy",
            ts=1743163501462,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081584",
            px=1894.99,
            sz=0.006,
            side="buy",
            ts=1743163501484,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081585",
            px=1894.99,
            sz=0.08798,
            side="sell",
            ts=1743163501617,
            count=1,
        ),
        Trade(
            instId="LTC-USDT",
            tradeId="154456063",
            px=87.95,
            sz=0.04165,
            side="buy",
            ts=1743163501926,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081586",
            px=1894.82,
            sz=0.053334,
            side="buy",
            ts=1743163502164,
            count=1,
        ),
        Trade(
            instId="ETH-USDT",
            tradeId="550081587",
            px=1894.82,
            sz=0.010095,
            side="buy",
            ts=1743163503063,
            count=1,
        ),
    ]
    trade_sorter(data=trades * 150)


if __name__ == "__main__":
    main()
