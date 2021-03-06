from typing import Any

from fastapi import APIRouter, Depends, Response, status
from src.application.service.project import ProjectService, ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel
from src.presentation.controller._common_query_param import CommonQueryParams
from src.presentation.schema.project import Project as ProjectSchema
from src.presentation.schema.project import ProjectPatch as ProjectPatchSchema
from src.presentation.schema.project import Projects as ProjectsSchema

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("", response_model=ProjectsSchema)
def get_projects(
        params: CommonQueryParams = Depends(CommonQueryParams),
        service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    projects = service.read_projects(params.skip, params.limit)
    return {"projects": projects}


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(project_id: int, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.read(project_id)
    return project


@router.post("", response_model=ProjectSchema)
def post(
        payload: ProjectSchema,
        service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.create(ProjectModel(**payload.dict()))
    return project


@router.put("/{project_id}", response_model=ProjectSchema)
def put(project_id: int, payload: ProjectSchema, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.replace(ProjectModel(**payload.dict()), project_id)
    return project


@router.patch("/{project_id}", response_model=ProjectPatchSchema)
def patch(project_id: int, payload: ProjectPatchSchema, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    project = service.update(payload.dict(exclude_unset=True), project_id)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: int, service: ProjectService = Depends(ProjectServiceImpl)) -> Any:
    service.delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
