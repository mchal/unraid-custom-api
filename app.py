from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

import re
import asyncpg
import movie

app = FastAPI()

origins = [
    "https://*.imdb.com/title/tt*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def connect():
    host = 'fastapi-postgres'
    username = 'watchlist'
    password = 'blahblah'
    database = 'watchlist'

    conn = await asyncpg.connect(f'postgres://{username}:{password}@{host}/{database}')
    return conn


def valid_imdb_id(imdb_id):
    imdb_id = imdb_id.strip()
    pattern = '^tt[0-9]+$'

    matched = re.match(pattern, imdb_id)
    if matched:
        return True
    return False


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movie/{imdb_id}")
async def get_movies(imdb_id: str):
    # filter out invalid imdb_ids
    imdbs = map(lambda x: x.strip(), imdb_id.split(','))
    imdbs = list(filter(valid_imdb_id, imdbs))
    if not imdbs:
        return {}

    conn = await connect()
    data = await movie.get_movies(conn, imdbs)
    return data


@app.delete("/movie/{imdb_id}/{collection_id}")
async def delete_movies(imdb_id: str, collection_id: int):
    conn = await connect()
    email = 'm@wth.me'
    data = await movie.delete_movie(conn, imdb_id, collection_id, email)
    return {"result": data}


@app.put("/movie/{imdb_id}/{collection_id}")
async def add_movie(imdb_id: str, collection_id: int):
    conn = await connect()
    email = 'm@wth.me'
    data = await movie.add_movie(conn, imdb_id, collection_id, email)
    return {"result": data}
