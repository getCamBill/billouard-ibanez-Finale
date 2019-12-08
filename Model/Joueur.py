from Controller.BDD import *


class Joueur(object):

    def __init__(self, pseudo: str):

        self.pseudo: str = pseudo
        self.jouer: bool = False

        self.database: str = "./Controller/UserDatabase.db"
        self.conn = create_connection(self.database)

    def setPieceAttribuee(self, idPiece: str):
        self.pieceAttribuee = idPiece

    def setInfoJoueur(self, win: int, lose: int):
        with self.conn:
            update_partie_joueur(self.conn, (win, lose, self.pseudo))

    def show(self):
        with self.conn:
            print("1. Classement des joueurs par victoire:")
            select_joueur_by_victory(self.conn)