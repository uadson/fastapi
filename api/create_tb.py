from time import sleep

from sqlmodel import SQLModel

from core.database import engine


async def create_tables() -> None:
    import models.__all_models
    print("Creating tables...")
    sleep(1.5)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print('Tables created successfully.')
    sleep(1.5)


if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
