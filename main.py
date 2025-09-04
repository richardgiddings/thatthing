from typing import Annotated
from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from starlette import status
from decouple import config

from models import *
from auth import get_current_user, router
from auth_bearer import JWTBearer
from database import SessionDep, get_session, create_db_and_tables

# pagination
from fastapi_pagination import add_pagination, paginate
from fastapi_pagination.links import Page as BasePage
from fastapi_pagination.customization import UseParamsFields, CustomizedPage
from fastapi_pagination.utils import disable_installed_extensions_check


PAGE_SIZE = config('PAGE_SIZE', default=15, cast=int)

# Set the page size
Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(PAGE_SIZE, ge=0),
    ),
]

app = FastAPI()
add_pagination(app)

# import the auth paths
app.include_router(router)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency):
    """
    Returns the user details including token when logged in
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}

@app.get('/countries/')
def read_countries(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Country]:
    countries = session.exec(select(Country).offset(offset).limit(limit)).all()
    return countries

@app.get('/locations/')
def read_locations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Location]:
    locations = session.exec(select(Location).offset(offset).limit(limit)).all()
    return locations

@app.get('/groups/')
def read_groups(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Thing_Group]:
    groups = session.exec(select(Thing_Group).offset(offset).limit(limit)).all()
    return groups

@app.get('/categories/')
def read_categories(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Category]:
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories

@app.get('/images/')
def read_images(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Image]:
    images = session.exec(select(Image).offset(offset).limit(limit)).all()
    return images

@app.get('/things/')
def read_things(*, session: Session = Depends(get_session)) -> Page[ThingPublic]:
    things = session.exec(select(Thing)).all()
    return paginate(things)

@app.get('/things_for_user/', dependencies=[Depends(JWTBearer())])
def read_things_for_user(*, 
                            session: Session = Depends(get_session), 
                            current_user: Annotated[Users, Depends(get_current_user)]
                        ) -> Page[ThingPublic]:

    user_id = current_user.get("id")
    things = session.exec(select(Thing).filter_by(thing_user=user_id)).all()
    return paginate(things)