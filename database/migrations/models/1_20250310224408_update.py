from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
        ALTER TABLE "post" ALTER COLUMN "category_id" DROP NOT NULL;
        CREATE TABLE IF NOT EXISTS "user_post" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_post";
        ALTER TABLE "post" ALTER COLUMN "category_id" SET NOT NULL;
        DROP TABLE IF EXISTS "comment";"""
