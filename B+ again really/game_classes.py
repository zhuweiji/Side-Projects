from itertools import cycle  # for cyclical lists
import os
import random

# Player and Wheel classes are more or less complete but GameState class needs work
# need to incorporate a few player instances and change instance attributes (cash)
# but do with GameState methods or Player methods?
# GameState methods seem to be too many


class Player:
    """player class that is instanced for each player in game"""
    def __init__(self, name):
        self.name = str(name)
        self.cash = 0

    def return_cash(self):
        return self.cash

    def change_cash(self, change):
        if type(change) is int:
            return self.cash + change
        else:
            print(f'change in {self.name} cash is {change}')
            print('cash not changed')
            pass

    def bankrupt(self):
        self.cash = 0

    def __str__(self):
        return f'Player {self.name}'


class Wheel:
    """Wheel class to create one wheel object """
    SPIN_STRENGTH = (20, 100)

    def __init__(self):
        all_wheels = [i for i, filename in enumerate(os.listdir(os.path.join(os.getcwd(), 'misc', 'wheels')))]  # unused

        with open(os.path.join(os.getcwd(), 'misc', 'wheel_outcomes'), 'r') as f:
            wheel_outcomes = f.read().split(',')
            wheel_outcomes = (map(lambda x: int(x) if x.isdigit() else x, wheel_outcomes))

        self.states = {
            state: outcome for (state, outcome) in zip(all_wheels, wheel_outcomes)
        }
        self.state_cycle_object = cycle(all_wheels)
        self.current_position = next(self.state_cycle_object)

    def return_wheelposition(self):
        return self.current_position

    def return_outcome(self):
        return self.states[self.current_position]

    def next_position(self):
        self.current_position = next(self.state_cycle_object)
        return self.current_position

    def wheel_image_path(self):
        return str(self.current_position) + '.gif'


class GameState:
    DEFAULT_NUMPLAYERS = 3

    def __init__(self, numplayers=DEFAULT_NUMPLAYERS):
        with open(os.path.join(os.getcwd(), 'misc', 'Phrases.txt'), 'r') as f:
            phrase_list = f.read().split('\n')
            puzzle_phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
        self.puzzle_phrase = puzzle_phrase

        self.player_pool = cycle([Player(i+1) for i in range(numplayers)])
        self.current_player = next(self.player_pool)
        self.current_action = None
        self.wheel = Wheel()

    def next_player(self):
        self.current_player = next(self.player_pool)
        return self.current_player

    def current_playername(self):
        return self.current_player.name

    def curent_playercash(self):
        return self.current_player.cash

    def wheelposition(self):
        return self.wheel.return_wheelposition()

    def wheel_outcome(self):
        return self.wheel.return_outcome()

    def wheel_turn(self):
        return self.wheel.next_position()

    def wheel_spin(self):
        for i in range(random.randint(self.wheel.SPIN_STRENGTH)):
            self.wheel_turn()
        return self.wheelposition()


if __name__ == '__main__':
    game = GameState(2)
    print(game.current_player)
    print(game.wheelposition())
    print(game.puzzle_phrase)
