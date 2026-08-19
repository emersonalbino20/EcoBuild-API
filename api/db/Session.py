import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
  raise ValueError("Env variable DATABASE_URL not set")

if database_url:
  if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(database_url)

AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
	)

async def get_db():
  async with AsyncSessionLocal() as db:
    yield db

