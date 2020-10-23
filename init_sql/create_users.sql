CREATE TABLE users (
    id serial primary key  not null,
    email varchar(200) not null,
    created_date timestamp default CURRENT_TIMESTAMP
);

insert into users (email) values('m@wth.me');