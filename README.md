# Asynchronous CoinGecko API wrapper
[![PyPi Version](https://img.shields.io/pypi/v/aiocoingecko.svg)](https://pypi.python.org/pypi/aiocoingecko/)

Python3 wrapper around the [CoinGecko](https://www.coingecko.com/) API (V3)

Features 100% API implementation and full Pythonic documentation.

### Notice

CoinGecko now requires a free API key to access its API. You can pass your API key into the `AsyncCoinGeckoAPISession`
constructor like below:

```python
from aiocoingecko import AsyncCoinGeckoAPISession

AsyncCoinGeckoAPISession(demo_api_key="CG-GuQ43vEyHED1dQCV3b46X3a7")
```

### Installation

PyPI
```bash
pip install aiocoingecko
```

### Usage

```python
import asyncio

from aiocoingecko import AsyncCoinGeckoAPISession


async def main():
    async with AsyncCoinGeckoAPISession() as cg:
        print(await cg.ping())

        
asyncio.run(main())
```
