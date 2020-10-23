CREATE TABLE collections (
    id serial primary key not null,
    name varchar(50) not null,
    user_id int not null default -1,
    created_date timestamp default CURRENT_TIMESTAMP
);

INSERT INTO collections (name, user_id)
VALUES('watchlist', -1), ('owned', -1);