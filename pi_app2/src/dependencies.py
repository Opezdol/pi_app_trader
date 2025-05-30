from fastapi import Depends
from typing import Annotated
import logging
from logging import INFO, basicConfig, getLogger


async def get_logger() -> logging.Logger:
    logger = getLogger(__name__)
    basicConfig(level=INFO)
    return logger


LoggerDep = Annotated[logging.Logger, Depends(get_logger)]
