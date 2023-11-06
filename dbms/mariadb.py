from os import getenv as cfg
import aiomysql

# decorator
def dbaio(func):
    async def wrapper():
        try:
            conn = await aiomysql.connect(host=cfg("MARIADB_HOST"), port=int(cfg("MARIADB_PORT")), user=cfg("MARIADB_USER"), password=cfg("MARIADB_PASSWORD"), db=cfg("MARIADB_DATABASE"), charset="utf8mb4", autocommit=False)
            cur = await conn.cursor()
            await func(conn, cur)
        except Exception as e:
            await cur.close()
            conn.close()
            print(f"DB Error: {e}")
        finally:
            await cur.close()
            conn.close()
    return wrapper


async def create_db():
    await db_create_user()
    print("[create_db success.]")


@dbaio
async def db_create_user(db, cur):
    await cur.execute("""CREATE TABLE IF NOT EXISTS user (
        id UUID PRIMARY KEY DEFAULT UUID(),
        email VARCHAR(10) UNIQUE NOT NULL,
        pw CHAR(64) NOT NULL,
        nickname CHAR(30) UNIQUE NOT NULL,
        country VARCHAR(2) NOT NULL,
        follows JSON NOT NULL,
        likes JSON NOT NULL,
        hashtags JSON NULL,
        image VARCHAR(20) NULL,
        body VARCHAR(10) NULL,
        created_at DATETIME NOT NULL,
        status bool NOT NULL DEFAULT TRUE );
    """)
    await db.commit()

@dbaio
async def db_test(db, cur):
    await cur.execute("""INSERT INTO user (email,pw,nickname,country,follows,likes,created_at)
        VALUES('em3@e.com','pass','nick3','ko','{"count": "0"}','{"count": "0"}','2011-03-11');""")
    await db.commit()