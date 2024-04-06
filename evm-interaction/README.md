>> After cloning need to execute `npm install`

Need to create `.env` at root of this project and add this :
```
MNEMONIC="your mnemonic"
```

Create new smart contract
`truffle migrate --network xrpl`
>> parse "contract address:" for need smartcontract address

Get all hash of specific smartcontract
`truffle exec --network xrpl ./scripts/getHashList.js <smart_contract_address>`

Push hash on specific smartcontract
`truffle exec ./pushHash.js <smart_contract_address> <hash>`