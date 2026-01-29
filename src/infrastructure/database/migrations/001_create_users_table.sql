create table if not exists users (
    id serial primary key,
    email varchar(255) unique not null,
    name varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

create index if not exists idx_users_email on users(email);

