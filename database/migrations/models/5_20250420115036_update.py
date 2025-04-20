from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "userfavouritepost";
        DROP TABLE IF EXISTS "userfavouritepost";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "userfavouritepost" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""
