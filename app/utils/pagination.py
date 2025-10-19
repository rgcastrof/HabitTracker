from typing import List, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def paginate_data(
        data: List[dict],
        page: int,
        page_size: int,
        model: Type[T]
    ) -> dict:

    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = [model.model_validate(u) for u in data[start:end]]
    total = len(data)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": paginated_items
    }
