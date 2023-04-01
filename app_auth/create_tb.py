from core.configs import settings
from core.database import engine

from time import sleep


async def create_tables() -> None:
    import models.__all_models
    print("Creating tables on database")
    sleep(2)

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print("Tables created successfully.")
    sleep(2)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
