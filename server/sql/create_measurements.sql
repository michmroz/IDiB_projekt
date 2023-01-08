CREATE TABLE measurements ( 
id integer primary key auto_increment,
date INT not null,
temperature real not null,
humidity real not null,
light real not null,
previous_data_used_ser boolean default TRUE
)

