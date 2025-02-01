import typing

from pytoniq import Cell


class AbstractMessage():

    def __init__(self, message: str, exit_code: int):

        self.message = message
        self.exit_code = exit_code


class SendBocSchema:

    def __init__(self, boc: str, batch: typing.List[str] = []):

        self.boc = boc
        self.batch = batch


class StateInit:

    def __init__(self, code: Cell, data: Cell):
        
        if self.validate([code, data]):

            self.code = code
            self.data = data

        else:
            raise ValueError("Invalid StateInit object")


    def validate(self, vars: typing.List) -> bool:

        for elem in vars:
            if isinstance(elem, Cell): 
                return True

            return False

    
    