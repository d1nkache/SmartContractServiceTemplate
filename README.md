# Автоматизация работы со смарт-контрактами TON на Python

---

## 📆 Аннотация
Шаблон, написанный на Python, представляет собой готовое решение для работы со смарт-контрактами в блокчейне TON с использованием библиотеки `pytoniq`. Проект предлагает минимально необходимую, но полноценную среду для разработки смарт-контрактов на языке Func, включая развёртывание, отправку сообщений и утилитарные модули.

---

## 📂 Структура проекта
```
project_root/
├── contracts/     # Исходные коды смарт-контрактов (.fc)
├── core/          # Основные абстракции, такие как Contract и Wallet
├── model/         # Схемы данных и конфигурации
├── service/       # Высокоуровневые сервисные классы
└── utils/         # Вспомогательные утилиты
```

---

## 🔍 Основные классы

### `Contract`
Абстракция над смарт-контрактом в сети TON. Предоставляет методы:
- Развёртывание контракта
- Отправка внутренних сообщений
- Вызов get-методов

#### Пример развёртывания
```python
contract = Contract(...)
contract.deploy()
```

#### Отправка внутренних сообщений
```python
contract.send_internal_message("method", params)
```

#### Вызов get-методов
```python
result = contract.run_get_method("method_name", args)
```

---

### `AdminWallet`
Обёртка над кошельком TON, управляющая взаимодействием со смарт-контрактами.
Инициализируется заранее заданными параметрами конфигурации.

#### Отправка сообщений
```python
wallet = AdminWallet(config)
wallet.send_message(contract_address, payload)
```

---

### `DeployService`
Высокоуровневый API для развёртывания контрактов с интеграцией ядра проекта.

```python
from src.core.contract import Contract
from src.model.schemas import StateInit, AbstractMessage

class DeployService:

    async def deploy_smart_contract_via_client(self, state_init: StateInit) -> AbstractMessage:
        print("[DEPLOY SERVICE] = [Start Deploying Smart Contract]")
        result: AbstractMessage = await Contract(state_init = state_init).deploy_smart_contract_via_client()
        print(f"[DEPLOY SERVICE] = [{result.message}]")

        return result

    async def deploy_smart_contract_via_tonapi(self, state_init: StateInit) -> AbstractMessage:
        print("[DEPLOY SERVICE] = [Start Deploying Smart Contract]")
        result: AbstractMessage = await Contract(state_init = state_init).deploy_smart_contract_via_tonapi()
        print(f"[DEPLOY SERVICE] = [{result.message}]")

        return result
```

---
### Главный метод кошелька

#### `send_internal_message_via_client`
```python
async def send_internal_message_via_client(
    self,
    destination: str,
    amount: int,
    body: Cell = Cell.empty(),
    state_init: StateInit = None
) -> AbstractMessage:

    if self.provider_config is None:
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
```

### Методы контракта

#### `run_get_method`
```python
async def run_get_method(self, method_name: str) -> int:
    wallet = AdminWallet()

    if wallet.provider_config is None:
        async with LiteClient.from_mainnet_config(trust_level = 2) as provider:
            pytoniq_wallet = await AdminWallet().as_wallet_v4r2(provider = provider)
            result = await pytoniq_wallet.run_get_method(
                method = method_name,
                stack = []
            )
            return result

    async with LiteClient.from_mainnet_config(trust_level = wallet.provider_config) as provider:
        pytoniq_wallet = await AdminWallet().as_wallet_v4r2(provider = provider)
        result = await pytoniq_wallet.run_get_method(
            method = method_name,
            stack = []
        )
        return result
```

#### `send_message_to_smart_contract`
```python
async def send_message_to_smart_contract(
    self,
    body: Cell,
    amount: int = DEFAULT_AMOUNT
) -> AbstractMessage:

    wallet = AdminWallet()

    result = await wallet.send_internal_message_via_client(
        destination = self.address,
        amount = amount,
        body = body
    )

    return result
```

#### `deploy_smart_contract_via_client`
```python
async def deploy_smart_contract_via_client(
    self,
    amount: int = DEFAULT_AMOUNT
) -> AbstractMessage:

    wallet = AdminWallet()

    result = await wallet.send_internal_message_via_client(
        destination = self.address,
        amount = amount,
        state_init = PytoniqStateInit(
            data = self.state_init.data,
            code = self.state_init.code
        )
    )

    return result
```

---

## 📅 Точка входа в проект
Основная логика инициализации и развёртывания контракта:
```python
async def main():
    state_init = StateInit(
        code = await from_boc_to_cell(CODE_BOC_FORMAT),
        data = await as_init_data(number = 0)
    )

    contract = await Contract.create(state_init)
    result = await contract.deploy_smart_contract_via_client()

    print(result.message)
```

---

## 📖 Список литературы
- Дуров Н. *Telegram Open Network*, 2 марта 2019, 132 страницы
