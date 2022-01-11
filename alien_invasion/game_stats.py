class GameStart:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_start()
        self.game_active = False
    def reset_start(self):
        self.ships_left = self.settings.ship_limit