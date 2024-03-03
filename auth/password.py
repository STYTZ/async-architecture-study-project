from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"])


def check(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)
