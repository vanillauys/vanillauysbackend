# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import httpx
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- VALR Crypto Exchange Rates --------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Valr():

    def url(self, pair: str) -> str:
        return f"https://api.valr.com/v1/public/{pair}/marketsummary"


    def formatted(self, values: list) -> list[Dict[str, float]]:
        results = []
        results.append({
            'name': 'Bitcoin',
            'price': values[0]['lastTradedPrice'],
            'change': values[0]['changeFromPrevious']
        })
        results.append({
            'name': 'Ethereum',
            'price': values[1]['lastTradedPrice'],
            'change': values[1]['changeFromPrevious']
        })
        results.append({
            'name': 'Ripple XRP',
            'price': values[2]['lastTradedPrice'],
            'change': values[2]['changeFromPrevious']
        })
        results.append({
            'name': 'Solana',
            'price': values[3]['lastTradedPrice'],
            'change': values[3]['changeFromPrevious']
        })
        results.append({
            'name': 'Binance Coin',
            'price': values[4]['lastTradedPrice'],
            'change': values[4]['changeFromPrevious']
        })
        results.append({
            'name': 'USD Coin',
            'price': values[5]['lastTradedPrice'],
            'change': values[5]['changeFromPrevious']
        })
        results.append({
            'name': 'Shib Token',
            'price': values[6]['lastTradedPrice'],
            'change': values[6]['changeFromPrevious']
        })
        results.append({
            'name': 'Avalanche',
            'price': values[7]['lastTradedPrice'],
            'change': values[7]['changeFromPrevious']
        })
        return results


    async def get_exchange_rates(self) -> Tuple[int, str, list[Dict[str, float]]]:
        async with httpx.AsyncClient() as client:
            btc = await client.get(self.url('BTCZAR'), headers={})
            eth = await client.get(self.url('ETHZAR'), headers={})
            xrp = await client.get(self.url('XRPZAR'), headers={})
            sol = await client.get(self.url('SOLZAR'), headers={})
            bnb = await client.get(self.url('BNBZAR'), headers={})
            usdc = await client.get(self.url('USDCZAR'), headers={})
            shib = await client.get(self.url('SHIBZAR'), headers={})
            avax = await client.get(self.url('AVAXZAR'), headers={})

        try:
            values = [
                btc.json(),
                eth.json(),
                xrp.json(),
                sol.json(),
                bnb.json(),
                usdc.json(),
                shib.json(),
                avax.json()
            ]

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
