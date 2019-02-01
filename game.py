import urwid
from player import Player
import world


class Game:

    begin_text = "Durant une nuit festive à Port-Royal, vous avez gagné aux \
jeux une carte maritime au fin fond d'une taverne à l'atmosphère si \
alcolisée que tout le monde est saoul avant même d'avoir commandé son \
premier verre de rhum. En effet votre adversaire de table n'était autre \
que «Pimflick jambe de bois», le dernier membre vivant de l'équipage de \
«Barbe noire» le célèbre pirate qui écuma les mers des Caraïbes. Pimflick \
n'a pas eu d'autre choix que de vous donner sa carte pour honorer son pari \
perdu. Mauvais joueur qu'il est, c'est surtout votre mousquet sur son \
front qu'il l'a convaincu.\n\
\n\
«Va au diable, pauvre fou !», ce sont les\
dernières paroles que vous avez entendu en quittant la taverne. Grace à \
la carte de Pimflick, vous venez d'aborder l'île de la tortue, avec la \
ferme intention de découvrir et de ramener ...\n\
\n\
... LE TRÉSOR DE BARBE NOIR !"

    player_death_text = "Vous venez de rejoindre la horde des pirates \
mort-vivants qui hantent cette île maudite qui jadis comme vous avaient eu le \
rêve fou de quitter ce lieu avec le trésor de Barbe Noire...\n\
\n\
Le pirate qui repartira vivant est, semble t-il, pas encore né !"

    def __init__(self):


        self.player = None
        self.room = None

        # Styles for urwid
        self.palette = [
        ('button normal', 'white', 'default'),
        ('button select', 'black', 'white'),
        ('line', 'white', 'default'),
        ]

        #ui
        self._intro_text = urwid.Text('') # Descripitif du lieu
        self._feedback_text = urwid.Text('') # Retour utilisateur
        self._status_text = urwid.Text('') # Status du joueur
        self._map_text = urwid.Text('') # La carte d'exploration du joueur


        texts = urwid.Padding(
            urwid.Filler(
                urwid.Pile([
                    self._intro_text,
                    self._feedback_text,
                    ]),
                valign='middle'
                ),
            left = 1,
            right = 1
            )

        self.controls = urwid.SimpleListWalker([])
        controls_box = urwid.ListBox(self.controls)
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')

        layout = urwid.Columns([
            ('weight', 2, urwid.Padding(texts,left=4, right=2)),
            ('fixed', 1, vline),
            ('weight', 1, urwid.Padding(controls_box, left=2, right=2))
            ])

        outlined_box = urwid.LineBox(layout)
        title_game = urwid.Text("L'île au trésor".upper(), align='center')
        self.main_box = urwid.Frame(outlined_box, header=title_game)

        # Init début du jeu
        self.start()

    def start(self, button=None):
        """Initialisation du jeu en début de chaque partie"""
        world.create_world()

        # Joueur au début du jeu
        self.player = Player(world.starting_position)
        # Lieu de démarrage
        self.room = world.tile_at(self.player.x, self.player.y)
        self.room.visited = True
        # Texte de présentation du jeu
        self._intro_text.set_text(Game.begin_text)
        # Update clonne gauche : map + status + actions
        self.update_controls()

    def quit(self, button=None):
        raise urwid.ExitMainLoop()

    def get_action_buttons(self):
        """Une liste de boutons correpondants aux actions disponible
        du lieu en cours"""
        buttons_list = []
        if self.player.is_alive() and not self.player.victory:
            available_actions = self.room.available_actions()
            for a in available_actions:
                button = urwid.Button(a.name)
                urwid.connect_signal(button, 'click', self.do_player_action, a)
                b = urwid.AttrWrap(button, 'button normal', 'button select')
                buttons_list.append(b)
        else:
            but_start = urwid.Button('Nouvelle partie ?', on_press=self.start)
            b = urwid.AttrWrap(but_start, 'button normal', 'button select')
            buttons_list.append(b)
            but_quit = urwid.Button('Quitter', on_press=self.quit)
            b = urwid.AttrWrap(but_quit, 'button normal', 'button select')
            buttons_list.append(b)

        #     buttons_list = []
        return buttons_list

    def get_player_status(self):
        """Retourne les points de vie et taux d'ébriété"""
        status = "Vos points de vie : {}".format(self.player.hp)
        if self.player.drunkness > 0:
            status += "\nÉbriété : {}".format(round(self.player.drunkness,2))
        self._status_text.set_text(status)

    def get_map(self):
        map_txt = self.player.print_map(world.world_map)
        self._map_text.set_text(map_txt)

    def update_controls(self):
        """Actualise toute la colonne gauche dédiée aux contrôles
        """
        self.get_player_status()
        self.get_map()
        self.controls[:] = [
            urwid.Text('CARTE', align = 'center'),
            urwid.LineBox(self._map_text),
            urwid.Divider(),
            urwid.Text('STATUS', align = 'center'),
            urwid.LineBox(self._status_text),
            urwid.Divider(),
            urwid.Text('ACTIONS', align = 'center'),
        ] + self.get_action_buttons()


        # self._controls_filler.original_widget = urwid.Pile(self.buttons_list)

    def do_player_action(self, button, action):
        # Init retour utilisateur
        feedback = []
        feedback_modify_player = None
        feedback_action = None


        # On execute l'action du joueur
        if self.player.is_alive() and not self.player.victory:
            # On execute l'action du joueur
            feedback_action = self.player.do_action(action, **action.kwargs)

        if self.player.is_alive() and not self.player.victory:
            # Si l'action etait un mouvement, l'emplacement est actualisé
            self.room = world.tile_at(self.player.x, self.player.y)
            # L'emplacement est maintenant connu de la map
            self.room.visited = True
            # Affichage de l'intro de l'emplacement
            self._intro_text.set_text(self.room.intro_text(self.player))
            # Le temps passant l'alcolémie du joueur passe
            if self.player.drunkness > 0 and action.hotkey != "b":
                self.player.drunkness *= 0.85 if self.player.drunkness>0.5 else 0
            # Le joueur est impacté par de son nouvel environnement
            if action.hotkey != "i": # Inventaire est non agissant
                feedback_modify_player = self.room.modify_player(self.player)

        # Le joueur est mort
        if not self.player.is_alive():
            feedback_modify_player = None
            feedback_action = None
            self._intro_text.set_text(Game.player_death_text)

        # Affichage feedback lieu + action
        if feedback_modify_player is not None:
            feedback.append(feedback_modify_player)
        if feedback_action is not None:
            feedback.append(feedback_action)
        self._feedback_text.set_text("\n".join(feedback))

        # Les actions possibles sont actualisées
        self.update_controls()

    def run(self):
        loop = urwid.MainLoop(self.main_box, self.palette)
        loop.run()


if __name__ == "__main__":
    game = Game()
    game.run()