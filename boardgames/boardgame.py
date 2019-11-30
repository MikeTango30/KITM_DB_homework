class boardgame:

    def __init__(self, boardgame_id, publisher_id, boardgame_title, year_released, selling_price, min_players,
                 max_players, playing_time, age_from, printed_quantity, printing_price):
        self.boardgame_id = boardgame_id
        self.publisher_id = publisher_id
        self.boardgame_title = boardgame_title
        self.year_released = year_released
        self.selling_price = selling_price
        self.min_players = min_players
        self.max_players = max_players
        self.playing_time = playing_time
        self.age_from = age_from
        self.printed_quantity = printed_quantity
        self.printing_price = printing_price
