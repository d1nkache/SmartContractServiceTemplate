import typing

from pytoniq import Cell, begin_cell

from src.model.schemas import SendBocSchema, StateInit, AbstractMessage


async def as_state_init(code: Cell, data: Cell) -> typing.Union[AbstractMessage, StateInit]:

    state_init = StateInit(
        code = code,
        data = data
    )

    if state_init.validate(): return state_init
    
    return AbstractMessage(
        message = "Error: Not valide data",
        exit_code = -1
    )


async def as_state_init_message(state_init_object: StateInit) -> Cell:
    
    settings = bytes(''.join(['1' if i else '0' for i in [False, False, True, True, False]]), 'utf-8')

    return (
        begin_cell()
            .store_bytes(settings)
            .store_ref(state_init_object.code)
            .store_ref(state_init_object.data)
        .end_cell()
    )


async def from_boc_to_cell(boc: str) -> Cell:

    return Cell.one_from_boc(boc)


async def as_init_data(number: int) -> Cell:

    return (
        begin_cell()
            .store_uint(number, 32)
        .end_cell()
    )


def as_boc_request(send_boc: SendBocSchema) -> dict:


    return {
        "boc": send_boc.boc,
        "batch": send_boc.batch,
        "meta": {}
    }
      