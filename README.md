# Proof of Knowledge Smart Contract for Tezos

Written and tested with [SmartPy](https://smartpy.io/ide). 

Anyone can use this contract to record on the tezos blockchain that they knew of the existence of some document or hashable object at one time.

Recording knowledge of documents  could have uses to support claims such as authorship, copyright, or innovation (for patents).

The hashable object itself is not stored in the contract. 

# Usage : 

There is currently no dedicated website for this contract. You can however use it by inputting parameters at better call dev. Links below. 

To use the contract use the claim() entry_point and supply
|Parameter|Type|Description|
|---|---|---|
|hash                 |string|A cryptographic signature of a hashable data object such as a file|
|claim_origination    |boolean|Set to True if you claim to be the originator of the object,<br>Set to False if you only wish to confirm you knew of its existence.|
|claim_copyright      |boolean|Set to True if you claim to be the originator of the object, False otherwise|
|claim_innovation     |boolean|Set to True if you claim to be the innovator of (some of) the ideas contained in the object, False otherwise|
|claim_message        |optional string|An optional message that adds further details to your claim.|
|claimed_on_behalf_of |optional string|An optional donor that you act as attorney for when making the claim.|

## Published on-chain 

Proof of Knowledge Contract ID `KT1C52fE3yCmhCrr9oQEXG1Hh7WfsCGeA1gW` on 2022-11-12.

View or interact with the contract :
 - [[view on better-call.dev]](https://better-call.dev/mainnet/KT1C52fE3yCmhCrr9oQEXG1Hh7WfsCGeA1gW) [[interact]](https://better-call.dev/mainnet/KT1C52fE3yCmhCrr9oQEXG1Hh7WfsCGeA1gW/interact/claim)
 - [[view on tzkt.io]](https://tzkt.io/KT1C52fE3yCmhCrr9oQEXG1Hh7WfsCGeA1gW)
 
