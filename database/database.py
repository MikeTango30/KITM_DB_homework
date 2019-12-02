import sqlite3
from boardgames.boardgame import boardgame
from boardgames.designer import designer
from boardgames.publisher import publisher
from boardgames.artist import artist
from boardgames.category import category


# Boardgames
#
# Game: boardgame_id, boardgame_title, year_released, selling_price, min_players, max_players, playing_time, age_from

# Designer: designer_id, first_name, last_name, birthdate

# Publisher: publisher_id, boardgame_id(FK), publisher_name, printed_quantity, printing_price

# Artist: artist_id, first_name, last_name, birthdate

# Categories: category_id, category_name


# One to many
# game -> publisher

# Many to Many
# designer_id, game_id          important info
# designer_id, publisher_id     important info
# designer_id, artist_id        not important info

# publisher_id, artist_id       not important info

# artist_id, game_id            not important info

create_table_games = """CREATE TABLE IF NOT EXISTS boardgames (
                                                        boardgame_id integer PRIMARY KEY,
                                                        boardgame_title text NOT NULL,
                                                        year_released date NOT NULL,
                                                        selling_price numeric NOT NULL,
                                                        min_players integer NOT NULL,
                                                        max_players integer NOT NULL,
                                                        playing_time integer NOT NULL,
                                                        age_from integer NOT NULL
                                                        )"""

create_table_designers = """CREATE TABLE IF NOT EXISTS designers (
                                                        designer_id integer PRIMARY KEY,
                                                        first_name text NOT NULL,
                                                        last_name text NOT NULL,
                                                        birthdate date NOT NULL
                                                        )"""

create_table_publishers = """CREATE TABLE IF NOT EXISTS publishers (
                                                        publisher_id integer PRIMARY KEY,
                                                        publisher_name text NOT NULL,
                                                        printed_quantity integer NOT NULL,
                                                        printing_price numeric NOT NULL,
                                                        FOREIGN KEY (boardgame_id) REFERENCES boardgames(boardgame_id)
                                                        ON UPDATE CASCADE
                                                        )"""
create_table_artists = """CREATE TABLE IF NOT EXISTS artists (
                                                        artist_id integer PRIMARY KEY,
                                                        first_name text NOT NULL,
                                                        last_name text NOT NULL,
                                                        birthdate date NOT NULL
                                                        )"""

create_table_category = """CREATE TABLE IF NOT EXISTS categories (
                                                        category_id integer PRIMARY KEY,
                                                        category_name text NOT NULL
                                                        )"""

create_table_junction = """CREATE TABLE IF NOT EXISTS junction (
                                                    boardgame_id int,
                                                    designer_id int,
                                                    publisher_id int,
                                                    artist_id int,
                                                    category_id int
                                                    FOREIGN KEY(boardgame_id) REFERENCES boardgames(boardgame_id)
                                                    FOREIGN KEY(designer_id) REFERENCES designers(designer_id)
                                                    FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
                                                    FOREIGN KEY(artist_id) REFERENCES artists(artist_id)
                                                    FOREIGN KEY(category_id) REFERENCES categories(category_id)
                                                    )"""


create_table_queries_list = [
                            create_table_games,
                            create_table_designers,
                            create_table_publishers,
                            create_table_artists,
                            create_table_category,
                            create_table_junction
                            ]


def open_connection():
    connection = sqlite3.connect("boardgames.db")
    cursor = connection.cursor()

    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_table(query):
    try:
        connection, cursor = open_connection()
        cursor.execute(query)
    except sqlite3.DatabaseError as error:
        print(error)
    finally:
        # noinspection PyUnboundLocalVariable
        close_connection(connection, cursor)


for query in create_table_queries_list:
    create_table(query)
