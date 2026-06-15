from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.database import get_db
from src.infrastructure.postgres.repositories.location_rep import LocationRepository
from src.application.use_cases.location.create_location import CreateLocationUseCase
from src.application.use_cases.location.update_location import UpdateLocationUseCase
from src.application.use_cases.location.delete_location import DeleteLocationUseCase
from src.application.use_cases.location.get_location import GetLocationUseCase
from src.application.use_cases.location.get_list_location import GetLocationListUseCase


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_location_repository(session: DbSession) -> LocationRepository:
    return LocationRepository(session)


LocationRepositoryDep = Annotated[LocationRepository,
                                  Depends(get_location_repository)]


def get_location_list_use_case(
    repository: LocationRepositoryDep,
) -> GetLocationListUseCase:
    return GetLocationListUseCase(repository)


def get_location_use_case(
    repository: LocationRepositoryDep,
) -> GetLocationUseCase:
    return GetLocationUseCase(repository)


def get_create_location_use_case(
    repository: LocationRepositoryDep,
) -> CreateLocationUseCase:
    return CreateLocationUseCase(repository)


def get_update_location_use_case(
    repository: LocationRepositoryDep,
) -> UpdateLocationUseCase:
    return UpdateLocationUseCase(repository)


def get_delete_location_use_case(
    repository: LocationRepositoryDep,
) -> DeleteLocationUseCase:
    return DeleteLocationUseCase(repository)


GetLocationListUseCaseDep = Annotated[
    GetLocationListUseCase,
    Depends(get_location_list_use_case),
]

GetLocationUseCaseDep = Annotated[
    GetLocationUseCase,
    Depends(get_location_use_case),
]

CreateLocationUseCaseDep = Annotated[
    CreateLocationUseCase,
    Depends(get_create_location_use_case),
]

UpdateLocationUseCaseDep = Annotated[
    UpdateLocationUseCase,
    Depends(get_update_location_use_case),
]

DeleteLocationUseCaseDep = Annotated[
    DeleteLocationUseCase,
    Depends(get_delete_location_use_case),
]
