CREATE TABLE if not exists Users (
  id serial primary key,
  name varchar,
  email varchar,
  imgURL varchar,
  total_finished_challenges integer,
  finished_challenges varchar,
  streak integer,
  last_challenge_completion_time date
);

CREATE TABLE if not exists Challenge (
  id serial primary key,
  text varchar,
  imgURL varchar,
  time_to_finish date
);

CREATE TABLE if not exists Completions (
  id serial primary key,
  user_id integer,
  challenge_id integer,
  start_time date,
  finish_time date,

  FOREIGN KEY (user_id) REFERENCES Users (id),
  FOREIGN KEY (challenge_id) REFERENCES Challenge (id)
);

-- drop table Challenge cascade;
-- drop table Users;
-- drop table Completions;
