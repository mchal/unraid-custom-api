import asyncio
import asyncpg
import pandas as pd


async def connect():
    host = '192.168.86.100'
    username = 'watchlist'
    password = 'blahblah'
    database = 'watchlist'

    conn = await asyncpg.connect(f'postgres://{username}:{password}@{host}/{database}')
    return conn


async def main():
    conn = await connect()

    results = await conn.fetch('select * from movies')
    df = pd.DataFrame([dict(r.items()) for r in results])

    df.to_csv('export_watchlist.csv', index=False)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
