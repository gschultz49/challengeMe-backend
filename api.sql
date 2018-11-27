-- https://bitwiser.in/2015/09/09/add-google-login-in-flask.html
-- https://developers.facebook.com/docs/graph-api/reference/user/friends/
-- https://github.com/rochacbruno/flasgger

--get users data (streak, total finished challenges, name, imgURL, email) to display on the "my account" page
select * from Users where id = ?

--get all of the users completed
select * from Completions
inner join Challenge on Challenge.id = Completions.challenge_id
where Completions.user_id = ?
--most recent completions first
order by Completions.id asc


--get all rows back (helpful for random challenge selection)
select * from Challenge

