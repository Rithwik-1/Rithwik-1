from hedera import Client, AccountId, PrivateKey, TokenCreateTransaction, TokenType, TokenSupplyType, TokenMintTransaction, TransferTransaction, TokenBalanceQuery

client = Client.for_testnet()
client.set_operator(AccountId.fromString("your-account-id"), PrivateKey.fromString("your-private-key"))

def create_fungible_token():
    tx = TokenCreateTransaction() \
        .set_token_name("MyToken") \
        .set_token_symbol("MTK") \
        .set_decimals(2) \
        .set_initial_supply(1000) \
        .set_treasury_account_id(AccountId.fromString("your-account-id")) \
        .set_token_type(TokenType.FUNGIBLE_COMMON) \
        .set_supply_type(TokenSupplyType.INFINITE) \
        .freeze_with(client)
    tx_sign = tx.sign(PrivateKey.fromString("your-private-key"))
    tx_response = tx_sign.execute(client)
    receipt = tx_response.get_receipt(client)
    token_id = receipt.token_id
    print(f"Token Created: {token_id}")
    return token_id

def mint_tokens(token_id, amount):
    mint_tx = TokenMintTransaction() \
        .set_token_id(token_id) \
        .set_amount(amount) \
        .freeze_with(client)
    mint_sign = mint_tx.sign(PrivateKey.fromString("your-private-key"))
    mint_response = mint_sign.execute(client)
    mint_receipt = mint_response.get_receipt(client)
    print(f"Tokens Minted: {mint_receipt.status}")

def transfer_tokens(token_id, from_account_id, to_account_ids, amount_per_recipient):
    transfers = {from_account_id: -amount_per_recipient}
    for recipient_id in to_account_ids:
        transfers[recipient_id] = amount_per_recipient
    transfer_tx = TransferTransaction() \
        .add_token_transfer(token_id, transfers) \
        .freeze_with(client)
    transfer_sign = transfer_tx.sign(PrivateKey.fromString("your-private-key"))
    transfer_response = transfer_sign.execute(client)
    transfer_receipt = transfer_response.get_receipt(client)
    print(f"Transfer Status: {transfer_receipt.status}")

def get_balance(token_id, account_id):
    balance_query = TokenBalanceQuery() \
        .set_token_id(token_id) \
        .set_account_id(account_id)
    balance = balance_query.execute(client)
    return balance.amount

def main():
    token_id = create_fungible_token()
    mint_tokens(token_id, 500)
    recipient_ids = [
        "recipient-account-id-1",
        "recipient-account-id-2"
    ]
    transfer_tokens(token_id, "your-account-id", recipient_ids, 100)
    treasury_balance = get_balance(token_id, "your-account-id")
    print(f"Treasury Balance: {treasury_balance} MTK")
    for recipient_id in recipient_ids:
        recipient_balance = get_balance(token_id, recipient_id)
        print(f"Recipient ({recipient_id}) Balance: {recipient_balance} MTK")

if __name__ == "__main__":
    main()
