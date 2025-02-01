import typing
import aiohttp

from src.model.mappers import as_boc_request
from src.model.config import AdminWalletConfig, TonApiConfig
from src.model.schemas import SendBocSchema, AbstractMessage, StateInit

from pytoniq import WalletV4R2, Cell, LiteClient, SimpleAccount, LiteBalancer


class AdminWallet:

    def __init__(self, address: str, mnemonic: str, provider_config = None):

        self.address = address
        self.mnemonic = mnemonic

        if provider_config is None:
            self.provider_config = None                # переделать логику - лень


    def __init__(self, provider_config: str):

        self.address = AdminWalletConfig.ADDRESS
        self.mnemonic = AdminWalletConfig.MNEMONIC
        self.provider_config = provider_config

    
    def __init__(self):

        self.address = AdminWalletConfig.ADDRESS
        self.mnemonic = AdminWalletConfig.MNEMONIC
        self.provider_config = None   
    

    async def as_wallet_v4r2(self, provider: typing.Union[LiteClient, LiteBalancer]) -> WalletV4R2: 
        
        if self.provider_config is None:
            return await WalletV4R2.from_mnemonic(provider = provider, mnemonics = self.mnemonic)

        return await WalletV4R2.from_mnemonic(provider = provider, mnemonics = self.mnemonic)
        

    async def get_wallet_seqno_via_client(self) -> typing.Union[int, AbstractMessage]:

        try:
            wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2()

            return await wallet_v4r2.get_seqno()
        
        except:
            return AbstractMessage(
                message = "Error: something went wrong",
                exit_code = -1
            )
    

    async def get_wallet_balance_via_client(self) -> typing.Union[int, AbstractMessage]:

        try:
            wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2()

            return await wallet_v4r2.get_balance()
        
        except:
            return AbstractMessage(
                message = "Error: something went wrong",
                exit_code = -1
            )
    

    async def get_wallet_public_key_via_client(self) -> typing.Union[int, AbstractMessage]:

        try:
            wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2()

            return await wallet_v4r2.get_public_key()
        
        except:
            return AbstractMessage(
                message = "Error: something went wrong",
                exit_code = -1
            )
    

    async def get_wallet_public_key_via_client(self) -> typing.Union[SimpleAccount, AbstractMessage]:

        try:
            wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2()

            return await wallet_v4r2.get_account_state()
        
        except:
            return AbstractMessage(
                message = "Error: something went wrong",
                exit_code = -1
            )
        

    async def get_wallet_seqno_via_client(self) -> typing.Union[int, AbstractMessage]:

        try:
            wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2()

            return await wallet_v4r2.get_seqno()
        
        except:
            return AbstractMessage(
                message = "Error: something went wrong",
                exit_code = -1
            )


    async def get_wallet_seqno_via_tonapi(self) -> typing.Union[int, AbstractMessage]:

        url = f"{TonApiConfig.BASE_URL}/v2/wallet/{self.address}/seqno "
        timeout = aiohttp.ClientTimeout(total = 30)
        headers = {'Content-Type': 'application/json'}

        try:

            async with aiohttp.ClientSession(timeout = timeout) as session:
                async with session.get(url = url) as response:

                    response.raise_for_status()
                    data = await response.json()
                    seqno = data.get("seqno")

                    if seqno is None:

                        return AbstractMessage(
                            message = "Error: seqno is None",
                            exit_code = -1
                        )
                    
                    return  seqno
                
        except aiohttp.ClientResponseError as e:
            return AbstractMessage(
                message = f"Error: status - {e.status} - {e.message}",
                exit_code = -1
            )
        except aiohttp.ClientConnectionError:
            return AbstractMessage(
                message = f"Error: connection error",
                exit_code = -1
            )
        except Exception as e:
            return AbstractMessage(
                message = f"Error: something went wrong",
                exit_code = -1
            )


    async def send_internal_message_via_client(
            self,
            destination: str,
            amount: int,
            body: Cell = Cell.empty(),
            state_init: StateInit = None
        ) -> AbstractMessage:
    
        if self.provider_config is None:

            print("я тут")

            try:
                async with LiteClient.from_mainnet_config(trust_level = 2) as provider:
                    
                    wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2(provider = provider)
                    
                    await wallet_v4r2.transfer(
                        destination = destination,
                        amount = amount,
                        body = body,
                        state_init = state_init
                    )

                    return AbstractMessage(
                        message = "Success: External message was sent",
                        exit_code = 0
                    )
                
            except(Exception) as ex:
                return AbstractMessage(
                    message = f"Error: External message was not sent - {ex}",
                    exit_code = -1
                )

        async with LiteClient.from_config(self.provider_config) as provider:
            try:
                wallet_v4r2: WalletV4R2 = await self.as_wallet_v4r2(provider = provider)
                await wallet_v4r2.transfer(
                    destination = destination,
                    amount = amount,
                    body = body,
                    state_init = state_init
                )

                return AbstractMessage(
                    message = "Success: External message was sent",
                    exit_code = 0
                )
            
            except(Exception) as ex:
                return AbstractMessage(
                    message = f"Error: External message was not sent - {ex}",
                    exit_code = -1
                )


    async def send_external_message_via_ton_api(self, message: SendBocSchema) -> AbstractMessage:
        
        url = f"{TonApiConfig.BASE_URL}/v2/blockchain/message"
        timeout = aiohttp.ClientTimeout(total = 30)
        headers = {'Content-Type': 'application/json'}

        try:
            async with aiohttp.ClientSession(timeout = timeout) as session:                
                async with session.post(url = url, json = as_boc_request(message), headers = headers) as response:
                        
                    response.raise_for_status()
                    
                    return AbstractMessage(
                        message = "Success: External message was sent",
                        exit_code = 0
                    )
                
        except aiohttp.ClientResponseError as e:
            return AbstractMessage(
                message = f"Error: status - {e.status} - {e.message}",
                exit_code = -1
            )
        except aiohttp.ClientConnectionError:
            return AbstractMessage(
                message = f"Error: connection error",
                exit_code = -1
            )
        except Exception as e:
            return AbstractMessage(
                message = f"Error: something went wrong - {e}",
                exit_code = -1
            )