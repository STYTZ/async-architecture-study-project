import uuid

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings
from models import DbBase, Role, User
from password import get_hash

engine = create_async_engine(settings.auth_db_url.unicode_string())
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.create_all)
    async with new_session() as session:
        root = User(
            public_id=str(uuid.uuid4()),
            login="root",
            password=get_hash(settings.auth_root_password),
            email="root@popug.com",
            role=Role.ADMIN,
        )
        session.add(root)
        await session.commit()


async def clean_db():
    async with engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.drop_all)
