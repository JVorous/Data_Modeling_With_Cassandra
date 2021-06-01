#drop table statements
drop_session_table = "DROP TABLE IF EXISTS session_library"
drop_user_song_table = "DROP TABLE IF EXISTS user_song_library"
drop_user_session_table = "DROP TABLE IF EXISTS user_session_library"


#Create table statements
create_session_table = ("""
    CREATE TABLE IF NOT EXISTS session_library
    (session_id int, item_in_session int, artist_name text, song_title text, song_length float, 
    PRIMARY KEY(session_id, item_in_session))
""")

create_user_song_table = ("""    
    CREATE TABLE IF NOT EXISTS user_song_library
    (song_title text, user_id int, first_name text, last_name text, PRIMARY KEY(song_title, user_id))
""")

create_user_session_table = ("""    
    CREATE TABLE IF NOT EXISTS user_session_library
    (user_id int, session_id int, item_in_session int, first_name text, last_name text, 
    artist_name text, song_title text, PRIMARY KEY ((user_id, session_id), item_in_session))
""")

#Insert data statements
session_table_insert = [("""
    INSERT INTO session_library (session_id, item_in_session, artist_name, song_title, song_length)
    VALUES (%s, %s, %s, %s, %s)
"""), 'session_library']

user_song_table_insert = [("""
    INSERT INTO user_song_library (song_title, user_id, first_name, last_name)
    VALUES (%s, %s, %s, %s)
"""), 'user_song_library']

user_session_table_insert = [("""
    INSERT INTO user_session_library (user_id, session_id, item_in_session, first_name, last_name, artist_name, song_title)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""), 'user_session_library']


# QUERY LISTS

create_table_queries = [create_session_table, create_user_song_table, create_user_session_table]
insert_data_queries = [session_table_insert, user_session_table_insert, user_song_table_insert]
drop_table_queries = [drop_session_table, drop_user_song_table, drop_user_session_table]
