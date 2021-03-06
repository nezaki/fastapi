from typing import List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: Optional[int] = Field(
        title="id",
        readOnly=True,
    )
    name: str = Field(
        title="名前",
        description="名前",
        min_length=1,
        max_length=32,
        example="name example",
        nullable=False,
    )
    description: Optional[str] = Field(
        title="説明",
        description="説明",
        min_length=1,
        max_length=256,
        example="description example",
        nullable=True,
    )

    class Config:
        orm_mode = True


class Projects(BaseModel):
    projects: List[Project]


class ProjectPatch(Project):
    name: Optional[str] = Project.__fields__.get("name").field_info
