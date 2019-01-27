from player import Player
import world

class Game:

    begin_text = """
        Durant une nuit festive à Port-Royal, vous avez gagné aux jeux une carte
        maritime au fin fond d'une taverne à l'atmosphère si alcolisée que tout
        le monde est saoul avant même d'avoir commandé son premier verre de
        rhum. En effet votre adversaire de table n'était autre que
        "Pimflick jambe de bois", le dernier membre vivant de l'équipage de
        "Barbe noire" le célèbre pirate qui écuma les mers des Caraïbes.
        Pimflick n'a pas eu d'autre choix que de vous donner sa carte pour
        honorer son pari perdu. Mauvais joueur qu'il est, c'est surtout votre
        mousquet sur son front qu'il l'a convaincu.
        "Va au diable, pauvre fou !", ce sont les dernières paroles que vous
        avez entendu en quittant la taverne.

        Grace à la carte de Pimflick, vous venez d'aborder l'île de la tortue,
        avec la ferme intention de découvrir et de ramener ...

        ... LE TRÉSOR DE BARBE NOIR !
        """

    player_death_text = """
        Vous venez de rejoindre la horde des pirates mort-vivants qui hantent
        cette île maudite qui jadis comme vous avaient eu le rêve fou de quitter
        ce lieu avec le trésor de Barbe Noire...

        Le pirate qui repartira vivant est, semble t-il, pas encore né !
        """

    def __init__(self):
        world.create_world()
        self.player = Player(world.starting_position)
        self.last_input = None

        print('[ BEGIN GAME ]')
        print(Game.begin_text)

    def run(self):
        while self.player.is_alive() and not self.player.victory:
            # room est l'endroit où le jouer se situe
            room = world.tile_at(self.player.x, self.player.y)
            room.visited = True
            print('[ INTRO TEXT ]')
            print(room.intro_text(self.player))

            # Le temps passant l'alcolémie du joueur passe
            if self.player.drunkness > 0 and self.last_input != "b":
                self.player.drunkness *= 0.85 if self.player.drunkness>0.5 else 0

            # Voir l'inventaire n'est pas considéré comme agissant dans le jeu
            if self.last_input != "i":
                print('[ MODIFY PLAYER ]')
                room.modify_player(self.player)

            if self.player.is_alive() and not self.player.victory:

                print('[ STATUS ]')
                print("Vos points de vie : {}".format(self.player.hp))
                if self.player.drunkness > 0:
                    print("Ébriété : {}".format(round(self.player.drunkness,2)))


                print('[ CHOICE ACTION ]')
                print("\nChoisir une action:\n")
                available_actions = room.available_actions()
                for action in available_actions:
                    print(action)

                correct_input = False
                while not correct_input:
                    action_input = input('\nAction: ')
                    for action in available_actions:
                        if action_input == action.hotkey:
                            print('[ PLAYER DO ACTION RESULT ]')
                            self.player.do_action(action, **action.kwargs)
                            correct_input = True
                            self.last_input = action.hotkey
                            break

        if not self.player.is_alive():
            print('[END GAME]')
            print(Game.end_text)




if __name__ == "__main__":
    game = Game()
    game.run()