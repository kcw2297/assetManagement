# Library
from fastapi import HTTPException
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuthError
from httpx import AsyncClient
# Module
from auth.service.config import oauth

async def fetch_kakao_user_info(access_token: str):
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers)
        user_info = response.json()
        return user_info

async def authenticate_with_kakao(request: Request):
    try:
        token_response = await oauth.kakao.authorize_access_token(request)
        user_info = await fetch_kakao_user_info(token_response['access_token'])
        
        social_id = user_info.get('id')
        if not social_id:
            raise HTTPException(status_code=400, detail="카카오 로그인이 실패하였습니다.")
        return social_id
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error.error}")

    
    