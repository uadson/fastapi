from fastapi import FastAPI, HTTPException, status, Query, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


# SCHEMAS/MODELS
  
# TEAMS
class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str
    

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    heroes: list['Hero'] = Relationship(back_populates='team')
    

class TeamCreate(TeamBase):
    pass


class TeamPublic(TeamBase):
    id: int
    
    
class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


# HEROES
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    
    team_id: int | None = Field(default=None, foreign_key='team.id')
    
    
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    team: Team | None = Relationship(back_populates='heroes')
    

class HeroCreate(HeroBase):
    password: str  


class HeroPublic(HeroBase):
    id: int
    

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    password: str | None = None
    team_id: int | None = None

# DATABASE
sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

# DEPENDS
def get_session():
    with Session(engine) as session:
        yield session


# ACTIONS
def hash_password(password: str) -> str:
    return f'not really hashed {password} hehehe'

# MAIN
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ROUTERS

# CREATE

# NO DEPENDS
# @app.post("/heroes/", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
# def create_hero(hero: HeroCreate):
#     hashed_password = hash_password(hero.password)
#     with Session(engine) as session:
#         extra_data = {'hashed_password': hashed_password}
#         db_hero = Hero.model_validate(hero, update=extra_data)
#         session.add(db_hero)
#         session.commit()
#         session.refresh(db_hero)
#         return db_hero

# WITH DEPENDS
@app.post('/heroes/', response_model= HeroPublic, status_code=status.HTTP_201_CREATED)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    hashed_password = hash_password(hero.password)
    extra_data = {'hashed_password': hashed_password}
    db_hero = Hero.model_validate(hero, update=extra_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


# @app.get("/heroes/", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
# def read_heroes():
#     with Session(engine) as session:
#         heroes = session.exec(select(Hero)).all()
#         return heroes

# READ

# NO DEPENDS
# @app.get("/heroes/", response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
# def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
#     with Session(engine) as session:
#         heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#         return heroes

# WITH DEPENDS
@app.get('/heroes/', response_model=list[HeroPublic], status_code=status.HTTP_200_OK)
def read_heroes(session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# READ

# NO DEPENDS
# @app.get("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
# def read_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
#         return hero

# WITH DEPENDS
@app.get('/heroes/{hero_id}', response_model=HeroPublic, status_code=status.HTTP_200_OK)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hero not found')
    return hero
    

# UPDATE

# NO DEPENDS
# @app.patch("/heroes/{hero_id}", response_model=HeroPublic, status_code=status.HTTP_200_OK)
# def update_hero(hero_id: int, hero: HeroUpdate):
#     with Session(engine) as session:
#         db_hero = session.get(Hero, hero_id)
#         if not db_hero:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
#         hero_data = hero.model_dump(exclude_unset=True)
#         extra_data = {}
#         if 'password' in hero_data:
#             password = hero_data['password']
#             hashed_password = hash_password(password)
#             extra_data['hashed_password'] = hashed_password
#         db_hero.sqlmodel_update(hero_data)
#         session.add(db_hero)
#         session.commit()
#         session.refresh(db_hero)
#         return db_hero

# WITH DEPENDS
@app.patch('/heroes/{hero_id}', response_model=HeroPublic, status_code=status.HTTP_202_ACCEPTED)
def update_hero(*, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hero not found')
    
    hero_data = hero.model_dump(exclude_unset=True)
    
    extra_data = {}
    
    if 'password' in hero_data:
        password = hero_data['password']
        hashed_password = hash_password(password)
        extra_data['hashed_password'] = hashed_password
        
    db_hero.sqlmodel_update(hero_data)
    
    # for key, value in hero_data.items():
    #     setattr(db_hero, key, value)
    
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    
    return db_hero
    

# DELETE
# NO DEPENDS
# @app.delete('/heroes/{hero_id}')
# def delete_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hero not found')
#         session.delete(hero)
#         session.commit()
#         message = 'Hero deleted successfully!'
#         return {'message': message}

# WITH DEPENDS
@app.delete('/heroes/{hero_id}')
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hero not found')
    session.delete(hero)
    session.commit()
    message = 'Hero deleted successfully'
    return {'message': message}

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

# CREATE
@app.post('/teams/', response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


# READ
@app.get('/teams/', response_model=list[TeamPublic], status_code=status.HTTP_200_OK)
def read_teams(session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams
