from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "flower" ALTER COLUMN "type" SET DEFAULT 'white';
        ALTER TABLE "user" ADD "token" VARCHAR(128) NOT NULL DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "token";
        ALTER TABLE "flower" ALTER COLUMN "type" SET DEFAULT 'FlowerType.white';"""
