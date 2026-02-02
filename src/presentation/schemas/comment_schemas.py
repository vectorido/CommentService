from pydantic import BaseModel

class CommentCreateSchema(BaseModel):
    entity_type: str
    entity_id: str
    author_id: str
    text: str


class CommentUpdateSchema(BaseModel):
    comment_id: str
    entity_type: str
    entity_id: str
    new_text: str


class CommentOutSchema(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    author_id: str
    text: str
    created_at: str
    updated_at: str

