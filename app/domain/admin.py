import asyncio

from app.api.dependencies import AuthProvider
from app.config import load_config
from app.infrastructure.database.dao import HolderDao
from app.infrastructure.database.factory import make_connection_string, create_pool


class Creator:
    def __init__(self):
        self.settings = load_config()
        self.auth_provider = AuthProvider(settings=self.settings)
        self.pool = create_pool(url=make_connection_string(settings=self.settings))

    async def create_superuser(self):
        first_name = input(">> Enter firstname: ")
        last_name = input(">> Enter lastname: ")
        email = input(">> Enter email: ")
        password = input(">> Enter password: ")
        async with self.pool() as session:
            dao = HolderDao(session=session)
            if await dao.user.get_user(email=email) is None:
                await dao.user.add_user(
                    firstname=first_name,
                    lastname=last_name,
                    email=email,
                    password=self.auth_provider.get_password_hash(password=password),
                )

    async def create_all(self):
        await self.create_superuser()


creator = Creator()
asyncio.run(creator.create_all())
