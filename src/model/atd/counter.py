import base64

from model.atd.wallet import AdminWallet
from model.schemas import AbstractMessage, SendBocSchema
from model.mappers import as_init_data
from model.mappers import StateInit

from utils.getters import get_smart_contract_address

from pytoniq import LiteClient, WalletV4R2
from pytoniq import StateInit as PytoniqStateInit

class Counter:

    def __init__(self, state_init: StateInit): 

        self.address = get_smart_contract_address(state_init)
        self.state_init = state_init


    async def send_number(self, number: int) -> AbstractMessage:

        wallet = AdminWallet()

        result = await wallet.send_internal_message_via_client(
            destination = self.address,
            amount = int(0.01 * 10 ** 9),
            body = await as_init_data(number = number)  # плохо
        )

        return result
    

    async def deploy_smart_contract_via_client(self, start_number: int) -> AbstractMessage:

        wallet = AdminWallet()

        result = await wallet.send_internal_message_via_client(
            destination = self.address,
            amount = int(0.01 * 10 ** 9),
            state_init = StateInit(
                code = self.state_init.code,
                data = await as_init_data(number = start_number) # плохо
            )
        )

        return result
    

    async def deploy_smart_contract_via_tonapi(self, start_number: int) -> AbstractMessage:

        wallet = AdminWallet()

        boc =  WalletV4R2.create_external_msg(
            dest = wallet.address,
            body = WalletV4R2.create_internal_msg(
                dest = self.address,
                ihr_fee = int(0.02 * 10 ** 9),
                state_init = PytoniqStateInit(
                    data = self.state_init.data,
                    code = self.state_init.code
                )
            ).serialize()
        ).serialize().to_boc()
        
        boc_base64 = base64.b64encode(boc).decode('utf-8')
        
        result: AbstractMessage = await wallet.send_external_message_via_ton_api(
            message = SendBocSchema(boc = boc_base64)
        )

        return result
    

    async def get_number(self) -> int:

        wallet = AdminWallet()

        if wallet.provider_config is None:

            async with LiteClient.from_mainnet_config(trust_level = 2) as provider:

                pytoniq_wallet = await AdminWallet().as_wallet_v4r2(provider = provider)
                result = await pytoniq_wallet.run_get_method(
                    method = "get_total",
                    stack = []
                )
                
                return result
            
        async with LiteClient.from_mainnet_config(trust_level = wallet.provider_config) as provider:
            
            pytoniq_wallet = await AdminWallet().as_wallet_v4r2(provider = provider)
            result = await wallet.run_get_method(
                method = "get_total",
                stack = []
            )
            
            return result