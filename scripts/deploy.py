from brownie import SupplyChain, accounts
from scripts.helpful_scripts import get_account


def deploy_supply_chain():
    account = get_account()
    supply_chain = SupplyChain.deploy({"from": account})
    print(f"Supply Chain deployed to {supply_chain.address}")
    return supply_chain


def main():
    deploy_supply_chain()