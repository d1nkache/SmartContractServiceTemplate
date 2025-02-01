import asyncio

from src.model.atd.counter import Counter
from src.model.schemas import StateInit
from src.model.config import CODE_BOC_FORMAT
from src.model.mappers import as_init_data, from_boc_to_cell


async def main():

    state_init = StateInit(
        code = from_boc_to_cell(CODE_BOC_FORMAT),
        data = await as_init_data(number = 0)
    )

    result = await Counter(state_init = state_init).deploy_smart_contract_via_client(
        start_number = 0
    )

    print(result.message)
     
    
asyncio.run(main())