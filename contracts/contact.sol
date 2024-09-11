// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract contact {

  address owner;

    string[] _names;
    string[] _mobiles;
    string[] _emails;
    string[] _organizations;

    mapping (string => bool) _contacts;
  constructor() public {
     owner=msg.sender;
    
  }
  modifier onlyOwner {
    require(owner==msg.sender);
    _;
  }
 function insertContact(string memory name, string memory mobile, string memory email, string memory org) public {
    require(!_contacts[mobile], "This contact already exists");
    _names.push(name);
    _mobiles.push(mobile);
    _emails.push(email);
    _organizations.push(org);
    _contacts[mobile] = true;
}

  //read contact from blockchain
  function viewContacts() onlyOwner public view returns(string[] memory,string[] memory,string[] memory,string[] memory){
      return(_names,_mobiles,_emails,_organizations);
  }
}
