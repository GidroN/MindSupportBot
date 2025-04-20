from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "userfavouritepost";
        ALTER TABLE "post" ADD "text" TEXT NOT NULL;
        ALTER TABLE "post" DROP COLUMN "url";
        ALTER TABLE "post" DROP COLUMN "title";
        DROP TABLE IF EXISTS "userfavouritepost";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ADD "url" VARCHAR(300) NOT NULL;
        ALTER TABLE "post" ADD "title" VARCHAR(255) NOT NULL;
        ALTER TABLE "post" DROP COLUMN "text";
        CREATE TABLE "userfavouritepost" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""
