from src.model.schemas import StateInit

from pytoniq import Address
from pytoniq import StateInit as PytoniqStateInit


async def get_smart_contract_address(state_init: StateInit) -> Address: 

    hash_part: bytes = PytoniqStateInit(
        code = state_init.code,
        data = state_init.data
    ).serialize().hash

    print(f"[GETTERS] - [Smart Contract Address]: {str(0) + ':' + hash_part.hex()}")
    return Address(str(0) + ":" + hash_part.hex())
    
    
