// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GovernmentBlockchain {
    struct GovernmentBlock {
        uint256 index;
        uint256 timestamp;
        string data;
        string location;
        string name;
        bytes32 previousHash;
        bytes32 hash;
    }

    mapping(uint256 => GovernmentBlock) public blocks;
    uint256 public blockCount;

    event BlockAdded(
        uint256 indexed index,
        uint256 timestamp,
        string data,
        string location,
        string name,
        bytes32 previousHash,
        bytes32 hash
    );

    constructor() {
        blockCount = 0;
    }

    function addBlock(string memory _data, string memory _location, string memory _name) public {
        blockCount++;
        bytes32 previousHash = blockCount == 1 ? bytes32(0) : blocks[blockCount - 1].hash;
        bytes32 newHash = calculateHash(blockCount, block.timestamp, _data, _location, _name, previousHash);
        
        GovernmentBlock memory newBlock = GovernmentBlock({
            index: blockCount,
            timestamp: block.timestamp,
            data: _data,
            location: _location,
            name: _name,
            previousHash: previousHash,
            hash: newHash
        });
        
        blocks[blockCount] = newBlock;
        emit BlockAdded(
            newBlock.index,
            newBlock.timestamp,
            newBlock.data,
            newBlock.location,
            newBlock.name,
            newBlock.previousHash,
            newBlock.hash
        );
    }

    function calculateHash(
        uint256 index,
        uint256 timestamp,
        string memory data,
        string memory location,
        string memory name,
        bytes32 previousHash
    ) private pure returns (bytes32) {
        return keccak256(abi.encodePacked(index, timestamp, data, location, name, previousHash));
    }
}
