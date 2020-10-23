from typing import List


async def get_movies(conn, imdb_ids: List[str]):
    imdb_dict = {}

    in_imdbs = "'" + "', '".join(imdb_ids) + "'"

    sql = f'''
        select m.imdb_id, c.name
        from movies m
        inner join collections c
        on m.collection_id = c.id
        where m.imdb_id in ({in_imdbs})
        '''

    data = await conn.fetch(sql)

    for row in data:
        if row['imdb_id'] not in imdb_dict:
            imdb_dict[row['imdb_id']] = []
        imdb_dict[row['imdb_id']].append(row['name'])

    return imdb_dict


async def delete_movie(conn, imdb_id, collection_id, email):
    sql = '''
    delete from movies m
    using users u, collections c
    WHERE
        c.id = m.collection_id
        and (c.user_id = u.id or c.user_id = -1)
        
        and m.imdb_id = $1
        AND u.email = $2
        AND c.id = $3;
    '''
    result = await conn.execute(sql, imdb_id, email, collection_id)
    return result


async def add_movie(conn, imdb_id, collection_id, email):
    sql = '''
    INSERT INTO movies (imdb_id, collection_id, user_id)
    SELECT $1, $2, u.id
    FROM collections c
    INNER JOIN users u 
    ON u.id = c.user_id OR c.user_id = -1 -- just to make sure that user has access to the colletion
    WHERE u.email = $3
    AND c.id = $2
    ON CONFLICT (imdb_id, collection_id, user_id) DO
    UPDATE SET
        created_date = NOW()
    '''

    result = await conn.execute(sql, imdb_id, collection_id, email)
    return result
