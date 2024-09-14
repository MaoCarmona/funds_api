from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from fund_management.core.enums import TransactionTypeEnum
from fund_management.infrastructure.environment import config
from fund_management.core.dto import FundResponse, SubscriptionRequest, UnSubscriptionRequest
from fund_management.core.entities import Transaction, Fund
from fund_management.infrastructure.repository_impl.fund_repository_impl import FundRepositoryImpl
from fund_management.infrastructure.repository_impl.notification_repository_impl import NotificationRepositoryImpl
from fund_management.infrastructure.repository_impl.transaction_repository_impl import TransactionRepositoryImpl

router = APIRouter()

async def get_fund_repository() -> FundRepositoryImpl:
    repo = FundRepositoryImpl()
    await repo.initialize(config.database_name)
    return repo

async def get_transaction_repository() -> TransactionRepositoryImpl:
    repo = TransactionRepositoryImpl()
    await repo.initialize(config.database_name)
    return repo

async def get_notification_repository() -> NotificationRepositoryImpl:
    repo = NotificationRepositoryImpl()
    return repo


@router.get("/funds/", response_model=List[FundResponse])
async def get_all_funds(repo: FundRepositoryImpl = Depends(get_fund_repository)):
    try:
        funds = await repo.find_all()
        return funds
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting funds: {e}")
    
@router.post("/funds/", response_model={})
async def save_fund(fund: Fund,repo: FundRepositoryImpl = Depends(get_fund_repository)):
    try:
        await repo.save(fund)
        return {"status": 200 , "msg": "Created succesfully"} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting funds: {e}")

@router.post("/funds/subscribe/{fund_id}", response_model=str)
async def subscribe_to_fund(data: SubscriptionRequest,fund_id, 
                            repo: FundRepositoryImpl = Depends(get_fund_repository), 
                            transaction_repo: TransactionRepositoryImpl = Depends(get_transaction_repository),
                            notification_repo: NotificationRepositoryImpl = Depends(get_notification_repository)):
    fund = await repo.find_by_id(str(fund_id))
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    if data.amount < fund.min_investment_amount:
        raise HTTPException(status_code=400, detail=f"No balance available to link to the fund {fund.name} , the minimum is ${fund.min_investment_amount}")
    
    transaction = Transaction(
        user_id=data.user_id,
        fund_id=str(fund_id),
        amount=data.amount,
        type=str(TransactionTypeEnum.SUBSCRIBE.value)
    )
    await transaction_repo.save(transaction)
    msg = f"Your subscription to the {fund.name} Fund was successful."
    notification_repo.send_sms(data.phone,msg )
    
    return msg

@router.post("/funds/unsubscribe/{fund_id}", response_model=str)
async def unsubscribe_from_fund(data: UnSubscriptionRequest,fund_id, 
                                repo: FundRepositoryImpl = Depends(get_fund_repository), 
                                transaction_repo: TransactionRepositoryImpl = Depends(get_transaction_repository),
                                notification_repo: NotificationRepositoryImpl = Depends(get_notification_repository)):
    fund = await repo.find_by_id(str(fund_id))
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    transaction = Transaction(
        user_id=data.user_id,
        fund_id=str(fund_id),
        amount=0,
        type=str(TransactionTypeEnum.UNSUSCRIBE.value)
    )
    await transaction_repo.save(transaction)
    msg = f"Your unsubscription to the {fund.name} Fund was successful."
    notification_repo.send_sms(data.phone,msg )
    return msg
