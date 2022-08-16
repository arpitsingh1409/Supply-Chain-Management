# Supply Chain Management using Blockchain Technology

## A proof of concept for my project at BITS Pilani

This is a smart contract built on the Ethereum Blockchain for basic supply chain management and servers as a proof of concept. This is can be extended to be implemneted on a custom blockchain (for example using Hyperledger) or the smart contract can be further enriched with custom features (for example adding a frontend), as Ethereum is moving to PoS system and gas fees are going to be reduced drastically!

## Features

- Adds an item with the provided name and price
- Emits a LogForSale event when an item is added
- Allow someone to purchase an item and update state accordingly
- Throws an error when not enough value is sent when purchasing an item
- Emits LogSold event when and item is purchased
- Reverts when someone that is not the seller tries to call shipItem()
- Allows the seller to mark the item as shipped
- Emits a LogShipped event when an item is shipped
- Allows the buyer to mark the item as received
- Reverts if an address other than the buyer calls receiveItem()
- Emits a LogReceived event when an item is received

## Installation

It is a smart contract written in Solidity and requires a Solidity Compiler (>= 0.8.0) (https://docs.soliditylang.org/en/v0.8.9/installing-solidity).

For running **scripts** and **tests** install Web3 and Brownie.

For Web3

```sh
npm install web3
```

Install Python first (if not already insalled)

```sh
sudo apt-get install python3
```

For Brownie (install as global application)

```sh
sudo apt install pipx
pipx install eth-brownie
pipx ensurepath
```

## License

MIT

**Free Software, Hell Yeah!**
