import asyncio

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/logout")
async def logout():
    await asyncio.sleep(0)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token", httponly=True)
    return response
