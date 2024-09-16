

from fastapi import APIRouter, Depends, HTTPException
from fund_management.infrastructure.environment import config
from fund_management.infrastructure.repository_impl.transaction_repository_impl import TransactionRepositoryImpl

router = APIRouter()


async def get_transaction_repository() -> TransactionRepositoryImpl:
    repo = TransactionRepositoryImpl()
    await repo.initialize(config.database_name)
    return repo

@router.get("/transactions/{user_id}", response_model={})
async def get_all_funds(user_id: str,repo: TransactionRepositoryImpl = Depends(get_transaction_repository)):
    try:
        funds = await repo.find_by_user_id(user_id)
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting funds: {e}")