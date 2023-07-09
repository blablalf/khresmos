// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Oracle {
    struct Staker {
        uint256 amountStaked;
        uint256 lastTimestamp;
        bool slashed;
    }

    struct AssetData {
        uint256 price;
        uint256 timestamp;
        uint256 ponderation;
    }

    address public owner;
    mapping(address => Staker) public stakers;
    mapping(address => AssetData) public assetData;
    uint256 public minStake;

    event Staked(address indexed staker, uint256 amount);
    event Slashed(address indexed staker, uint256 amount);
    event AssetDataUpdated(address indexed asset, uint256 price, uint256 timestamp);

    constructor(uint256 _minStake) {
        owner = msg.sender;
        minStake = _minStake;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    function stake(uint256 amount) external payable {
        require(amount > 0, "Amount must be greater than zero");

        Staker storage staker = stakers[msg.sender];
        staker.amountStaked += amount;

        emit Staked(msg.sender, amount);
    }

    function slash(address stakerAddress, uint256 amount) external onlyOwner {
        require(stakerAddress != address(0), "Invalid staker address");
        require(amount > 0, "Amount must be greater than zero");

        Staker storage staker = stakers[stakerAddress];
        require(staker.amountStaked >= amount, "Insufficient staked amount");

        staker.amountStaked -= amount;
        staker.slashed = true;

        emit Slashed(stakerAddress, amount);
    }

    function isSlashed(address stakerAddress) external view returns (bool) {
        return stakers[stakerAddress].slashed;
    }

    function updateAssetData(address asset, uint256 price) external {
        Staker storage staker = stakers[msg.sender];
        require(staker.amountStaked >= minStake, "Insufficient staked amount");
        require(!staker.slashed, "Staker has already been slashed");
        AssetData storage data = assetData[asset];
        require(data.timestamp != staker.lastTimestamp, "User has already participated");

        // init if it is not
        if (data.ponderation == 0) data.ponderation = 1;

        // If it's a new feed, then ponderate
        if (data.timestamp == block.timestamp) {
            data.price = (data.price * data.ponderation + price) / (data.ponderation + 1);
            data.ponderation++;
        } else {
            data.timestamp = block.timestamp;
            data.price = price;
            data.ponderation = 1;
        }

        emit AssetDataUpdated(asset, price, block.timestamp);
    }
}
