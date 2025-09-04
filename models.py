from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


# Users
class UsersBase(SQLModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    disabled: str

class Users(UsersBase, table=True):
    user_id: int | None = Field(default=None, primary_key=True)

# A country
class CountryBase(SQLModel):
    country_name: str

class Country(CountryBase, table=True):
    country_id: int = Field(primary_key=True)

    locations: list["Location"] = Relationship(back_populates="the_country")

class CountryPublic(CountryBase):
    country_id: int

# A location
class LocationBase(SQLModel):
    location_name: str
    country_id: int = Field(foreign_key="country.country_id")

class Location(LocationBase, table=True):
    location_id: int = Field(primary_key=True)

    the_country: Country | None = Relationship(back_populates="locations")

class LocationPublic(LocationBase):
    location_id: int

# A group
class Thing_GroupBase(SQLModel):
    group_name: str

class Thing_Group(Thing_GroupBase, table=True):
    group_id: int = Field(primary_key=True)

    categories: list["Category"] = Relationship(back_populates="the_group")

class Thing_GroupPublic(Thing_GroupBase):
    group_id: int

# A category
class CategoryBase(SQLModel):
    category_name: str
    group_id: int = Field(foreign_key="thing_group.group_id")

class Category(CategoryBase, table=True):
    category_id: int = Field(primary_key=True)

    the_group: Thing_Group | None = Relationship(back_populates="categories")

class CategoryPublic(CategoryBase):
    category_id: int

# An image
class ImageBase(SQLModel):
    image_ref: str

class Image(ImageBase, table=True):
    image_id: int = Field(primary_key=True)

class ImagePublic(ImageBase):
    image_id: int

# A Thing
class ThingBase(SQLModel):
    thing_title: str
    thing_desc: str
    thing_website: str
    thing_where: str
    thing_review: str
    thing_share: bool
    thing_date_added: datetime

    # these are actually foreign keys
    thing_img: int
    thing_category: int
    thing_user: int
    thing_location: int

class ThingPublic(ThingBase):
    thing_id: int

class Thing(ThingBase, table=True):
    thing_id: int | None = Field(default=None, primary_key=True)