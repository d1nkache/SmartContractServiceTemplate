## Counter

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
