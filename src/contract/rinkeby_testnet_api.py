from json import load as json_load
from pathlib import Path

from web3 import Web3, HTTPProvider
from web3.exceptions import InvalidAddress, ABIFunctionNotFound, ValidationError
from web3.middleware import geth_poa_middleware

ABI_PATH = Path(__file__).parent / "abi.json"

def connect_to_node(config: dict) -> dict:
    """Подключение к узлу сети Ethereum."""
    message = "ok"
    provider_url = config.get("provider_url", None)
    if provider_url is None:
        message = "Provider url is not specified."
        connection = None
        return {"message": message, "connection": connection}
    connection = Web3(HTTPProvider(f"{provider_url}"))
    connection.middleware_onion.inject(geth_poa_middleware, layer=0)
    if not connection.isConnected():
        message = "Can not establish node connection with given provider url."
        connection = None
    return {"message": message, "connection": connection}

def connect_to_contract(config: dict, w3: Web3) -> dict:
    """Подключение к смарт контракту."""
    message = "ok"
    address = config.get("contract_address", None)
    with open(ABI_PATH) as f:
        abi = json_load(f)
    if any([address is None, abi is None]):
        message = "Can not establish contract connection with given abi/address"
    try:
        contract = w3.eth.contract(address=address, abi=abi)
    except InvalidAddress as err:
        message = str(err)
        contract = None
    return {"message": message, "contract": contract}

def contract_mint(
    connection: Web3,
    contract, 
    owner: str,
    unique_hash: str,
    media_url: str,
    config: dict
    ):
    """API к методу mint смарт контракта."""
    message = "ok"
    tx_hash = None
    private_key = config.get("private_key", None)
    if private_key is None:
        message = "Private key must be specified."
    try:
        nonce = connection.eth.getTransactionCount(owner)
        txn = contract.functions.mint(owner, unique_hash, media_url).buildTransaction({
            "from": owner,
            "nonce": nonce
        })
        signed = connection.eth.account.sign_transaction(txn, private_key)
        tx_hash = Web3.toHex(Web3.keccak(
            connection.eth.send_raw_transaction(signed.rawTransaction)
        ))
    except ABIFunctionNotFound as err:
        message = str(err)
    except ValidationError as err:
        message = str(err)
    except InvalidAddress as err:
        message = str(err)
    return {"message": message, "tx_hash": tx_hash}


def contract_total_supply(contract):
    """API к методу totalSupply смарт контракта."""
    message = "ok"
    try:
        total_supply = contract.functions.totalSupply().call()
    except Exception as err:
        message = str(err)
    return {"message": message, "total_supply": total_supply}
