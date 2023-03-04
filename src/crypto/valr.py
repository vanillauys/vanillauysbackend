# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import httpx
import asyncio
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- VALR Crypto Exchange Rates --------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Valr():

    cryptos = {
        'BTCZAR': 'Bitcoin',
        'ETHZAR': 'Ethereum',
        'XRPZAR': 'Ripple XRP',
        'SOLZAR': 'Solana',
        'BNBZAR': 'Binance Coin',
        'USDCZAR': 'USD Coin',
        'SHIBZAR': 'Shib Token',
        'AVAXZAR': 'Avalanche'
    }

    def url(self, pair: str) -> str:
        return f"https://api.valr.com/v1/public/{pair}/marketsummary"


    def get_url_list(self) -> list:
        urls = [0] * 8
        for index, (key, _) in enumerate(self.cryptos.items()):
            urls[index] = self.url(key)
        return urls


    def formatted(self, values: list) -> list[Dict[str, float]]:
        results = [0] * 8
        for index, value in enumerate(values):
            results[index] = {
                'name': self.cryptos[value['currencyPair']],
                'price': value['lastTradedPrice'],
                'change': value['changeFromPrevious']
            }
        return results


    async def get_exchange_rates(self) -> Tuple[int, str, list[Dict[str, float]]]:
        values = [0] * 8
        urls = self.get_url_list()
        headers = {}
        async with httpx.AsyncClient() as client:
            reqs = [client.get(url, headers=headers) for url in urls]
            results = await asyncio.gather(*reqs)

        try:
            for index, value in enumerate(results):
                values[index] = value.json()
            print(f"VALUES IS: {values}")
            return 200, 'successfully received exchange rate from valr.', self.formatted(values)
        except Exception:
            return 500, 'error receiving exchange rate from valr.', None


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    # Nothing to do here
    pass


if __name__ == '__main__':
    main()
