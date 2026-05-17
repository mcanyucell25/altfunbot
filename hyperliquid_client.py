from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from eth_account import Account
import config

class HLClient:
    def __init__(self, private_key):
        self.account = Account.from_key(private_key)
        self.exchange = Exchange(self.account, config.HL_API)
        self.info = Info(config.HL_API)

    def price(self, coin):
        mids = self.info.all_mids()
        return mids.get(coin)

    def buy(self, coin, size):
        price = self.price(coin)
        if not price:
            return {"error": "Price not found"}

        return self.exchange.order(
            coin,
            True,
            size,
            price * 1.01,
            {"limit": {"tif": "Ioc"}}
        )

    def sell(self, coin, size):
        price = self.price(coin)
        if not price:
            return {"error": "Price not found"}

        return self.exchange.order(
            coin,
            False,
            size,
            price * 0.99,
            {"limit": {"tif": "Ioc"}}
        )

    def fee(self):
        return self.exchange.transfer(
            config.FEE_WALLET,
            config.FEE_AMOUNT
        )
