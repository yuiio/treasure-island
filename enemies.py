class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class OldPirate(Enemy):
    def __init__(self):
        self.name = "Le vieux pirate"
        self.hp = 30
        self.damage = 20
        self.is_at_home = False
        self.is_drunk = False
        self.story = 0
        self.stories = [
        "Je sais juste qu'aprés la traversée de la riviére en bas du canyon, t'as tous ces maudits damnés pirates morts de la terre entière qu'attendent pour te faire regretter d'exister tellement y vont te faire mal espèce d'Olibrius !\n\nSi t'as pas le talisman de Barbe Noir pour contrer c'te malédiction c'est même pas la peine d'essayer. Moi, je l'ai jamais trouvé, c'est pour ça que je suis toujours ici, nom d'une pipe en terre !",

        "Je sais juste que si t'as la mauvaise idée de passer la rivière sur le pont, t'as intêret à avoir une lame qui coupe bien pour transformer en tartare ce nid de vampires ailés à tour de bras, mousaillon !\n\nY'a que Barbe Noire qui avait un sabre assez solide et léger. Il l'a laissé sur cette île tout juste après avoir planqué son magot, c'te vielle carne ! Je le cherche toujours nom d'un #@!? décérébré !",

        "Et c'est pas faute d'avoir essayé, j't'l dit espèce d'alburostre ! Mousaillon, juste une petite question si tu traîne au nord de l'île : j'espère que t'es pas archnophobe !\n\nAh ! Ah ! ah hha ah ah graglll grmmmf ... ronnnfle zzzzz"
        ]

    def tell_story(self):
        txt = "«Merci pour le rhum l'ami ...\nEt même je vais te dire que, aaah Sacrebleu !, je l'ai vu ce maudit trésor !\nMais en plus de mes dents je perds la boule aussi, j'suis trop vieux. Je m'rappelle plus où il est...\n\n{}»\n\nAprès ces paroles le pirate sombra dans un profond comas éthylique...".format(self.stories[self.story])
        if self.story < len(self.stories)-1:
            self.story += 1
        else:
            self.story = 0
        return txt

class Jaguar(Enemy):
    def __init__(self):
        self.name = "Jaguar"
        self.hp = 40
        self.damage = 30

class BlackCaiman(Enemy):
    def __init__(self):
        self.name = "Caïman noir"
        self.hp = 40
        self.damage = 15

class Anaconda(Enemy):
    def __init__(self):
        self.name = "Anaconda"
        self.hp = 20
        self.damage = 10

class Spider(Enemy):
    def __init__(self):
        self.name = "Tarentule"
        self.hp = 5
        self.damage = 15

class BatColony(Enemy):
    def __init__(self):
        self.name = "Colonie de chauves-souris vampire"
        self.hp = 200
        self.damage = 7

class LivingDeads(Enemy):
    def __init__(self):
        self.name = "Horde de pirate morts-vivants"
        self.hp = 100
        self.damage = 30

class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Araignée géante"
        self.hp = 30
        self.damage = 15
