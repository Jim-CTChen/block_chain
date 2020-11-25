# README
## Prerequisites
None

## How To Work
### 1. some helpful tips
``` bash
>> python3 ./pseudoBitcoin.py -h
```
### 2. create a blockchain with address (or reset the old one)
(all coinbase reward will go to the specified address)
``` bash
>> python3 ./pseudoBitcoin.py createblockchain -address {address}
```

### 3. print whole blockchain
```bash
>> python3 ./pseudoBitcoin.py printchain
```

### 4. print spicific block with height
```bash
>> python3 ./pseudoBitcoin.py printblock -h {height}
```

### 5. get balance with address
```bash
>> python3 ./pseudoBitcoin.py getbalance -address {address}
```

### 6. send money from one address to another
```bash
>> python3 ./pseudoBitcoin.py send -from {from_address} -to {to_address} -amount {amount}
```

## Functionalities
1. Block
2. BlockChain
3. POW
4. Database
5. Client
6. UTXO
7. Mining Reward
8. Merkle Tree