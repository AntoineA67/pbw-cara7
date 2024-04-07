const contractJson = require('../build/contracts/HashStorage.json');

module.exports = async function (callback) {
    try {
        if (process.argv.length < 6) {
            console.error("Usage: truffle exec ./getHashList.js <smart_contract_address>");
            return callback();
        }
        const contractAddress = process.argv[6];
        const contractABI = contractJson.abi;
        const hashStorage = new web3.eth.Contract(contractABI, contractAddress);
        const getHashListResult = await hashStorage.methods.getHashList().call();

        console.log(`Hash list: ${getHashListResult}`);

    } catch (error) {
        console.error(error);
    }

    callback();
}