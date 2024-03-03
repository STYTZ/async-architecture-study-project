import logging
import uuid
from contextlib import asynccontextmanager

from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException
from faststream.confluent import KafkaBroker

import schemas
import db
import models
from password import check, get_hash
from settings import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(name)s:\t%(message)s"
)
logger = logging.getLogger(__name__)

broker = KafkaBroker(settings.kafka_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await db.init_db()
    # logger.info("DB ready")
    await broker.start()
    logger.info("Broker started")
    try:
        yield
    finally:
        await broker.close()
        logger.info("Broker stopped")
        # await db.clean_db()
        # logger.info("DB cleaned")


app = FastAPI(lifespan=lifespan)


@app.post("/signup")
async def signup(signup_data: schemas.SignUp = Depends()) -> dict:
    async with db.new_session() as session:
        query = select(models.User).where(models.User.login == signup_data.login)
        result = await session.scalar(query)
        if result:
            msg = f"User with login={result.login} already exists with public_id={result.public_id}"
            raise HTTPException(status_code=400, detail=msg)
        new_user = models.User(
            public_id=str(uuid.uuid4()),
            login=signup_data.login,
            password=get_hash(signup_data.password),
            email=signup_data.email,
            role=models.Role.EMPLOYEE,
        )
        session.add(new_user)
        await session.commit()
    event = schemas.UserCreatedEvent(
        public_id=new_user.public_id,
        login=new_user.login,
        email=new_user.email,
        role=new_user.role,
    )
    await broker.publish(event, topic="user-events")
    return {"public_id": new_user.public_id}


# @app.post("/login")
# async def login(login_data: schemas.Login = Depends()) -> dict:
#     return {}