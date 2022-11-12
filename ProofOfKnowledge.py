# Proof of Knowledge Contract
#
# Anyone can use this contract to record on the tezos blockchain that they
# knew of the existence of some document or hashable object at one time.
#
# This could have uses to support claims such as authorship, copyright,
# or innovation (for patents).
#
# To use the contract use the claim() entry_point and supply
#
#     hash:                 A cryptographic signature of a hashable data object such as a file
#     claim_origination:    Set to True if you claim to be the originator of the object,
#                           Set to False if you only wish to confirm you knew of its existence.
#     claim_copyright:      Set to True if you claim to be the originator of the object, False otherwise
#     claim_innovation:     Set to True if you claim to be the innovator of (some of) the ideas contained in the object, False otherwise
#     claim_message:        An optional message that adds further details to your claim.
#     claimed_on_behalf_of: An optional donor that you act as attorney for when making the claim.
#
# The object itself is not stored in the contract.

import smartpy as sp

class ProofOfKnowledge(sp.Contract):

    @staticmethod
    def get_claim_key(claimant,hash):
        return sp.record(
                claimant=claimant,
                hash=hash
            )

    @staticmethod
    def get_claim_data(claim_origination=sp.bool(False), claim_copyright=sp.bool(False), claim_innovation=sp.bool(False), claim_message=sp.none, claimed_on_behalf_of=sp.none):
        return sp.record(
                claim_origination=claim_origination,
                claim_copyright=claim_copyright,
                claim_innovation=claim_innovation,
                claim_message=claim_message,
                claimed_on_behalf_of=claimed_on_behalf_of,
            )

    CLAIM_KEY = sp.TRecord(
            claimant=sp.TAddress,
            hash=sp.TString
        ).layout(
            ("claimant", "hash")
        )

    CLAIM_DATA = sp.TRecord(
            claim_origination=sp.TBool,
            claim_copyright=sp.TBool,
            claim_innovation=sp.TBool,
            claim_message=sp.TOption(sp.TString),
            claimed_on_behalf_of=sp.TOption(sp.TString),
        ).layout(
            ("claim_origination", ("claim_copyright", ("claim_innovation", ("claim_message","claimed_on_behalf_of"))))
        )

    def __init__(self):
        """Initializes the contract.
        Parameters
        ----------
        proofs: sp.TBigMap(ProofOfKnowledge.CLAIM_HASH, ProofOfKnowledge.CLAIM_DATA)
        """
        # Define the contract storage data types for clarity
        self.init_type(sp.TRecord(
            metadata=sp.TMap(sp.TString, sp.TString),
            proofs=sp.TBigMap(ProofOfKnowledge.CLAIM_KEY, ProofOfKnowledge.CLAIM_DATA),
            )
        )
        metadata = {
            "name": "Proof of Knowledge",
            "description": "Prove you knew of a file or hashable object. Optionally claim origination, copyright, etc.",
        }
        # Initialize the contract storage
        self.init( metadata=metadata, proofs=sp.big_map() )

    @sp.entry_point
    def claim(self, params):
        # Make or update a claim
        sp.set_type(params, sp.TRecord(
            hash=sp.TString,
            claim_origination=sp.TBool,
            claim_copyright=sp.TBool,
            claim_innovation=sp.TBool,
            claim_message=sp.TOption(sp.TString),
            claimed_on_behalf_of=sp.TOption(sp.TString),
            ).layout(
                ("hash", ("claim_origination", ("claim_copyright", ("claim_innovation", ("claim_message","claimed_on_behalf_of")))))
            )
        )
        sp.verify(sp.amount==sp.mutez(0), message="NONZERO_AMOUNT")
        claim_id = self.get_claim_key(sp.source, params.hash)
        claim_msg = self.get_claim_data(
            claim_origination=params.claim_origination,
            claim_copyright=params.claim_copyright,
            claim_innovation=params.claim_innovation,
            claim_message=params.claim_message,
            claimed_on_behalf_of=params.claimed_on_behalf_of
            )
        self.data.proofs[claim_id] = claim_msg

    @sp.entry_point
    def withdraw_claim(self, hash):
        # Delete claim (transaction remains on blockchain)
        sp.set_type(hash, sp.TString)
        sp.verify(sp.amount==sp.mutez(0), message="NONZERO_AMOUNT")
        claim_id = self.get_claim_key(sp.source, hash)
        del self.data.proofs[claim_id]

if "templates" not in __name__:
    @sp.add_test(name = "ProofOfKnowledgeScenario")
    def test():
        some_guy = sp.test_account("some_guy")
        c1 = ProofOfKnowledge()
        scenario = sp.test_scenario()
        scenario.h1("POK")
        scenario += c1
        c1.claim(sp.record(
            hash="3dc1115d86910942af0d1b0bee7183e45a9f2b777f503f895546254ffdcb5017", claim_message=sp.none, claimed_on_behalf_of=sp.none,
            claim_origination=sp.bool(True), claim_copyright=sp.bool(True), claim_innovation=sp.bool(True)
            )).run(valid=True, sender=some_guy)
        c1.claim(sp.record(
            hash="abc2", claim_message=sp.some("msg"), claimed_on_behalf_of=sp.none,
            claim_origination=sp.bool(False), claim_copyright=sp.bool(True), claim_innovation=sp.bool(True)
            )).run(sender=some_guy, amount=sp.mutez(10),valid=False)
        c1.claim(sp.record(
            hash="abc2", claim_message=sp.some("msg"), claimed_on_behalf_of=sp.none,
            claim_origination=sp.bool(False), claim_copyright=sp.bool(True), claim_innovation=sp.bool(True)
            )).run(sender=some_guy, amount=sp.mutez(0),valid=True)
        c1.claim(sp.record(
            hash="abc2", claim_message=sp.some("msg"), claimed_on_behalf_of=sp.some("Yo"),
            claim_origination=sp.bool(False), claim_copyright=sp.bool(True), claim_innovation=sp.bool(True)
            )).run(valid=True, sender=some_guy)
        c1.withdraw_claim("notexisting").run(valid=True, sender=some_guy)
        c1.withdraw_claim("abc2").run(valid=True, sender=some_guy)

    sp.add_compilation_target("Proof Of Knowledge", ProofOfKnowledge())
