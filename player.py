import random
import items

class Player():
    def __init__(self, starting_position):
        self.inventory = [
            items.PirateMusket(),
            items.Dagger(),
            items.RhumFlask()]
        self.hp = 100
        self.x, self.y = starting_position
        self.victory = False
        self.has_sword = False
        self.has_talisman = False
        self.drunkness = 0
        self.flee_move = None

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print("""
    Inventaire :
    """)
        for item in self.inventory:
            print(item)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)
        self.flee_move = self.move_south

    def move_south(self):
        self.move(dx=0, dy=1)
        self.flee_move = self.move_north

    def move_east(self):
        self.move(dx=1, dy=0)
        self.flee_move = self.move_west

    def move_west(self):
        self.move(dx=-1, dy=0)
        self.flee_move = self.move_east

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("""
        Vous utilisez {} contre {} !
        """.format(best_weapon.name, enemy.name), end="")
        damage = self.get_drunk_damage(best_weapon.damage)
        if self.drunkness > 0:
            print("""
        (Vous avez un malus de -{} de dégats à cause du rhum...)
        """.format(best_weapon.damage - damage), end="")
        enemy.hp -= damage
        if not enemy.is_alive():
            print("""
        Vous avez tué {} !
        """.format(enemy.name))
        else:
            print("""
        {} a {} points de vie.
        """.format(enemy.name, enemy.hp))

    def get_drunk_damage(self, damage):
        """Calcul les dégats d'une arme en fonction de l'alcolémie du joueur"""
        d = min(5, round(self.drunkness)) # On fixe le taux maximum à 5
        return int(round((damage/5)*(5-d)))

    def has_rhum(self):
        for i in self.inventory:
            if isinstance(i, items.RhumFlask):
                return i
        return None

    def offer_rhum(self):
        rhum = self.has_rhum()
        if rhum is not None:
            self.inventory.remove(rhum)
            print("""
        Vous offrez une flasque de rhum.
        """)
            return True
        else:
            print("""
        Damned ! Vous n'avez plus de rhum. Cela n'aide pas à délier les langues.
        """)
            return False

    def drink_rhum(self):
        rhum = self.has_rhum()
        if rhum is not None:
            self.inventory.remove(rhum)
            if self.drunkness < 1:
                print("""
        Les pirates ça tournent au ruhm.
        Rien de tel qu'un petit remontant pour prendre des forces !
        Vous récupérez 20 points de vie.
        """)
                self.hp += 20
            elif self.drunkness < 3:
                print("""
        «Allez encore une petite lampée pour la route !»
        Vous récupérez 5 points de vie.
        """)
                self.hp += 5
            elif self.drunkness < 4:
                print("""
        «Râaallez 'core une ch'tite rampée pour la loute !»
        """)
            elif self.drunkness < 5:
                print("""
        «Encore le dernier de les derniers et après je va allé»
        Votre foie commence à saturé. Vous perdez 5 points de vie.
        """)
                self.hp -= 5
            elif self.drunkness >=5:
                drunk_damage = int(round(self.drunkness * 3))
                print("""
        Vous vomissez partout.
        Vous perdez {} points de vie.
        """.format(drunk_damage))
                self.hp -= drunk_damage
            self.drunkness += 1
        else:
            print("""
        Bon sang ! Vous n'avez plus de rhum.
        """)

    def negociate(self, tile):
        tile.negociate(self)

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        # available_moves = tile.flee_moves()
        # r = random.randint(0, len(available_moves) - 1)
        # self.do_action(available_moves[r])

        """Go back to previous place !"""
        available_moves = tile.flee_moves()
        flee_success = False
        for move in available_moves:
            if self.flee_move.__name__ == move.method.__name__:
                self.flee_move()
                flee_success = True
                break

        if not flee_success:
            print("""
        Pas de fuite en arrière possibe !
        """)

    def print_map(self, world_map):
        print("""
Carte :
    N
    ↑
 O ←✛→ E
    ↓
    S
""")
        for y, row in enumerate(world_map):
            line = ["        "]
            print_empty = False
            for x, tile in enumerate(row):
                if x == self.x and y == self.y:
                    line.append("X")
                elif tile is not None:
                    if getattr(tile, 'broken', False):
                        line.append(" ")
                        print_empty = True
                    elif tile.visited:
                        line.append(".")
                    else:
                        line.append(" ")
                else:
                    line.append(" ")
            out_line = " ".join(line)
            if "." in out_line or "X" in out_line or print_empty:
                print(out_line)

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

