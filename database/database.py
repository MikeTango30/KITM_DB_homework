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
# publisher -> game

# Many to Many
# designer_id, game_id          important info
# designer_id, publisher_id     important info
# designer_id, artist_id        not important info

# publisher_id, artist_id       not important info

# artist_id, game_id            not important info


# tables
table_boardgames = 'boardgames'
table_designers = 'designers'
table_artists = 'artists'
table_publishers = 'publishers'
table_categories = 'categories'

# queries for creating tables
create_table_games = """CREATE TABLE IF NOT EXISTS boardgames (
                                                        boardgame_id integer PRIMARY KEY,
                                                        publisher_id integer,
                                                        boardgame_title text NOT NULL UNIQUE,
                                                        year_released date NOT NULL,
                                                        selling_price numeric NOT NULL,
                                                        min_players integer NOT NULL,
                                                        max_players integer NOT NULL,
                                                        playing_time integer NOT NULL,
                                                        age_from integer NOT NULL,
                                                        FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
                                                        ON UPDATE CASCADE
                                                        )"""
create_table_designers = """CREATE TABLE IF NOT EXISTS designers (
                                                        designer_id integer PRIMARY KEY,
                                                        first_name text NOT NULL,
                                                        last_name text NOT NULL
                                                        )"""
create_table_publishers = """CREATE TABLE IF NOT EXISTS publishers (
                                                        publisher_id integer PRIMARY KEY,
                                                        publisher_name text NOT NULL,
                                                        printed_quantity integer NOT NULL,
                                                        printing_price numeric NOT NULL
                                                        )"""
create_table_artists = """CREATE TABLE IF NOT EXISTS artists (
                                                        artist_id integer PRIMARY KEY,
                                                        first_name text NOT NULL,
                                                        last_name text NOT NULL
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
                                                    category_id int,
                                                    FOREIGN KEY(boardgame_id) REFERENCES boardgames(boardgame_id),
                                                    FOREIGN KEY(designer_id) REFERENCES designers(designer_id),
                                                    FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id),
                                                    FOREIGN KEY(artist_id) REFERENCES artists(artist_id),
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


# db conn
def open_connection():
    connection = sqlite3.connect("boardgames.db")
    cursor = connection.cursor()

    return connection, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


def create_table(create_table_query):
    try:
        connection, cursor = open_connection()
        cursor.execute(create_table_query)
    except sqlite3.DatabaseError as error:
        print(error)
    finally:
        # noinspection PyUnboundLocalVariable
        close_connection(connection, cursor)


# crud
# -------
# helpers
def get_fields_for_where(entity):
    field_values = [attr + ' = (?)' for attr, value in entity.__dict__.items()]

    return field_values


def execute_query(sql_query, query_parameters, select=None):
    try:
        connection, cursor = open_connection()

        if select is None:
            cursor.execute(sql_query, query_parameters)
            connection.commit()
        if select:
            rows = [row for row in cursor.execute(sql_query, query_parameters)]
            return rows

    except sqlite3.DatabaseError as error:
        print(error)
    finally:
        # noinspection PyUnboundLocalVariable
        close_connection(connection, cursor)


def gather_parameters(entity):
    parameters = [value for attr, value in entity.__dict__.items()]

    return parameters


# query builders
def build_insert_query(entity, table_name):
    field_values = ['?' for field in range(len(entity.__dict__.items()))]  # !readable?
    insert_query = "INSERT INTO " + table_name + " VALUES(" + ', '.join(field_values) + ")"

    return insert_query


def build_select_query(entity, table_name):
    get_query = "SELECT * FROM " + table_name + " WHERE " + ' OR '.join(get_fields_for_where(entity)) + ""

    return get_query


def build_update_query(entity, table_name, field_to_update, new_value):
    new_value = "'" + new_value + "'"
    field_id = get_fields_for_where(entity)[0]
    update_query = "UPDATE " + table_name + " SET " + field_to_update + " = " + new_value + " WHERE " + field_id + ""

    return update_query


def build_delete_query(entity, table_name):
    field_id = get_fields_for_where(entity)[0]
    delete_query = "DELETE FROM " + table_name + " WHERE " + field_id + ""

    return delete_query


# c
def insert_entity(entity, table_name):
    execute_query(build_insert_query(entity, table_name), gather_parameters(entity))


# r
def get_entity(entity, table_name):
    return execute_query(build_select_query(entity, table_name), gather_parameters(entity), True)


# u
def update_entity(entity, table_name, field_to_update, new_value):
    update_query = build_update_query(entity, table_name, field_to_update, new_value)
    entity_id = [get_entity(entity, table_name)[0][0]]
    execute_query(update_query, entity_id)


# d
def delete_entity(entity, table_name):
    delete_query = build_delete_query(entity, table_name)
    entity_id = [get_entity(entity, table_name)[0][0]]
    execute_query(delete_query, entity_id)


# entries
boardgame_tta = boardgame(None, 1, 'Through the Ages: a new Story of Civilization', 2015, 65, 2, 4, 120, 14)
artist_tta_1 = artist(None, 'Filip', 'Murmak')
artist_tta_2 = artist(None, 'Radim', 'Pech')
designer_tta = designer(None, 'Vlaada', 'Chvatil')
publisher_tta = publisher(None, 'Czech Games Edition', 25000, 30)
category_tta = category(None, 'Strategy')

field_to_update = 'boardgame_title'
new_value = "Through the Ages: A New Story of Civilization"

# create tables
# for query in create_table_queries_list:
#     create_table(query)

# insert_entity(boardgame_tta, table_boardgames)
# insert_entity(artist_tta_1, table_artists)
# insert_entity(artist_tta_2, table_artists)
# insert_entity(designer_tta, table_designers)
# insert_entity(publisher_tta, table_publishers)
# insert_entity(category_tta, table_categories)

# print(get_entity(designer_tta, table_designers))
# update_entity(boardgame_tta, table_boardgames, field_to_update, new_value)
# delete_entity(artist_tta_2, table_artists)
