from player import Player

class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)

class MoveNorth(Action):
    def __init__(self):
        super().__init__(method=Player.move_north, name='Aller au nord', hotkey='n')


class MoveSouth(Action):
    def __init__(self):
        super().__init__(method=Player.move_south, name='Aller au sud', hotkey='s')


class MoveEast(Action):
    def __init__(self):
        super().__init__(method=Player.move_east, name='Aller à l\'est', hotkey='e')


class MoveWest(Action):
    def __init__(self):
        super().__init__(method=Player.move_west, name='Aller à l\'ouest', hotkey='o')


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='Inventaire', hotkey='i')


class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attaquer", hotkey='a', enemy=enemy)


class Negociate(Action):
    def __init__(self, tile):
        super().__init__(method=Player.negociate, name="Discuter", hotkey='d', tile=tile)


class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Fuir", hotkey='f', tile=tile)


class DrinkRhum(Action):
    def __init__(self):
        super().__init__(method=Player.drink_rhum, name='Boire', hotkey='b')


class ViewMap(Action):
    """Prints the map with payer position"""
    def __init__(self, world_map):
        super().__init__(method=Player.print_map, name='Carte', hotkey='c', world_map=world_map)
