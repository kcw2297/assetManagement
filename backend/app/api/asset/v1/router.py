from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.common.auth.security import verify_jwt_token
from app.common.schema import JsonResponse
from app.common.util.logging import logging
from app.module.asset.model import AssetStock
from app.module.asset.repository.asset_repository import AssetRepository
from app.module.asset.schema.asset_schema import AssetTransaction, AssetTransactionRequest
from app.module.asset.schema.stock_schema import StockAsset, StockAssetResponse
from app.module.auth.constant import DUMMY_USER_ID
from database.dependency import get_mysql_session

asset_router = APIRouter(prefix="/v1")


@asset_router.get("/dummy/asset", summary="임시 자산 정보를 반환합니다.", response_model=StockAssetResponse)
async def get_dummy_assets(db: AsyncSession = Depends(get_mysql_session)) -> StockAssetResponse:
    dummy_assets = await AssetRepository.get_asset_stock(db, DUMMY_USER_ID)

    stock_assets = []
    total_asset_amount = 0
    total_asset_growth_rate = 0
    total_invest_amount = 0
    total_invest_growth_rate = 0
    total_profit_amount = 0
    total_profit_rate = 0
    total_dividend_amount = 0
    total_dividend_rate = 0

    for asset in dummy_assets:
        logging.info(
            f"[분석]Asset ID: {asset.id}, Quantity: {asset.quantity}, Investment Bank: {asset.investment_bank}, User ID: {asset.user_id}"
        )
        for stock in asset.stock:
            asset_stock = await db.execute(
                select(AssetStock).filter(AssetStock.asset_id == asset.id, AssetStock.stock_code == stock.code)
            )
            asset_stock = asset_stock.scalar_one_or_none()

            logging.info(
                f"[분석]Stock Code: {stock.code}, Stock Name: {stock.name}, Market Index: {stock.market_index}, Purchase Price: {asset_stock.purchase_price}"
            )
            # [수정] 현재 매입가와 배당금 데이터 수집이 미완료 되어서, 데이터 수집 완료 후 수정하겠습니다.
            purchase_price = asset_stock.purchase_price if asset_stock.purchase_price is not None else 1000.0
            temp_dividend = 1000.0

            stock_asset = StockAsset(
                stock_name=stock.name,
                quantity=asset.quantity,
                buy_date=asset.purchase_date,
                profit=0,
                highest_price=0,
                lowest_price=0,
                stock_volume=0,
                investment_bank=asset.investment_bank,
                dividend=temp_dividend,
                purchase_price=purchase_price,
                purchase_amount=purchase_price * asset.quantity,
            )
            stock_assets.append(stock_asset)

    return StockAssetResponse(
        stock_assets=stock_assets,
        total_asset_amount=total_asset_amount,
        total_asset_growth_rate=total_asset_growth_rate,
        total_invest_amount=total_invest_amount,
        total_invest_growth_rate=total_invest_growth_rate,
        total_profit_amount=total_profit_amount,
        total_profit_rate=total_profit_rate,
        total_dividend_amount=total_dividend_amount,
        total_dividend_rate=total_dividend_rate,
    )


@asset_router.get("/asset", summary="사용자의 자산 정보를 반환합니다.", response_model=list[AssetTransaction])
async def get_assets(
    token: dict = Depends(verify_jwt_token), db: AsyncSession = Depends(get_mysql_session)
) -> list[AssetTransaction]:
    user_id = token.get("sub")
    if user_id is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자 id를 찾지 못하였습니다.")

    try:
        result = await AssetRepository.get_assets(db, user_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자의 자산관리 정보를 찾지 못하였습니다.")
    else:
        return result


@asset_router.post("/asset", summary="자산관리 정보를 등록합니다.", response_model=JsonResponse)
async def save_assets(
    transaction_data: AssetTransactionRequest,
    token: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_mysql_session),
) -> JsonResponse:
    try:
        await AssetRepository.save_assets(db, transaction_data.transactions)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="자산 정보를 저장하는데 실패하였습니다.")
    else:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"detail": "자산 정보가 성공적으로 저장되었습니다."})


@asset_router.put("/asset", summary="자산관리 정보를 수정합니다.", response_model=JsonResponse)
async def update_assets(
    transaction_data: AssetTransactionRequest,
    token: dict = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_mysql_session),
) -> JsonResponse:
    try:
        await AssetRepository.update_assets(db, transaction_data.transactions)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="해당 자산관리 정보를 찾지 못하였습니다.")
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"detail": "자산 정보가 성공적으로 수정 되었습니다."})
