from database import SessionDependency
from models import User


async def get_users_db(session: SessionDependency):
    yield User.get_db(session=session)
