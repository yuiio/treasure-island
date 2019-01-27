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
        lines = ["""
    Inventaire :
    """]
        for item in self.inventory:
            lines.append(str(item))
        return '\n'.join(lines)

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

        feedback = ["""
        Vous utilisez votre {} contre : {} !
        """.format(best_weapon.name, enemy.name)]
        damage = self.get_drunk_damage(best_weapon.damage)
        if best_weapon.damage - damage > 0:
            feedback.append("""
        (Vous avez un malus de -{} de dégats à cause du rhum...)
        """.format(best_weapon.damage - damage))
        enemy.hp -= damage
        if not enemy.is_alive():
            feedback.append("""
        Vous avez tué : {} !
        """.format(enemy.name))
        else:
            feedback.append("""
        {} a {} points de vie.
        """.format(enemy.name, enemy.hp))
        return "\n".join(feedback)

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
            return True
        else:
            return False

    def drink_rhum(self):
        rhum = self.has_rhum()
        if rhum is not None:
            self.inventory.remove(rhum)
            if self.drunkness < 1:
                self.hp += 20
                feedback =  """
        Les pirates ça tournent au ruhm.
        Rien de tel qu'un petit remontant pour prendre des forces !
        Vous récupérez 20 points de vie.
        """
            elif self.drunkness < 3:
                self.hp += 5
                feedback =  """
        «Allez encore une petite lampée pour la route !»
        Vous récupérez 5 points de vie.
        """
            elif self.drunkness < 4:
                feedback =  """
        «Râaallez 'core une ch'tite rampée pour la loute !»
        """
            elif self.drunkness < 5:
                self.hp -= 5
                feedback =  """
        «Encore le dernier de les derniers et après je va allé»
        Votre foie commence à saturé. Vous perdez 5 points de vie.
        """
            elif self.drunkness >=5:
                drunk_damage = int(round(self.drunkness * 3))
                self.hp -= drunk_damage
                feedback =  """
        Vous vomissez partout.
        Vous perdez {} points de vie.
        """.format(drunk_damage)
            self.drunkness += 1
        else:
            feedback =  """
        Bon sang ! Vous n'avez plus de rhum.
        """
        return feedback

    def negociate(self, tile):
        return tile.negociate(self)

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
            return """
        Pas de fuite en arrière possibe !
        """

    def print_map(self, world_map):
        the_map = ["""
Carte :
    N
    ↑
 O ←✛→ E
    ↓
    S
"""]
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
                the_map.append(out_line)
        return "\n".join(the_map)

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            return action_method(**kwargs)

