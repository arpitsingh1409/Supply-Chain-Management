from brownie import SupplyChain, accounts
from scripts.deploy import deploy_supply_chain
from scripts.helpful_scripts import get_account
from web3 import Web3
import time
 
items_dict = {
   "Mac": 3 * 10 ** 18,
   "Dell": 2 * 10 ** 18,
   # "HP": 10 * 10 ** 18,
   # "Lenovo": 10 * 10 ** 18,
}
# items_dict = {"Mac": 1000}
sku = 1
 
 
def addItem():
   print("Adding Item")
   account = get_account()
   supply_chain = SupplyChain[-1]
   # supply_chain = SupplyChain.deploy({"from": account})
   print(f"Owner of Contract is {supply_chain.owner()}")
   print(
       f"Seller Account Before Transaction {Web3.fromWei(account.balance(), 'ether')}"
   )
 
   for i, (k, v) in enumerate(items_dict.items()):
       tx = supply_chain.addItem(k, v, {"from": account})
       tx.wait(1)
       print(supply_chain.skuCount())
       get_item_details(i)
       # items = supply_chain.items(i)
       # print(
       #     f"Name : {items[0]}, Sku : {items[1]}, Price : {items[2]}, State : {items[3]}, Seller : {items[4]}, Buyer : {items[5]}"
       # )
 
 
def buyItem():
   print("Buying Item")
   account = accounts[1]
   supply_chain = SupplyChain[-1]
   # print(Web3.fromWei(supply_chain.getBalance(), "ether"))
   # supply_chain = SupplyChain.deploy({"from": account})
   # items = supply_chain.items(sku)
   # print(
   #     f"Name : {items[0]}, Sku : {items[1]}, Price : {Web3.fromWei(items[2], 'ether')}, State : {items[3]}, Seller : {items[4]}, Buyer : {items[5]}"
   # )
   # print(f"Price: {Web3.fromWei(supply_chain.items(sku)[2], 'ether')}")
   print(f"Account Balance: {Web3.fromWei(account.balance(), 'ether')}")
   tx = supply_chain.buyItem(
       sku,
       {
           "from": account,
           "gas_limit": 100000,
           "allow_revert": True,
           "value": 5 * 10 ** 18,
       },
   )
   tx.wait(1)
   time.sleep(5)
   print(
       f"Account Balance After Transaction: {Web3.fromWei(account.balance(), 'ether')}"
   )
 
 
def shipItem():
   print("Shipping Item")
   account = get_account()
   supply_chain = SupplyChain[-1]
   supply_chain.shipItem(sku, {"from": account})
   print("Item Shipped")
 
 
def receiveItem():
   print("Check Receive Item")
   account = accounts[1]
   print(
       f"Seller Account After Transaction {Web3.fromWei(account.balance(), 'ether')}"
   )
   supply_chain = SupplyChain[-1]
   supply_chain.receiveItem(sku, {"from": account})
   print("Item Received")
 
 
def get_item_details(sku):
   print("Getting Item details")
   account = get_account()
   supply_chain = SupplyChain[-1]
   items = supply_chain.items(sku)
   print(
       f"Name : {items[0]}, Sku : {items[1]}, Price : {Web3.fromWei(items[2], 'ether')}, State : {items[3]}, Seller : {items[4]}, Buyer : {items[5]}"
   )
   print("\n")
 
 
def main():
   bf = get_account().balance()
   get_item_details(sku)
   addItem()
   get_item_details(sku)
   buyItem()
   time.sleep(5)
   get_item_details(sku)
   shipItem()
   time.sleep(5)
   get_item_details(sku)
   receiveItem()
   time.sleep(5)
   get_item_details(sku)
   af = get_account().balance()
   print(f"Income {Web3.fromWei(af-bf, 'ether')}")