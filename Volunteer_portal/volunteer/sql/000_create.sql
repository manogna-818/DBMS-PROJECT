drop table if exists users cascade;
drop table if exists student cascade;
drop table if exists administrator cascade;
drop table if exists activities cascade;
drop table if exists applications cascade;

create table users(
    id serial primary key,
    u_id text unique not null, 
    name text not null,
    dob date,
    email text unique not null,
    mobileno text unique not null,
    usertype text not null,
    yearofstudy text ,
    dept text,
    password text not null
);

create table student(
    stu_id text unique references users(u_id) on delete cascade,
    yearofstudy text not null
);

create table administrator(
    adm_id text unique references users(u_id) on delete cascade,
    dept text not null
);

create table activities(
    act_id serial primary key,
    adm_id text references administrator(adm_id) on delete cascade,
    title text not null,
    skills text not null,
    description text not null,
    startdate date,
    enddate date
);
create table applications(
    app_id serial primary key,
    stu_id text references student(stu_id) on delete cascade,
    adm_id text references administrator(adm_id) on delete cascade,
    act_id integer references activities(act_id) on delete cascade,
    status text default 'applied',
    applicationdate date
);
