# Asynchronous CoinGecko API wrapper
[![PyPi Version](https://img.shields.io/pypi/v/aiocoingecko.svg)](https://pypi.python.org/pypi/aiocoingecko/)

Python3 wrapper around the [CoinGecko](https://www.coingecko.com/) API (V3)

Features 100% API implementation and full Pythonic documentation.

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
