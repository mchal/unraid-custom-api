CREATE TABLE movies (
    id serial primary key  not null,
    imdb_id varchar(20) not null,
    collection_id int not null,
    user_id int not null,
    created_date timestamp default CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX uix_movies ON movies(imdb_id, collection_id, user_id);
