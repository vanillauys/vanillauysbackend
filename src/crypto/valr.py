# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import typer
from rich import print
import httpx
import asyncio


# ---------------------------------------------------------------------------- #
# --- VALR Crypto Exchange Rates --------------------------------------------- #
# ---------------------------------------------------------------------------- #


def url(pair: str):
    return f"https://api.valr.com/v1/public/{pair}/marketsummary"


def formatted(values: list):
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


async def get_exchange_rates():
    async with httpx.AsyncClient() as client:
        btc = await client.get(url('BTCZAR'), headers={})
        eth = await client.get(url('ETHZAR'), headers={})
        xrp = await client.get(url('XRPZAR'), headers={})
        sol = await client.get(url('SOLZAR'), headers={})
        bnb = await client.get(url('BNBZAR'), headers={})
        usdc = await client.get(url('USDCZAR'), headers={})
        shib = await client.get(url('SHIBZAR'), headers={})
        avax = await client.get(url('AVAXZAR'), headers={})

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

        return True, formatted(values)
    except Exception as e:
        print(e)
        return False, None


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    rates = asyncio.run(get_exchange_rates())
    for rate in rates:
        print(rate)
        print('---------')


if __name__ == '__main__':
    typer.run(main)
