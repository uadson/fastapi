from fastapi import FastAPI, HTTPException, status, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    
    
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    

class HeroCreate(HeroBase):
    pass    


class HeroPublic(HeroBase):
    id: int
    

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
def create_hero(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


# @app.get("/heroes/", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
# def read_heroes():
#     with Session(engine) as session:
#         heroes = session.exec(select(Hero)).all()
#         return heroes

@app.get("/heroes/", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes
    

@app.get("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
        return hero
    

@app.patch("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero


# def select_heroes():
#     with Session(engine) as session:
#         statement_1 = select(Hero)
#         results = session.exec(statement_1)
#         heroes = results.all()
#         Compact
#         heroes = session.exec(select(Hero)).all()
#         print(heroes)
#         List
#         for hero in results:
#             print(hero)
#         Filter
#         statement_2 = select(Hero).where(Hero.name == "DeadPond")
#         one_hero = session.exec(statement_2)
#         for data in one_hero:
#             print(data)
        

# def main():
#     select_heroes()
    

# if __name__ == "__main__":
#     main()
