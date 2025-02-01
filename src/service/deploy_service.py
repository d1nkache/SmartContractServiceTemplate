from src.model.atd.counter import Counter
from src.model.schemas import StateInit, AbstractMessage


class DeployService:
    
    async def deploy_smart_contract_via_client(self, state_init: StateInit) -> AbstractMessage:

        print("[DEPLOY SERVICE] - [Start Deploying Smart Contract]")
        result: AbstractMessage = await Counter(state_init = state_init).deploy_smart_contract_via_client(start_number = 0)
        print(f"[DEPLOY SERVICE] - [{result.message}]")

        return result
        

    async def deploy_smart_contract_via_tonapi(self, state_init: StateInit) -> AbstractMessage: 

        print("[DEPLOY SERVICE] - [Start Deploying Smart Contract]")
        result: AbstractMessage = await Counter(state_init = state_init).deploy_smart_contract_via_tonapi(start_number = 0)
        print(f"[DEPLOY SERVICE] - [{result.message}]")

        return result
