import asyncio

from src.сore.contract import Contract
from src.model.schemas import StateInit
from src.model.config import CODE_BOC_FORMAT
from src.model.mappers import as_init_data, from_boc_to_cell


async def main():

    state_init = StateInit(
        code = from_boc_to_cell(CODE_BOC_FORMAT),
        data = await as_init_data(number = 0)
    )

    contract = await Contract.create(state_init)
    result = await contract.deploy_smart_contract_via_client()

    print(result.message)
     
    
asyncio.run(main())