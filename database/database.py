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
                                                        printed_quantity integer NOT NULL,
                                                        printing_price numeric NOT NULL,
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
                                                        publisher_name text NOT NULL
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
# boardgames
boardgame_tta = boardgame(None, None, 'Through The Ages: A New Story of Civilization', 2015, 65, 2, 4, 120, 14, 25000,
                          30)
gloomhaven = boardgame(None, None, 'Gloomhaven', 2017, 120, 1, 4, 120, 12, 50000, 60)
terraforming_mars = boardgame(None, None, 'Terraforming Mars', 2016, 60, 1, 5, 120, 12, 60000, 25)
rebellion = boardgame(None, None, 'Star Wars: Rebellion', 2016, 95, 2, 4, 240, 14, 120000, 40)
gaia = boardgame(None, None, 'Gaia Project', 2017, 110, 1, 4, 150, 12, 60000, 45)
scythe = boardgame(None, None, 'Scythe', 2016, 70, 1, 5, 115, 14, 70000, 35)
great_western_trail = boardgame(None, None, 'Great Western Trail', 2016, 60, 2, 4, 150, 12, 70000, 35)
arkham_horror = boardgame(None, None, 'Arkham Horror: The Card Game', 2016, 30, 1, 2, 120, 14, 90000, 12)
blood_rage = boardgame(None, None, 'Blood Rage', 2015, 95, 2, 4, 90, 14, 45000, 40)
imperial_assault = boardgame(None, None, 'Star Wars: Imperial Assault', 2014, 90, 2, 5, 120, 14, 150000, 55)
root = boardgame(None, None, 'Root', 2018, 50, 2, 4, 90, 10, 30000, 25)
crokinole = boardgame(None, None, 'Crokinole', 1876, 150, 2, 4, 30, 8, 200000, 75)

boardgames = [boardgame_tta, gloomhaven, terraforming_mars, rebellion, gaia, scythe, great_western_trail, arkham_horror,
              blood_rage, imperial_assault, root, crokinole]

# designers
designer_tta = designer(None, 'Vlaada', 'Chvatil')
designer_gloomhaven = designer(None, 'Isac', 'Childres')
designer_terraforming_mars = designer(None, 'Jacob', 'Fryxelius')
designer_rebellion = designer(None, 'Corey', 'Konieczka')
designer_gaia_1 = designer(None, 'Jens', 'DroegenMueller')
designer_gaia_2 = designer(None, 'Helge', 'Ostertag')
designer_scythe = designer(None, 'Jamey', 'Stegmeier')
designer_gwt = designer(None, 'Alexander', 'Pfister')
designer_arkham_1 = designer(None, 'Nate', 'French')
designer_arkham_2 = designer(None, 'Matthew', 'Newman')
designer_blood_rage = designer(None, 'Eric', 'M. Lang')
designer_imperial_assault_1 = designer(None, 'Justin', 'Kemppainen')
designer_imperial_assault_2 = designer(None, 'Jonathan', 'Ying')
designer_root = designer(None, 'Cole', 'Wehrle')
designer_crokionle = designer(None, '(Uncredited)', '(Uncredited)')

designers = [designer_tta, designer_gloomhaven, designer_terraforming_mars, designer_rebellion, designer_gaia_1,
             designer_gaia_2, designer_scythe, designer_gwt, designer_arkham_1, designer_arkham_2, designer_blood_rage,
             designer_imperial_assault_1, designer_imperial_assault_2, designer_root, designer_crokionle]

# artists
artist_tta_1 = artist(None, 'Filip', 'Murmak')
artist_tta_2 = artist(None, 'Radim', 'Pech')
artist_gloomhaven_1 = artist(None, 'Alexander', 'Elichev')
artist_gloomhaven_2 = artist(None, 'Josh', 'T. McDowell')
artist_terraforming_mars = artist(None, 'Isaac', 'Fryxelius')
artist_rebellion_1 = artist(None, 'Matt', 'Allsopp')
artist_rebellion_2 = artist(None, 'David', 'Ardila')
artist_gaia = artist(None, 'Dennis', 'Lohausen')
artist_scythe = artist(None, 'Jakub', 'Rozalski')
artist_gwt = artist(None, 'Andreas', 'Resch')
artist_arkham_1 = artist(None, 'Christopher', 'Hosch')
artist_arkham_2 = artist(None, 'Marcin', 'Jakubowski')
artist_blood_rage_1 = artist(None, 'Henning', 'Ludvigsen')
artist_imperial_assault_1 = artist(None, 'Arden', 'Beckwith')
artist_imperial_assault_2 = artist(None, 'Christopher', 'Burdett')
artist_root = artist(None, 'Kyle', 'Ferrin')
artist_crokinole = artist(None, '(Uncredited)', '(Uncredited)')

artists = [artist_tta_1, artist_tta_2, artist_gloomhaven_1, artist_gloomhaven_2, artist_terraforming_mars,
           artist_rebellion_1, artist_rebellion_2, artist_gaia, artist_scythe, artist_gwt, artist_arkham_1,
           artist_arkham_2, artist_blood_rage_1, artist_imperial_assault_1, artist_imperial_assault_2, artist_root,
           artist_crokinole]

# publishers
publisher_tta = publisher(None, 'Czech Games Edition')
publisher_gloomhaven = (None, 'Cephalofair Games')
publisher_fryxgames = (None, 'FryxGames')
publisher_ffg = (None, 'Fantasy Flight Games')
publisher_feuerland = (None, 'Feuerland Spiele')
publisher_stonemeier = (None, 'Stonemeier Games')
publisher_gwt = (None, 'Eggert Spiele')
publisher_cmon = (None, 'CMON')
publisher_leder = (None, 'Leder Games')
publisher_public = (None, '(Public Domain)')

publishers = [publisher_tta, publisher_gloomhaven, publisher_fryxgames, publisher_ffg, publisher_feuerland,
              publisher_stonemeier, great_western_trail, publisher_cmon, publisher_leder, publisher_public]

# categories
category_tta = category(None, 'Strategy')
category_card_game = category(None, 'Card Game')
category_civilization = category(None, 'Civilization')
category_economic = category(None, 'Economic')
category_adventure = category(None, 'Adventure')
category_exploration = category(None, 'Exploration')
category_fighting = category(None, 'Fighting')
category_fantasy = category(None, 'Fantasy')
category_miniatures = category(None, 'Miniatures')
category_scifi = category(None, 'Science Fiction')
category_space_exploration = category(None, 'Space Exploration')
category_territory_building = category(None, 'Territory Building')
category_industry = category(None, 'Industry / Manufacturing')
category_environmental = category(None, 'Environmental')
category_movies = category(None, 'Movies / TV / Radio theme')
category_wargame = category(None, 'Wargame')
category_american_west = category(None, 'American West')
category_animals = category(None, 'Animals')
category_mythology = category(None, 'Mythology')
category_flicking = category(None, 'Flicking')

categories = [category_tta, category_card_game, category_civilization, category_economic, category_adventure,
              category_exploration, category_fighting, category_fantasy, category_miniatures, category_scifi,
              category_space_exploration, category_territory_building, category_industry, category_environmental,
              category_movies, category_wargame, category_american_west, category_animals, category_mythology,
              category_flicking]

# # field_to_update = 'boardgame_title'
# new_value = "Through the Ages: A New Story of Civilization"

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
