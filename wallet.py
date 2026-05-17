from eth_account import Account
import secrets

def create_wallet():
    private_key = "0x" + secrets.token_hex(32)
    account = Account.from_key(private_key)
    return private_key, account.address
