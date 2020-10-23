import asyncio
import asyncpg
import pandas as pd


async def connect():
    host = '127.0.0.1'
    username = 'watchlist'
    password = 'blahblah'
    database = 'watchlist'

    conn = await asyncpg.connect(f'postgres://{username}:{password}@{host}/{database}')
    return conn


async def main():
    conn = await connect()

    df = pd.read_csv('export_watchlist.csv')
    df['id'] = None

    df['created_date'] = pd.to_datetime(df['created_date'], format='%Y-%m-%d %H:%M:%S')
    sql = '''INSERT INTO movies(imdb_id, collection_id, user_id, created_date) 
    SELECT imdb_id, collection_id, user_id, created_date FROM UNNEST($1::movies[]) a
    '''
    await conn.execute(sql, df[['id', 'imdb_id', 'collection_id', 'user_id', 'created_date']].to_dict('records'))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
