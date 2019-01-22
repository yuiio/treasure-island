class Item():
    """The base class for all items"""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return """
    {}
    ----
    {}
    """.format(self.name, self.description)


class Weapon(Item):
    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)

    def __str__(self):
        return """
    {}
    ----
    {}
    dégats: {}
    """.format(self.name, self.description, self.damage)


class RhumFlask(Item):
    def __init__(self):
        super().__init__(name="Flasque de Rhum",
                         description="En cas de coup de mou uniquement...")

class BlackBearTalisman(Item):
    def __init__(self):
        super().__init__(name="Talisman de Barbe Noire",
                         description="Éloigne les créatures surnaturelles")

class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dague",
                         description="Pour le corps à corps",
                         damage=5)


class PirateMusket(Weapon):
    def __init__(self):
        super().__init__(name="Mousquet de pirate",
                         description="Puissant mais lent",
                         damage=20)

class BlackBeardSword(Weapon):
    def __init__(self):
        super().__init__(name="Sabre de Barbe Noire",
                         description="Léger et très tranchant; permet d'avancer " \
                         "plus vite dans la jungle",
                         damage=15)




