class Item():
    """The base class for all items"""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        # titled_name = self.name[0].upper() + self.name[1:]
        return "{}, {}".format(self.name, self.description)


class Weapon(Item):
    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)

    def __str__(self):
        # titled_name = self.name[0].upper() + self.name[1:]
        return "{}, {} (dégats: {})".format(
            self.name,
            self.description,
            self.damage)


class RhumFlask(Item):
    def __init__(self):
        super().__init__(name="une flasque de rhum",
                         description="en cas de coup de mou uniquement...")

class BlackBearTalisman(Item):
    def __init__(self):
        super().__init__(name="le talisman de Barbe Noire",
                         description="éloigne les créatures surnaturelles")

class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="dague",
                         description="pour le corps à corps",
                         damage=5)


class PirateMusket(Weapon):
    def __init__(self):
        super().__init__(name="mousquet de pirate",
                         description="puissant mais lent",
                         damage=20)

class BlackBeardSword(Weapon):
    def __init__(self):
        super().__init__(name="sabre de Barbe Noire",
                         description="léger et très tranchant; il permet d'avancer plus vite dans la jungle",
                         damage=15)




