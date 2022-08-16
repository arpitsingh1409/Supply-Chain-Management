from brownie import (
    network,
    config,
    accounts,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMT = ["mainnet-fork", "mainnet-fork-dev", "rinkeby"]


def get_account(index=None, id=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[5]
    else:
        return accounts.add(config["wallets"]["from_key"])