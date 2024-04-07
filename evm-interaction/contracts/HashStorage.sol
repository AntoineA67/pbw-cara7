// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

contract HashStorage {
    address private _owner;
    string[] hashList;

    modifier onlyOwner() {
        require(msg.sender == _owner, "Only owner can call this function.");
        _;
    }

    constructor() {
        _owner = msg.sender;
    }

    function pushHash(string memory _hash) public {
        hashList.push(_hash);
    }

    function getHashList() public view returns (string[] memory) {
        return hashList;
    }
}
