require('dotenv').config();
const HDWalletProvider = require('@truffle/hdwallet-provider');
const infuraProjectId = process.env.INFURA_PROJECT_ID;
const etherscanApi = process.env.ETHERSCAN_API;
const mnemonic = process.env.MNEMONIC;

module.exports = {

  networks: {

    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*",
    },

    xrpl: {
      provider: () => new HDWalletProvider(mnemonic, `https://rpc-evm-sidechain.xrpl.org/`),
      network_id: 1440002,
      gas: 5500000,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    },
  },

  plugins: ['truffle-plugin-verify'],

  mocha: {
  },

  api_keys: {
    etherscan: `${etherscanApi}`,
  },

  compilers: {
    solc: {
      version: "0.8.20",
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        },
        evmVersion: "byzantium"
      }
    }
  },
};
