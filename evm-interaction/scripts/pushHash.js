const contractJson = require('../build/contracts/HashStorage.json');

module.exports = async function (callback) {
    try {
        if (process.argv.length < 7) {
            console.error("Usage: truffle exec ./pushHash.js <smart_contract_address> <hash>");
            return callback();
        }
        const contractAddress = process.argv[6];
        const hash = process.argv[7];
        const contractABI = contractJson.abi;

        const hashStorage = new web3.eth.Contract(contractABI, contractAddress);
        const accounts = await web3.eth.getAccounts();

        const pushHashResult = await hashStorage.methods.pushHash(hash).send({ from: accounts[0] });
        console.log(`pushHash transaction hash: ${pushHashResult.transactionHash}`);

    } catch (error) {
        console.error(error);
    }

    callback();
}