from fastapi import APIRouter, Query, Depends
from typing import List, Dict, Optional
from app.repositories.goods_repository import GoodsRepository

router = APIRouter(prefix="/goods", tags=["Dangerous Goods"])


def get_goods_repository() -> GoodsRepository:
    return GoodsRepository()


@router.get("/search", response_model=List[Dict])
async def search_goods(
    query: str = Query(..., min_length=2, description="Search query (UN number or name)"),
    class_filter: Optional[str] = Query(None, description="Filter by DG class"),
    repo: GoodsRepository = Depends(get_goods_repository)
):
    """Search dangerous goods by UN number or name"""
    return repo.search(query, class_filter)


@router.get("/{un_number}", response_model=Dict)
async def get_good_by_un(
    un_number: str,
    repo: GoodsRepository = Depends(get_goods_repository)
):
    """Get dangerous good details by UN number"""
    return repo.get_by_un_number(un_number)


@router.get("/", response_model=List[Dict])
async def list_goods(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    repo: GoodsRepository = Depends(get_goods_repository)
):
    """List all dangerous goods with pagination"""
    return repo.get_all(limit, offset)