import pytest
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_supply_chain
from scripts.add_buy_ship_receive import addItem, buyItem, shipItem
from brownie import network, accounts, exceptions
import time
from web3 import Web3
 
items_dict = {
   "Mac": 3 * 10 ** 18,
   "Dell": 2 * 10 ** 18,
}
 
item = "Mac"
sku = 0
 
 
def test_addItem():
   account = get_account()
   supply_chain = deploy_supply_chain()
   for i, (k, v) in enumerate(items_dict.items()):
       tx = supply_chain.addItem(k, v, {"from": account})
       tx.wait(1)
       assert supply_chain.items(i)[0] == k
       assert supply_chain.items(i)[1] == i
       assert supply_chain.items(i)[2] == v
       assert supply_chain.items(i)[3] == 0
       assert supply_chain.items(i)[4] == account
       assert supply_chain.items(i)[5] == "0x0000000000000000000000000000000000000000"
 
 
def test_buyItem():
   account = accounts[1]
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   tx = supply_chain.buyItem(
       sku,
       {
           "from": account,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 10 * 10 ** 18,
       },
   )
   tx.wait(1)
   time.sleep(5)
   assert supply_chain.items(sku)[3] == 1
   assert supply_chain.items(sku)[5] == account
 
 
def test_buyItem_paid_enough():
   account = accounts[1]
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   with pytest.raises(exceptions.VirtualMachineError):
       tx = supply_chain.buyItem(
           sku,
           {
               "from": account,
               "gas_limit": 100000,
               "allow_revert": True,
               "value": 1 * 10 ** 18,
           },
       )
 
 
def test_buyItem_checkValue():
   account = accounts[1]
   old_balance = Web3.fromWei(account.balance(), "ether")
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   tx = supply_chain.buyItem(
       sku,
       {
           "from": account,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 10 * 10 ** 18,
       },
   )
   tx.wait(1)
   time.sleep(5)
   new_balance = Web3.fromWei(account.balance(), "ether")
   assert (new_balance - old_balance) == supply_chain.items(sku)[1]
 
 
def test_shipItem():
   account = get_account()
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   tx = supply_chain.buyItem(
       sku,
       {
           "from": account,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 10 * 10 ** 18,
       },
   )
   tx.wait(1)
   supply_chain.shipItem(sku, {"from": account})
   time.sleep(5)
   assert supply_chain.items(sku)[3] == 2
 
 
def test_shipItem_checkSeller():
   account = get_account()
   buyer = accounts[1]
   non_seller_account = accounts[2]
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   tx = supply_chain.buyItem(
       sku,
       {
           "from": buyer,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 10 * 10 ** 18,
       },
   )
   tx.wait(1)
   with pytest.raises(exceptions.VirtualMachineError):
       supply_chain.shipItem(sku, {"from": buyer})
       supply_chain.shipItem(sku, {"from": non_seller_account})
 
 
def test_receiveItem():
   account = get_account()
   supply_chain = deploy_supply_chain()
   supply_chain.addItem(item, items_dict[item], {"from": account})
   tx = supply_chain.buyItem(
       sku,
       {
           "from": account,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 10 * 10 ** 18,
       },
   )
   tx.wait(1)
   supply_chain.shipItem(sku, {"from": account})
   supply_chain.receiveItem(sku, {"from": account})
   assert supply_chain.items(sku)[3] == 3