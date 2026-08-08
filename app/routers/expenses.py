from fastapi import APIRouter

router=APIRouter(prefix='/expenses',tags=['Expenses'])

@router.get("/")
async def get_all_expenses():
    return