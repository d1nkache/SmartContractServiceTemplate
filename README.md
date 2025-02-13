## Counter

# ❗Данный шаблон в данный момент в процессе разработки

### Пример деплоя смарт-контракта через LiteClient от Pytoniq

```
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
```


### Пример деплоя смарт-контракта через tonapi

```
async def main():

    state_init = StateInit(
        code = from_boc_to_cell(CODE_BOC_FORMAT),
        data = await as_init_data(number = 0)
    )

    result = await Counter(state_init = state_init).deploy_smart_contract_via_tonapi(
        start_number = 0
    )

    print(result.message)
     
    
asyncio.run(main())
```

# Адаптация шаблона 

1) ./src/model/config -> Необходимо внести ключ от тонапи(если имеется), а также внести данные Админского кошелька, ссылку на кофиг приватной ноды, и код смарт контракта в формате boc

```
CODE_BOC_FORMAT = "te6ccgEBBAEAOgABFP8A9KQT9LzyyAsBAgFiAgMANtBsMSDXScEg8mPTHzDtRNDTPzABoMjLP8ntVAARoen72omhpn5h"
PROVIDER_CONFIG_URL = ""

class TonApiConfig:
    
    BASE_URL = "https://tonapi.io"
    API_KEY = ""


class AdminWalletConfig:

    ADDRESS = ""
    MNEMONIC = ""
```

2) ./main -> Aдаптация state_init под ваш смарт-контракт, а также назввания СК и тп

```
state_init = StateInit(
        code = from_boc_to_cell(CODE_BOC_FORMAT),
        data = await as_init_data(number = 0)
    )

    result = await Counter(state_init = state_init).deploy_smart_contract_via_tonapi(
        start_number = 0
    )
```

3) ./src/model/atd/counter -> Необходимо изменить название класса на название вашего СК, а также адаптировать следующие методы

```
    async def send_number(self, number: int) -> AbstractMessage:

        wallet = AdminWallet()

        result = await wallet.send_internal_message_via_client(
            destination = self.address,
            amount = int(0.01 * 10 ** 9),
            body = await as_init_data(number = number)  # плохо
        )

        return result
```

```
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
```
