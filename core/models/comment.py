from pydantic import BaseModel


class Comment(BaseModel):
    """Модель для представления комментария."""
    postId: int
    id: int
    name: str
    email: str
    body: str