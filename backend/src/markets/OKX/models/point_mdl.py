from typing import Optional

from pydantic import BaseModel

"""
    alias: Optional[str] = Field(default=None, exclude=True)
    auction_end_time: Optional[str] = Field(default=None)
    base_ccy: str
    category: Optional[str] = Field(default=None)
    cont_td_sw_time: Optional[int] = Field(default=None, exclude=True)
    ct_mult: Optional[str] = Field(default=None, exclude=True)
    ct_type: Optional[str] = Field(default=None, exclude=True)
    ct_val: Optional[str] = Field(default=None, exclude=True)
    ct_val_ccy: Optional[str] = Field(default=None)
    exp_time: Optional[str] = Field(default=None, exclude=True)
    future_settlement: Optional[bool] = Field(default=None, exclude=True)
    inst_family: Optional[str] = Field(default=None, exclude=True)
    inst_id: str
    inst_type: Optional[str] = Field(default=None, exclude=True)
    lever: Optional[str] = Field(default=None, exclude=True)
    list_time: Optional[int] = Field(default=None)
    lot_sz: Optional[float] = Field(default=None)
    max_iceberg_sz: float | None = Field(default=None)
    max_lmt_amt: Optional[str] = Field(default=None, exclude=True)
    max_lmt_sz: Optional[float] = Field(default=None)
    max_mkt_amt: Optional[str] = Field(default=None, exclude=True)
    max_mkt_sz: Optional[int] = Field(default=None)
    max_stop_sz: Optional[int] = Field(default=None, exclude=True)
    max_trigger_sz: float | None = Field(default=None)
    max_twap_sz: float | None = Field(default=None)
    min_sz: Optional[float] = Field(default=None)
    open_type: Optional[str] = Field(default=None)
    opt_type: Optional[str] = Field(default=None, exclude=True)
    quote_ccy: Optional[str] = Field(default=None)
    rule_type: Optional[str] = Field(default=None, exclude=True)
    settle_ccy: Optional[str] = Field(default=None, exclude=True)
    state: Optional[str] = Field(default=None)
    stk: Optional[str] = Field(default=None, exclude=True)
    tick_sz: float
    uly: Optional[str] = Field(default=None, exclude=True)
    """


class Route(BaseModel):
    baseCcy: str
    instId: str
    instType: str
    lotSz: float
    minSz: float
    quoteCcy: str
    state: str
    tickSz: float


class RecvMdl(BaseModel):
    code: str
    data: list[Route]
    msg: Optional[str]
