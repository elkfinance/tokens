pragma solidity ^0.5.0;

contract MultiSender {
    // The address payable that will receive the fee
    address payable public feeReceiver;

    // The amount of the fee
    uint256 public feeAmount;

    uint256 owner;

    // The constructor sets the fee receiver and amount
    constructor(address payable _feeReceiver, uint256 _feeAmount, uint256 _owner) public {
        feeReceiver = _feeReceiver;
        feeAmount = _feeAmount;
        owner = _owner;
    }

    // The function that allows the fee receiver and amount to be changed
    function setFee(address payable _feeReceiver, uint256 _feeAmount) public onlyOwner {
        feeReceiver = _feeReceiver;
        feeAmount = _feeAmount;
    }

    // The function that sends a single amount of any token to multiple addresses
    function sendSingle(address[] memory _recipients, uint256 _amount) public {
        require(_recipients.length > 0, "No recipients specified");

        // Send the fee to the fee receiver
        feeReceiver.transfer(feeAmount);

        // Send the specified amount to each recipient
        for (uint256 i = 0; i < _recipients.length; i++) {
            _recipients[i].transfer(_amount);
        }
    }

    // The function that sends multiple amounts of any token to multiple addresses
    function sendMultiple(address[] memory _recipients, uint256[] memory _amounts) public {
        require(_recipients.length == _amounts.length, "Number of recipients and amounts must match");
        require(_recipients.length > 0, "No recipients specified");

        // Send the fee to the fee receiver
        feeReceiver.transfer(feeAmount);

        // Send the specified amount to each recipient
        for (uint256 i = 0; i < _recipients.length; i++) {
            _recipients[i].transfer(_amounts[i]);
        }
    }

    // The modifier that allows only the contract owner to call a function
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function");
        _;
    }
}
