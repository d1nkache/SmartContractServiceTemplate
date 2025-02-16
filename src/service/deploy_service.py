from src.сore.contract import Contract
from src.model.schemas import StateInit, AbstractMessage


class DeployService:
    
    async def deploy_smart_contract_via_client(self, state_init: StateInit) -> AbstractMessage:

        print("[DEPLOY SERVICE] - [Start Deploying Smart Contract]")
        result: AbstractMessage = await Contract(state_init = state_init).deploy_smart_contract_via_client()
        print(f"[DEPLOY SERVICE] - [{result.message}]")

        return result
        
    # навряд ли работает - не тестил
    async def deploy_smart_contract_via_tonapi(self, state_init: StateInit) -> AbstractMessage: 

        print("[DEPLOY SERVICE] - [Start Deploying Smart Contract]")
        result: AbstractMessage = await Contract(state_init = state_init).deploy_smart_contract_via_tonapi(start_number = 0)
        print(f"[DEPLOY SERVICE] - [{result.message}]")

        return result
