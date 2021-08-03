import unittest
import aiocoingecko


class AsyncCoinGeckoAPISessionTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._async_coin_gecko_api_session = aiocoingecko.AsyncCoinGeckoAPISession()

    async def asyncSetUp(self) -> None:
        self._async_coin_gecko_api_session = await self._async_coin_gecko_api_session.__aenter__()

    async def runTest(self):
        await self._async_coin_gecko_api_session.ping()
        await self._async_coin_gecko_api_session.get_price("ethereum", "usd")
        await self._async_coin_gecko_api_session.get_supported_vs_currencies()

    async def asyncTearDown(self) -> None:
        await self._async_coin_gecko_api_session.__aexit__(None, None, None)  # Not ideal.


if __name__ == "__main__":
    unittest.main()
