CREATE TABLE weather ( 
id integer primary key auto_increment,
date INT not null,
temperature_out real not null,
humidity_out real not null,
pressure_out real not null,
weather_description tinytext not null,
previous_data_used_api boolean default TRUE
)