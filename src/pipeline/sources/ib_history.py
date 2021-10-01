from datetime import datetime
from typing import Iterator, List, Optional

from entities.candle import Candle
from entities.timespan import TimeSpan
from market.ib_market import IBMarketProvider
from pipeline.source import Source
from providers.ib.interactive_brokers_connector import InteractiveBrokersConnector


class IBHistorySource(Source):
    def __init__(self, ib_connector: InteractiveBrokersConnector, symbols: List[str], timespan: TimeSpan,
                 from_time: datetime, to_time: Optional[datetime] = datetime.now()) -> None:
        self.timespan = timespan
        self.to_time = to_time
        self.from_time = from_time
        self.marketProvider = IBMarketProvider(ib_connector)
        self.symbols = symbols

    def read(self) -> Iterator[Candle]:
        for symbol in self.symbols:
            result = self.marketProvider.request_symbol_history(symbol, self.timespan, self.from_time, self.to_time)
            for candle in result.result():
                yield candle
