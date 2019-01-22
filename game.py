from player import Player
import world, enemies

intro_text = """
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

def play():

    print(intro_text)

    world.create_world()
    player = Player(world.starting_position)

    last_input = None

    # for damage in [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:
    #     print("{0:>3s}".format(str(damage)), end="")
    #     for drunkness in range(0, 6):
    #         print("{0:>3s}".format(str(player.get_damage(damage, drunkness))), end="")
    #     print("\n")


    while player.is_alive() and not player.victory:

        room = world.tile_at(player.x, player.y)
        room.visited = True
        print(room.intro_text(player))

        # Le temps passant l'alcolémie du joueur passe
        if player.drunkness > 0 and last_input != "b":
            player.drunkness *= 0.85 if player.drunkness>0.5 else 0

        # Voir l'inventaire n'est pas considéré comme agissant dans le jeu
        if last_input != "i":
            room.modify_player(player)

        if player.is_alive() and not player.victory:
            print("Vos points de vie : {}".format(player.hp))
            if player.drunkness > 0:
                print("Ébriété : {}".format(round(player.drunkness,2)))

            print("\nChoisir une action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)

            correct_input = False
            while not correct_input:
                action_input = input('\nAction: ')
                for action in available_actions:
                    if action_input == action.hotkey:
                        player.do_action(action, **action.kwargs)
                        correct_input = True
                        last_input = action.hotkey
                        break

    if not player.is_alive():
        print("""
        Vous venez de rejoindre la horde des pirates mort-vivants qui hantent
        cette île maudite qui jadis comme vous avaient eu le rêve fou de quitter
        ce lieu avec le trésor de Barbe Noire...

        Le pirate qui repartira vivant est, semble t-il, pas encore né !
        """)


if __name__ == "__main__":
    play()