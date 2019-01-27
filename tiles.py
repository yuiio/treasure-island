import random

import actions, enemies, items, world

# TODOS
# DONE refactoriser ennemi modify_player
# DONE Remplacer fuite par repli arrière ( attention pour le cas du pont )
# DONE Boire trop de rhum diminue les performances au combat  ébriété
# DONE Une map
# Interface avec curse

# pont et riviere : revoir traversée  + texte
# dans game.py room.visited plante quand le pont casse


# npc qui se retrouve sur plusieurs tiles
old_pirate = enemies.OldPirate()

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def intro_text(self, player):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def can_move_here(x, y):
        tile = world.tile_at(x, y)
        if tile and not getattr(tile, 'broken', False):
            return tile
        return None

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if MapTile.can_move_here(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if MapTile.can_move_here(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if MapTile.can_move_here(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if MapTile.can_move_here(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves


    def flee_moves(self):
        """Tous les mouvements permis en cas de fuite"""
        moves = []
        tile = MapTile.can_move_here(self.x + 1, self.y)
        if tile and not isinstance(tile, LeavingTile):
            moves.append(actions.MoveEast())
        tile = MapTile.can_move_here(self.x - 1, self.y)
        if tile and not isinstance(tile, LeavingTile):
            moves.append(actions.MoveWest())
        tile = MapTile.can_move_here(self.x, self.y - 1)
        if tile and not isinstance(tile, LeavingTile):
            moves.append(actions.MoveNorth())
        tile = MapTile.can_move_here(self.x, self.y + 1)
        if tile and not isinstance(tile, LeavingTile):
            moves.append(actions.MoveSouth())
        return moves


    def available_actions(self):
        """Returns all of the available actions in this room."""
        pos_actions = self.adjacent_moves()
        pos_actions.append(actions.DrinkRhum())
        pos_actions.append(actions.ViewInventory())
        pos_actions.append(actions.ViewMap(world.world_map))

        return pos_actions

    def __repr__(self):
        return type(self).__name__

class NeutralTile(MapTile):
    """
    For dev only
    """
    def intro_text(self, player):
        return """
        Rien de spécial ici...
        Coord. : x{} y{}
        """.format(self.x, self.y)

    def modify_player(self, player):
        pass



class StartingTile(MapTile):
    def intro_text(self, player):
        return """
        Vous êtes à l'endroit où vous avez acosté sur l'île. Derrière vous
        clapote sur l'eau votre chaloupe qui vous permettra de regagner votre
        navire ancré plus au large.
        """

    def modify_player(self, player):
        pass


class BeachTile(MapTile):
    def intro_text(self, player):
        return """
        Vous êtes sur la plage. Juste du sable fin à perte de vue
        et quelques coquillages.
        """

    def modify_player(self, player):
        pass


class JungleTile(MapTile):

    def intro_text(self, player):
        if player.has_sword:
            return """
        Vous progressez rapidement dans cette chaleur dense et humide en vous
        frayant un chemin à grand coup de sabre dans la végétation luxuriantes.
        """
        else:
            return """
        Vous vous enfoncez dans un jungle épaisse. La chaleur y est étouffante
        et les moustiques pulullent ... si seulement vous pouviez les semer.

        Toutes ces piqûres vous font perdre 2 points de vie...
        """

    def modify_player(self, player):
        # Les moustiques retirent des HP si le joueur n'a pas le sabre pour
        # progresser rapidemment
        if not player.has_sword:
            player.hp -= 2


class PirateTile(MapTile):

    def __init__(self, x, y):

        if old_pirate is None:
            raise NotImplementedError("OldPirate doesn't exist...")
        self.first_time = True
        super().__init__(x, y)

    def modify_player(self, player):

        if not old_pirate.is_at_home and old_pirate.is_alive() and not self.first_time:
            player.hp = player.hp - old_pirate.damage
            self.first_time = False
            return """
        Le vieux pirate vous inflige {} de dégat.
        Il vous reste {} points de vie.
        """.format(old_pirate.damage, player.hp)
        self.first_time = False

    def intro_text(self, player):
        if not self.is_here:
            return self.not_here_txt
        else:
            if old_pirate.is_alive():
                if not old_pirate.is_drunk:
                    return self.alive_txt
            else:
                return self.dead_txt

    def negociate(self, player):
        raise NotImplementedError()

    @property
    def is_here(self):
        raise NotImplementedError()



class OldPirateTile(PirateTile):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.alive_txt = """
        Un vieux pirate édenté à l'air un peu fou surgit devant vous en
        tournoyant son sabre furieusement au dessus de sa tête.

        «T'es qui Forband ! Je vais te découper en rondelle de mortadelle espèce
        de Sapajou des plages !»
        """

        self.dead_txt = """
        Le vieux pirate git devant vos pieds. Vous vous demandez encore depuis
        combien de temps survivait-il seul sur cette île maudite ?

        De toute manière, c'est définitivement terminé pour lui désormais...
        """

        self.not_here_txt = """
        Vous vous enfoncez dans un jungle épaisse. La chaleur y est étouffantes
        et les moustiques pulullent.
        """

    def negociate(self, player):
        if player.offer_rhum():
            old_pirate.is_at_home = True
            return """
        Vous offrez une flasque de rhum.

        «Ahhhhh ! Si tu me prends par les sentiments ça change tout...» dit
        le vieux pirate.

        Il s'immobilise d'un coup en regardant nerveusement
        à droite et à gauche. Prenant ses jambes à son coup, le vieux pirate
        disparait dans la jungle avec votre rhum en hurlant:

        «Rentre chez toi pendant qu'il est encore temps, mousaillon !»
                """
        else:
            return """
        Damned ! Vous n'avez plus de rhum à partager. Cela n'aide pas à délier
        les langues.

        «C'est tout ce que tu as dans le ventre orchidoclaste !?» réponds le
        vieux pirate.
                """

    @property
    def is_here(self):
        return not old_pirate.is_at_home

    def available_actions(self):
        if old_pirate.is_alive() and self.is_here and not old_pirate.is_drunk:
            return [actions.Attack(enemy=old_pirate),
                    actions.Negociate(tile=self),
                    actions.Flee(tile=self)]
        else:
            old_pirate.is_drunk = False
            return super().available_actions()



class HutOldPirateTile(PirateTile):
    def __init__(self, x, y):

        super().__init__(x, y)

        self.alive_txt = """
        Le vieux pirate est assis sous sa cabane en chaume de palmier.
        L'oeil vitreux, il vous jette un regard pas franchement droit.

        «Par saint Couillebeau ! Je te reconnais toi... t'aurais pas un petit
        coup de rhum pour le vieux Chuky ?»
        """

        self.dead_txt = """
        Le vieux pirate est étendu par terre au milieu de bouteilles vides et
        vous vous demandez si ce vieux fou n'aurait finalement pas pu vous être
        utile ?

        De toute évidence, vous ne le saurait jamais...
        """

        self.not_here_txt = """
        Cette cabane au beau milieu de la jungle bien qu'elle soit vide, montre
        qu'elle est actuellement habité.
        Des flasques vides de ruhm jonchent le sol; le propriétaire de la hutte
        semble aimer le rhum de maninière immodérée.
        """

    def negociate(self, player):
        if player.offer_rhum():
            old_pirate.is_drunk = True
            return old_pirate.tell_story()
        else:
            return """
        Damned ! Vous n'avez plus de rhum. Cela n'aide pas à délier les langues.

        «Va au diable coprolithe de bac à sable !» vous dit le vieux pirate.
                """


    @property
    def is_here(self):
        return old_pirate.is_at_home

    def available_actions(self):
        if old_pirate.is_alive() and self.is_here and not old_pirate.is_drunk:
            possible_actions = super().available_actions()
            # possible_actions.append(actions.Attack(enemy=old_pirate))
            possible_actions.append(actions.Negociate(tile=self))
            return possible_actions
        else:
            old_pirate.is_drunk = False
            return super().available_actions()


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.Spider()
            self.alive_text = """
        Une tarentule tombe d'un arbre sur votre bras.
        Elle est trés agressive.
        """
            self.dead_text = """
        Le corps de l'araignée n'est plus qu'un informe tas de tissus
        organiques. Vous avez horreur d'être surpris par ces bestioles...
        """
        elif r < 0.80:
            self.enemy = enemies.Anaconda()
            self.alive_text = """
        Un anaconda vous met un puissant coup de tête qui vous sonne et tente
        de s'enrouler autour de vous pour vous étouffer.
        """
            self.dead_text = """
        L'anaconda git au sol complètement flasque.
        """
        elif r < 0.95:
            self.enemy = enemies.BlackCaiman()
            self.alive_text = """
        Surgissant de nul part un énorme caïman noir vous barre la route,
        la gueule grande ouverte !
        """
            self.dead_text = """
        Le gros reptile inerte vous rappelle l'âpre combat qui a été nécessaire
        pour rester en vie tout entier.
        """
        else:
            self.enemy = enemies.Jaguar()
            self.alive_text = """
        Un jaquar, roi de la jungle, bondit d'un arbre et se poste juste devant
        vous. Il vous scrute de ses yeux jaunes et son rugissement vous glace la
        moelle épinière; il est très affamé...
        """
            self.dead_text = """
        Vaincu, l'énorme félin a trépassé. Si il n'était pas lourd vous l'auriez
        ramené pour récupérer sa peau.
        """

        super().__init__(x, y)

    def intro_text(self, player):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def fight_player(self, player, damage):
        player.hp = player.hp - damage
        if player.hp < 0:
            player.hp = 0
        return """
        Cet ennemi vous inflige {} points de dégats.
        Il vous reste {} points de vie.
        """.format(damage, player.hp)

    def modify_player(self, player):
        if self.enemy.is_alive():
            return self.fight_player(player, self.enemy.damage)

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.DrinkRhum()]
        else:
            return super().available_actions()

class FindTile(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)
        return "Vous prenez :\n{}".format(self.item)

    def modify_player(self, player):
        return self.add_loot(player)

class LootTile(FindTile):
    def __init__(self, x, y, item):
        self.loot_claimed = False
        super().__init__(x, y, item)

    def modify_player(self, player):
        if not self.loot_claimed:
            self.loot_claimed = True
            return super().modify_player(player)

class FindRhumTile(FindTile):
    def __init__(self, x, y):
        super().__init__(x, y, items.RhumFlask())

    def intro_text(self, player):
        return """
        Vous trouvez une vieille caisse remplie de flasques de rhum.
        «Ça se conserve bien c'te bonne chose là !»
        """

class FindTalisamanTile(LootTile):
    def __init__(self, x, y):
        super().__init__(x, y, items.BlackBearTalisman())

    def intro_text(self, player):
        if self.loot_claimed:
            return """
        La végétation est si dense qu'il est impossible d'aller plus loin.
        """
        else:
            player.has_talisman = True
            return """
        Votre oeil est attiré par quelque chose de brillant au sol.
        En écartant prudemment le feuillage vous découvrez un talisman rond. Des
        inscriptions rhuniques incompréhensibles pour vous sont gravées sur le
        cercle de métal au centre duquel est certi un énorme rubis. Cet objet à
        l'air très ancien. En le ramassant vous sentez qu'il est habité par une
        puissante magie ancestrale.
        """

class FindSwordTile(LootTile):
    def __init__(self, x, y):
        super().__init__(x, y, items.BlackBeardSword())

    def intro_text(self, player):
        if self.loot_claimed:
            return """
        Un vieux squelette à moitié recouvert de mousse est adossé à un tronc
        d'arbre.
        """
        else:
            return """
        Planté dans un squelette vous trouvez un sabre qui étrangement n'est
        absolument pas rouillé.
        Vous le prenez en main : léger et vif comme l'éclair, tranchant comme un
        rasoir. Vous décidez de le garder apparement il manque à personne.
        """

    def modify_player(self, player):
        if not self.loot_claimed:
            player.has_sword = True
        return super().modify_player(player)

class WarningTile(MapTile):

    def intro_text(self, player):
        if self.x < 2: # Avertissement chemin ouest
            return """
        Vous arrivez en bas du canyon. Si vous décidez de continuer votre
        chemin en direction du nord vous allez devoir traverser le lit
        d'une riviére relativement large. Vous essayez d'évaluer la force du
        courant et scruter les tourbillons occasionnant des remous.
            """
        else: # Avertissement chemin est
            return """
        Vous arriver en haut du canyon. Au nord se trouve un pont qui permet
        de passer au dessus d'une rivière en contre bas.
        Vous examinez attentivement l'état des lianes et des planches
        pour évaluer la solidité du pont.
        On dirait que le vent se lève doucement, un léger ballant anime ce chemin
        suspendu...
        """

    def modify_player(self, player):
        pass

class RiverTile(MapTile):

    def intro_text(self, player):
        return """
        Vous vous engagez dans la rivière. Vous avez de l'eau jusqu'au genou.
        Un étrange sentiment vous traverse.
        C'est comme si la rivière semblait vivante. Le courant de l'eau varie
        en permanence en fonction de son humeur...
        """

    def modify_player(self, player):
        r = random.random()
        if r < 0.50:
            return """
        Vous vous dépêchez de nager avant qu'il ne vous arrive malheur.
            """
        elif r < 0.80:
            player.hp -= 10
            return """
        Le courant était si fort que vous avez failli vous noyer. En crachant
        de l'eau, vous essayez de reprendre votre souffle malgré les remous.
        Vous ne vous attardez pas car vous êtes pressez de rejoindre la rive.

        Cet effort colossal vous coûte 10 points de vie.
            """
        elif r < 0.95:
            player.hp -= 30
            return """
        Entrainez par un tourbillon, votre tête cogne un rocher au fond de la
        rivière. Le front ensanglanté votre vue se brouille et la douleur vous
        lance. Vous allez chercher loin vos dernières forces pour vite rejoindre
        la berge. C'est miracle que vous n'ayez pas perdu connaissance.

        Vous perdez 30 points de vie.
            """
        else:
            player.hp -= 50
            return """
        En plein milieu de la rivière, vous tombez sur un banc de piranhas.
        À croire qu'ils attendaient pour être sûr que vous ne pourriez pas faire
        marche arrière. L'eau se colore de votre sang ...

        ... et vous perdez 50 points de vie.
            """


class BridgeTile(MapTile):

    def __init__(self, x, y):
        self.broken = False
        super().__init__(x, y)

    def intro_text(self, player):
        return """"
        Vous commencez la traversée du pont. Arrivé à mi-chemin vous commencez à
        vous demander si cela était une bonne idée. Les planchettes on vraiment
        l'air bien vermoulues ...
        """

    def modify_player(self, player):
        r = random.random()
        if r < 0.50:
            return """
        ... mais finalement vous être trop content de constater que vous allez
        pouvoir utiliser le pont sans dificulté.
            """
        elif r < 0.80:
            return """
        Le vent se léve et vous perdre l'équilibre. Vous basculez dans le vide
        et réussissez in extremis à vous rattraper d'une main.
        Avec beaucoup d'énergie vous réussissez à vous hisser de nouveau sur le
        pont...

        Cet effort colossal vous coûte 10 points de vie.
            """
            player.hp -= 10
        elif r < 0.95:
            if player.has_sword:
                return """
        Une planchette pourrie céde. Par réflexe vous vous aggripez
        aux lianes des deux mains pour ne pas tomber dans le vide. Dans votre
        précipitation vous lâcher votre sabre.

        Votre regard le suit jusqu'à ce qu'il transperce la surface de la
        rivière.
                """
                for i in player.inventory:
                    if isinstance(i, items.BlackBeardSword ):
                        player.inventory.remove(i)
                player.has_sword = False
            else:
                return """
        Le pont céde sous votre propre poids. Vous tombez dans la rivière juste
        au beau milieu d'un banc de pirahnas. L'adrénaline décuple vos forces et
        vous nagez comme un fou pour vous rattrapez à une liane pendante du
        pont. Votre orteil qui vient d'être grignoté ne vous facilite pas la
        remontée sur les plances. Vous maudissez ce vieux pont en tentant de
        stopper l'hémoragie avec un bout de tissu que vous déchirez de votre
        chemise.

        C'était la dernière fois que ce pont transportait quelqu'un.

        Vous perdez 30 points de vie.
            """
                player.hp -= 30
                self.broken = True
        else:

            return """
        Le pont est trop vieux et pourri pour supporter votre poid.
        Vous vous accrochez aux lianes devant vous, et dans un grand mouvement
        circulaire, vous vous fracassez la tête contre la paroi du canyon.
        Vous perdez une dent. La bouche ensanglantée vous finissez par remonter
        comme vous pouvez pour finir votre chemin.

        C'était la dernière fois que ce pont transportait quelqu'un.

        Vous perdez 50 points de vie.
            """
            player.hp -= 50
            self.broken = True


class LivingDeadTile(EnemyTile):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemy = enemies.LivingDeads()
        self.alive_text = """
        Une horde de pirates morts-vivants vous assaille. Vous comprenez que
        Barbe Noire n'avait pas choisi cette île au hasard pour protéger son
        trésor ... Toutes les âmes des plus vils mécréants que les océans aient
        portés errent ici en attendant de trouver un jour peut-être le repos.
        """
        self.dead_text = """
        Seuls quelques os témoingnent de l'âpre bataille que vous avez mené ici.
        Les âmes hantés qui animaient les morts semblent avoir été rappelées
        ailleurs.
        """

    def modify_player(self, player):
        if self.enemy.is_alive():
            damage = self.enemy.damage
            feedback = ""
            if player.has_talisman:
                feedback += """
        Heureusement pour vous, le talisman que vous avez trouvé vous protège
        des puissances maléfiques. Les forces de vos assaillants sont cinq fois
        plus faible.
                """
                damage /= 5
            feedback += super().fight_player(player, int(damage))
            return feedback


class BatsTile(EnemyTile):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemy = enemies.BatColony()
        self.alive_text = """
        Soudainement le ciel s'assombrit. Vous réalisez au bout d'un seconde
        qu'une colonie de chauves-souris vampires virvoltent autour de vous.
        À peine avez-vous saisi votre armes qu'une multitude de bestioles ailées
        foncent sur vous. Vous vous dîtes que Barbe Noire savait qu'elles
        défendraient son précieux butin pour lui.
        """
        self.dead_text = """
        Les cadavres par centaines de chiroptères qui jonchent le sol et aussi
        les morsures sur tout votre corps vous rappelle l'épuisant combat que
        vous avez mené contre ces mini-vampire ailés.
        """
        self.first_time = True # La premiere fois que le joueur arrive ici

    def modify_player(self, player):

        if self.first_time:
            # Contre les chauves-souris le mousquet de pirate est trop lent
            # à recharger... Ici le sabre va devenir un avantage
            # et le mousquet un handicap contre cet ennemi.
            musket = self.get_weapon(player, items.PirateMusket)
            musket.damage = 2
            if player.has_sword:
                sabre = self.get_weapon(player, items.BlackBeardSword)
                sabre.damage = 25
            self.first_time = False

        if self.enemy.is_alive():
            feedback = ""
            if player.has_sword:
                feedback += """
        Vous êtes vraiment content d'avoir trouvé ce sabre dans la jungle. Sans
        lui vous n'auriez aucune chance contre cette foule volante aussi dense.
        Certainement qu'il a du appartenir à Barbe Noire lui-même, sans quoi il
        ne serait jamais arrivé ici lui aussi.
                """
            else:
                feedback += """
        Une angoisse vous saisie : avec juste un mousquet de pirate si lent à
        recharger et une dague, vous vous dîtes que cela va être compliqué de
        faire face à ce nuage de chauves-souris sanguinaire...
                """
            feedback += super().fight_player(player, self.enemy.damage)
            return feedback
        else:
            # Le combat est terminé on restaure les armes à leur valeur initiale
            musket = self.get_weapon(player, items.PirateMusket)
            musket.damage = 20
            if player.has_sword:
                sabre = self.get_weapon(player, items.BlackBeardSword)
                sabre.damage = 15

    def get_weapon(self, player, weapon_type):
        for item in player.inventory:
            if isinstance(item, weapon_type ):
                return item
        return None


class LeavingTile(EnemyTile):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemy = enemies.GiantSpider()
        self.alive_text = """
        D'après votre carte le trèsor se trouve à quelque pas juste devant vous.
        Vous apercevez une sorte de grotte dans le renfoncement de la roche dont
        l'entrée semble dissimulée par un vieux voile gris.

        En vous approchant vous réalisez que ce voile n'est autre que...
        Trop tard ! Les vibrations sur cette gigantesque toile d'araignée ont
        alertée sa propriétaire !

        Une gigantesque araignée vous saute dessus et commence à vous engluer de
        toile particulièrement collante. Vous esquivez de justesse sa tentative
        de morsure fatale.
        """
        self.dead_text = """
        La toile géante est complétement déchirée après les derniers moments de
        combat de l'araignée géante.

        La vision de ce corps poilu à huit pattes vous glace d'effroi. Malgré
        le fait que vous savez avoir tué ce monstre, vous le contournez sans
        même oser y toucher.
        """

    def modify_player(self, player):
        if self.enemy.is_alive():
            return super().fight_player(player, self.enemy.damage)
        else:
            player.victory = True
            return """
        Vous pénétrez dans la cavité rocheuse heureusement peut profonde. Le peu
        de lumière suffit pour entrevoir un vieux coffre qui semble dormir ici
        depuis des siècles recouvert pour une couverture de toile d'araignée.

        D'un coup de caillou vous défoncez le cadenas complètement rouillé
        de ce vieux coffre . Votre visage est illuminé par le reflet de la

        ... vous avez réussi là où tous les autres ont échoués et finis
        par rejoindre la horde de morts-vivants qui hantent cette île maudite.

        Vous rebroussez très prudemment chemin en suivants vos pas
        jusqu'à votre navire.


        VICTOIRE ! Le trèsor de barbe noire est désormais votre.
        """
