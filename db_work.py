from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, Column, String
import environ

env = environ.Env()
environ.Env.read_env()


PG_DSN = env('DB')
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class People_swap(Base):

    __tablename__ = 'SwapiAllCaracters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def save_database(data: list):

    async with engine.begin() as new:
        await new.run_sync(Base.metadata.drop_all)
        await new.run_sync(Base.metadata.create_all)

    async_session = Session

    async with async_session() as session:
        async with session.begin():
            for person in data:
                    persons = People_swap(
                        name=person['name'],
                        birth_year=person['birth_year'],
                        eye_color=person['eye_color'],
                        films=person['films'],
                        gender=person['gender'],
                        hair_color=person['hair_color'],
                        height=person['height'],
                        homeworld=person['homeworld'],
                        mass=person['mass'],
                        skin_color=person['skin_color'],
                        species=person['species'],
                        starships=person['starships'],
                        vehicles=person['vehicles'],
                    )
                    session.add(persons)

        await session.commit()


