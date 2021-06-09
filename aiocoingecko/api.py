import json
from typing import Union

from aiohttp import ClientSession

from .errors import *


class AsyncCoinGeckoAPISession:
    _API_URL_BASE = 'https://api.coingecko.com/api/v3/'

    def __init__(self, api_base_url: str = _API_URL_BASE, *, client_session: ClientSession = None) -> None:
        self.api_base_url = api_base_url

        self._client_session = client_session
        self._client_session_is_passed = self._client_session is not None

    async def __aenter__(self):
        if not self._client_session_is_passed:
            self._client_session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._client_session_is_passed:
            await self._client_session.close()

    async def request(self, route: str, **kwargs):
        """Used to make interaction with the CoinGecko API.

        :argument route The route to make the GET request on.
        :argument kwargs Query parameters to use during the request."""

        async with self._client_session.get(self.api_base_url + route, params=kwargs) as response:
            if response.ok:
                try:
                    return await response.json()
                except json.decoder.JSONDecodeError:
                    raise UnknownResponse(resp=response)
            elif response.status == 429:
                raise RatelimitException(response.reason)
            else:
                raise HTTPException(response.reason, status_code=response.status)

    # ping
    async def ping(self) -> str:
        """Check API server status"""

        return await self.request("ping")

    # simple
    async def get_price(self, ids: str, vs_currencies: str, **kwargs) -> dict:
        """Get the current price of any cryptocurrencies in any other supported currencies that you need.

        :argument ids id of coins, comma-separated if querying more than 1 coin
        :argument vs_currencies vs_currency of coins, comma-separated if querying more than 1 vs_currency"""

        kwargs['ids'] = ids.replace(' ', '')
        kwargs['vs_currencies'] = vs_currencies.replace(' ', '')

        return await self.request("simple/price", **kwargs)

    async def get_token_price(self, token_id: str, contract_addresses: str, vs_currencies: str, **kwargs) -> dict:
        """Get current price of tokens (using contract addresses)
        for a given platform in any other currency that you need.

        :argument token_id The id of the platform issuing tokens (See asset_platforms endpoint for list of options)
        :argument contact_addresses The contract address of tokens, comma separated"""

        kwargs['contract_addresses'] = contract_addresses.replace(' ', '')
        kwargs['vs_currencies'] = vs_currencies.replace(' ', '')

        return await self.request(f"simple/token_price/{token_id}", **kwargs)

    async def get_supported_vs_currencies(self, **kwargs) -> dict:
        """Get list of supported_vs_currencies."""

        return await self.request("simple/supported_vs_currencies", **kwargs)

    # coins
    async def get_coins_list(self, **kwargs) -> dict:
        """List all supported coins id, name and symbol (no pagination required)"""

        return await self.request("coins/list", **kwargs)

    async def get_coins_markets(self, vs_currency: str, **kwargs) -> dict:
        """List all supported coins price, market cap, volume, and market related data

        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)"""

        kwargs['vs_currency'] = vs_currency

        return await self.request("coins/markets", **kwargs)

    async def get_coin_by_id(self, coin_id: str, **kwargs) -> dict:
        """Get current data (name, price, market, ... including exchange tickers) for a coin

        :argument coin_id pass the coin id (can be obtained from /coins) eg. bitcoin"""

        return await self.request(f"coins/{coin_id}/", **kwargs)

    async def get_coin_ticker_by_id(self, coin_id: str, **kwargs) -> dict:
        """Get coin tickers (paginated to 100 items)

        :argument coin_id pass the coin id (can be obtained from /coins/list) eg. bitcoin"""

        return await self.request(f"coins/{coin_id}/tickers", **kwargs)

    async def get_coin_history_by_id(self, coin_id: str, date: str, **kwargs) -> dict:
        """Get historical data (name, price, market, stats) at a given date for a coin

        :argument coin_id pass the coin id (can be obtained from /coins) eg. bitcoin
        :argument date The date of data snapshot in dd-mm-yyyy eg. 30-12-2017"""

        kwargs['date'] = date

        return await self.request(f"coins/{coin_id}/history", **kwargs)

    async def get_coin_market_chart_by_id(
            self,
            coin_id: str,
            vs_currency: str,
            days: Union[int, str],
            **kwargs,
    ) -> dict:
        """Get historical market data include price, market cap, and 24h volume (granularity auto)

        :argument coin_id pass the coin id (can be obtained from /coins) eg. bitcoin
        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)
        :argument days Data up to number of days ago (eg. 1,14,30,max)"""

        kwargs["vs_currency"] = vs_currency
        kwargs["days"] = days

        return await self.request(f"coins/{coin_id}/market_chart", **kwargs)

    async def get_coin_market_chart_range_by_id(
            self,
            coin_id: str,
            vs_currency: str,
            from_timestamp: int,
            to_timestamp: int,
            **kwargs,
    ) -> dict:
        """Get historical market data include price, market cap, and 24h volume within a range of timestamp
        (granularity auto)

        :argument coin_id pass the coin id (can be obtained from /coins) eg. bitcoin
        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)
        :argument from_timestamp From date in UNIX Timestamp (eg. 1392577232)
        :argument to_timestamp To date in UNIX Timestamp (eg. 1422577232)"""

        kwargs["vs_currency"] = vs_currency
        kwargs["from"] = from_timestamp
        kwargs["to"] = to_timestamp

        return await self.request(f"coins/{coin_id}/market_chart/range", **kwargs)

    async def get_coin_status_updates_by_id(self, coin_id: str, **kwargs) -> dict:
        """Get status updates for a given coin

        :argument pass the coin id (can be obtained from /coins) eg. bitcoin"""

        return await self.request(f"coins/{coin_id}/status_updates", **kwargs)

    async def get_coin_ohlc_by_id(self, coin_id: str, vs_currency: str, days: Union[int, str], **kwargs) -> list:
        """Get coin's OHLC

        :argument coin_id pass the coin id (can be obtained from /coins/list) eg. bitcoin
        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)
        :argument days Data up to number of days ago (1/7/14/30/90/180/365/max)"""

        kwargs["vs_currency"] = vs_currency
        kwargs["days"] = days

        return await self.request(f"coins/{coin_id}/ohlc", **kwargs)

    # contract
    async def get_coin_info_from_contract_address_by_id(self, platform_id: str, contract_address: str, **kwargs) -> dict:
        """Get coin info from contract address

        :argument platform_id Asset platform (See asset_platforms endpoint for list of options)
        :argument contract_address Token’s contract address"""

        return await self.request(f"coins/{platform_id}/contract/{contract_address}", **kwargs)

    async def get_coin_market_chart_from_contract_address_by_id(
            self,
            platform_id: str,
            contract_address: str,
            vs_currency: str,
            days: Union[str, int],
            **kwargs,
    ) -> dict:
        """Get historical market data include price, market cap,
        and 24h volume (granularity auto) from a contract address

        :argument platform_id The id of the platform issuing tokens (See asset_platforms endpoint for list of options)
        :argument contract_address Token’s contract address
        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)
        :days Data up to number of days ago (eg. 1,14,30,max)"""

        kwargs["vs_currency"] = vs_currency
        kwargs["days"] = days

        return await self.request(f"coins/{platform_id}/contract/{contract_address}/market_chart/", **kwargs)

    async def get_coin_market_chart_range_from_contract_address_by_id(
            self,
            platform_id: str,
            contract_address: str,
            vs_currency: str,
            from_timestamp: int,
            to_timestamp: int,
            **kwargs,
    ) -> dict:
        """Get historical market data include price, market cap,
        and 24h volume within a range of timestamp (granularity auto) from a contract address

        :argument platform_id The id of the platform issuing tokens (See asset_platforms endpoint for list of options)
        :argument contract_address Token’s contract address
        :argument vs_currency The target currency of market data (usd, eur, jpy, etc.)
        :argument from_timestamp From date in UNIX Timestamp (eg. 1392577232)
        :argument to_timestamp To date in UNIX Timestamp (eg. 1422577232)"""

        kwargs["vs_currency"] = vs_currency
        kwargs["from"] = from_timestamp
        kwargs["to"] = to_timestamp

        return await self.request(f"coins/{platform_id}/contract/{contract_address}/market_chart/range", **kwargs)

    # asset_platforms
    async def get_asset_platforms(self, **kwargs) -> dict:
        """List all asset platforms (Blockchain networks)"""

        return await self.request("asset_platforms", **kwargs)

    # categories
    async def get_coins_categories_list(self, **kwargs) -> dict:
        """List all categories"""

        return await self.request("coins/categories/list", **kwargs)

    async def get_coins_categories(self, **kwargs) -> dict:
        """List all categories with market data"""

        return await self.request("coins/categories", **kwargs)

    # exchanges
    async def get_exchanges_list(self, **kwargs) -> dict:
        """List all exchanges"""

        return await self.request("exchanges", **kwargs)

    async def get_exchanges_id_name_list(self, **kwargs) -> dict:
        """List all supported markets token_id and name (no pagination required)"""

        return await self.request("exchanges/list", **kwargs)

    async def get_exchanges_by_id(self, exchange_id: str, **kwargs) -> dict:
        """Get exchange volume in BTC and tickers

        :argument exchange_id pass the exchange id (can be obtained from /exchanges/list) eg. binance"""

        return await self.request(f"exchanges/{exchange_id}", **kwargs)

    async def get_exchanges_tickers_by_id(self, exchange_id: str, **kwargs) -> dict:
        """Get exchange tickers (paginated, 100 tickers per page)

        :argument exchange_id pass the exchange id (can be obtained from /exchanges/list) eg. binance"""

        return await self.request(f"exchanges/{exchange_id}/tickers", **kwargs)

    async def get_exchanges_status_updates_by_id(self, exchange_id: str, **kwargs) -> dict:
        """Get status updates for a given exchange

        :argument exchange_id pass the exchange id (can be obtained from /exchanges/list) eg. binance"""

        return await self.request(f"exchanges/{exchange_id}/status_updates", **kwargs)

    async def get_exchanges_volume_chart_by_id(self, exchange_id: str, days: int, **kwargs) -> dict:
        """Get volume chart data for a given exchange

        :argument exchange_id pass the exchange id (can be obtained from /exchanges/list) eg. binance"""

        kwargs['days'] = days

        return await self.request(f"exchanges/{exchange_id}/volume_chart", **kwargs)

    # finance
    async def get_finance_platforms(self, **kwargs) -> dict:
        """List all finance platforms"""

        return await self.request("finance_platforms", **kwargs)

    async def get_finance_products(self, **kwargs) -> dict:
        """List all finance products"""

        return await self.request("finance_products", **kwargs)

    # indexes
    async def get_indexes(self, **kwargs) -> dict:
        """List all market indexes"""

        return await self.request("indexes", **kwargs)

    async def get_indexes_market_id_index_id(self, market_id: str, index_id: str, **kwargs):
        """get market index by market id and index id

        :argument market_id pass the market id (can be obtained from /exchanges/list)
        :argument index_id pass the index id (can be obtained from /indexes/list)"""

        return await self.request(f"indexes/{market_id}/{index_id}", **kwargs)

    async def get_indexes_list(self, **kwargs) -> dict:
        """list market indexes id and name"""

        return await self.request("indexes/list", **kwargs)

    # derivatives
    async def get_derivatives(self, **kwargs) -> dict:
        """List all derivative tickers"""

        return await self.request("derivatives", **kwargs)

    async def get_derivatives_exchanges(self, **kwargs) -> dict:
        """List all derivative exchanges"""

        return await self.request("derivatives/exchanges", **kwargs)

    async def get_derivatives_exchanges_by_id(self, derivative_id: str, **kwargs) -> dict:
        """show derivative exchange data

        :argument derivative_id pass the exchange id (can be obtained from derivatives/exchanges/list) eg. bitmex"""

        return await self.request(f"derivatives/exchanges/{derivative_id}", **kwargs)

    async def get_derivatives_exchanges_list(self, **kwargs) -> dict:
        """List all derivative exchanges name and identifier"""

        return await self.request("derivatives/exchanges/list", **kwargs)

    # status_updates
    async def get_status_updates(self, **kwargs) -> dict:
        """List all status_updates with data (description, category, created_at, user, user_title and pin)"""

        return await self.request("status_updates", **kwargs)

    # events
    async def get_events(self, **kwargs) -> dict:
        """Get events, paginated by 100"""

        return await self.request("events", **kwargs)

    async def get_events_countries(self, **kwargs) -> dict:
        """Get list of event countries"""

        return await self.request("events/countries", **kwargs)

    async def get_events_types(self, **kwargs) -> dict:
        """Get list of event types"""

        return await self.request("events/types", **kwargs)

    # exchange_rates
    async def get_exchange_rates(self, **kwargs) -> dict:
        """Get BTC-to-Currency exchange rates"""

        return await self.request("exchange_rates", **kwargs)

    # trending
    async def get_search_trending(self, **kwargs) -> dict:
        """Top-7 trending coins on CoinGecko as searched by users in the last 24 hours
        (Ordered by most popular first)"""

        return await self.request("search/trending", **kwargs)

    # global
    async def get_global(self, **kwargs) -> dict:
        """Get cryptocurrency global data"""

        return await self.request("global", **kwargs)

    async def get_global_decentralized_finance_defi(self, **kwargs) -> dict:
        """Get cryptocurrency global decentralized finance(defi) data"""

        return await self.request("global/decentralized_finance_defi", **kwargs)

    # companies (beta)
    async def get_companies_coin_treasuries(self, coin_id: str, **kwargs):
        """Get public companies bitcoin or ethereum holdings (Ordered by total holdings descending)

        :argument coin_id bitcoin or ethereum"""

        return await self.request(f"companies/public_treasury/{coin_id}", **kwargs)


__all__ = ["AsyncCoinGeckoAPISession"]
