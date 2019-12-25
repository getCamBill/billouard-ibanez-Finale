# ==============================================================================
from tkinter import *
from tkinter import ttk
from Model.Tablier import Tablier
from Model.Pioche import Pioche
from Model.Joueur import Joueur
from Model.Etat import Etat
from Model.Tour import Tour
from Controller.BDD import *
from functools import partial
from threading import Timer
from View.Ajout_user_view import *
import pygame
from PIL import Image, ImageTk
from random import randrange as rr, random
LARGEUR = 500
HAUTEUR = 400
# ------------------------------------------------------------------------------
class Quarto():
    # ----------------------------------------------------------------------------
    def __init__(self, fenetre, joueur1: Joueur = None, joueur2: Joueur = None):
        """

        :param fenetre:
        :param joueur1:
        :param joueur2:
        """
        # --------------------------------------------------------------------------
        self.fenetre = fenetre
        self.fenetre.title("Quarto !! ")


        self.n = ttk.Notebook(self.fenetre)  # Création du système d'onglets
        self.n.pack()

        self.o1 = ttk.Frame(self.n)  # Ajout de l'onglet 1
        self.o1.pack()

        self.o2 = ttk.Frame(self.n)  # Ajout de l'onglet 2
        self.o2.pack()

        self.o3 = ttk.Frame(self.n)  # Ajout de l'onglet 2
        self.o3.pack()

        self.n.add(self.o1, text='Quarto')  # Nom de l'onglet 1
        self.n.add(self.o2, text='Joueurs')  # Nom de l'onglet 2
        self.n.add(self.o3, text='Selectionner')  # Nom de l'onglet 2

        AddUser(self.o2)
        # --------------------------------------------------------------------------
        self.database: str = 'C:\\Users\\camil\\PycharmProjects\\Quarto\\Controller\\UserDatabase.db'
        self.conn = create_connection(self.database)
        # --------------------------------------------------------------------------
        self.Tablier: Tablier = Tablier()
        self.Etat: Etat = Etat(self.Tablier)
        self.Pioche: Pioche = Pioche()
        self.Joueur1: Joueur = joueur1
        self.Joueur2: Joueur = joueur2
        # self.Joueur1: Joueur = None
        # self.Joueur2: Joueur = None
        # self.Tour: Tour = Tour(self.Joueur1, self.Joueur1)
        self.aborted: bool = False
        """create the main window and pack the widgets"""

        # --------------------------------------------------------------------------
        self.framePlateau = Frame(self.o1, width=200, height=400, bg="grey")
        self.framePlateau.grid(row=0, column=0, padx=10, pady=5)

        self.framePieces = Frame(self.o1, width=200, height=400, bg="grey")
        self.framePieces.grid(row=0, column=2, padx=10, pady=5)

        self.frameCentre = Frame(self.o1, width=200, height=400)
        self.frameCentre.grid(row=0, column=1, padx=10, pady=5)
        # --------------------------------------------------------------------------



        # --------------------------------------------------------------------------
        self.fr1 = Frame(self.o3)
        self.fr1.grid(row=0, column=0)
        self.fr2 = Frame(self.o3)
        self.fr2.grid(row=0, column=1)
        # --------------------------------------------------------------------------
        self.user_name = Entry(self.fr1, width=30)
        self.user_name.grid(row=0, column=1, padx=20)
        self.user_name_label = Label(self.fr1, text="Joueur 1")
        self.user_name_label.grid(row=0, column=0)

        self.user_name2 = Entry(self.fr1, width=30)
        self.user_name2.grid(row=1, column=1, padx=20)
        self.user_name_label2 = Label(self.fr1, text="Joueur 2")
        self.user_name_label2.grid(row=1, column=0)
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------

        self.n.select(2)
        # -------------------------------------------------------------------------
        self.submit_btn = Button(self.fr1, text="JOUER")
        self.submit_btn['command'] = lambda user1=self.user_name.get(), user2=self.user_name2.get(): self.submit()
        self.submit_btn.grid(row=2, column=1, padx=10, pady=10)


        # --------------------------------------------------------------------------
        self.fenetre.mainloop()
        # --------------------------------------------------------------------------

# -------------------------------------------------------------------------
    def submit(self):
        """

        :return:
        """
        # listeJ = select_joueur_by_victory(self.conn)
        user1 = self.user_name.get()
        user2 = self.user_name2.get()
        listeJ = [ele[1] for ele in select_joueur_by_victory(self.conn)]

        if user1 != "" and user2 != "" and user1 in listeJ and user2 in listeJ:# si les deux joueurs sont dans la BDD on joue
            self.Joueur1.pseudo = user1
            self.Joueur2.pseudo = user2
            self.Tour: Tour = Tour(user1, user2)
            self.new_game()
            self.n.select(0)
        else: # si au moin un des deux joueur n'y est pas
            # self.popup(3)
            self.n.select(1)
    # -------------------------------------------------------------------------
    def createPlateau(self):
        """

        :return:
        """
        photo = PhotoImage(file=r"Z.png")  # C:Users\camil\PycharmProjects\UI\
        photoimage = photo.subsample(1, 1)
        idCases = list(self.Tablier.tablier.keys())
        # print(idCases)
        i: int = 0
        for ligne in range(4):
            for colonne in range(4):
                # bt = Button(self.framePlateau, image=photoimage)
                id = idCases[i]
                bt = Button(self.framePlateau, text=id, width=5, height=5)
                bt['command'] = lambda idx=idCases[i], binst=bt: self.choisirCase(binst, idx)
                bt.grid(row=ligne, column=colonne)
                # bt.pack()
                i += 1
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
    def createPioche(self):
        """

        :return:
        """
        idPieces = list(self.Pioche.listPieceDispo())
        taille = len(self.Pioche.listPieceDispo())
        # print(idPieces)
        pieces = []
        i: int = 0
        for ligne in range(4):
            for colonne in range(4):
        # for i, piece in enumerate(self.Pioche.listPieceDispo()):
        #         image = Image.open(idPieces[i] + ".png")
        #         photo = ImageTk.PhotoImage(image)
                button = Button(self.framePieces, text=idPieces[i], width=5, height=5)
                # self.button['image'] = photo
                button['command'] = lambda idx=idPieces[i], binst=button: self.choixPiece(idx, binst)
                button.grid(row=ligne, column=colonne)
                # button.pack(side="bottom", fill="both", expand="yes")
                i += 1
# --------------------------------------------------------------------------
    def choixPiece(self, idxPiece, binst):
        """

        :param idxPiece:
        :param binst:
        :return:
        """
        self.aQuiLeTour['text'] = str(self.Tour.auTourDe()[1] + " choisis la case")
        print(idxPiece)
        self.pieceStby['text'] = idxPiece
        self.Tablier.piecePourAdversaire(idxPiece, self.Joueur2)
        binst.destroy()
        self.Tour.tour += 1
# ---------------------------------------------------------------------------
    def choisirCase(self, binst, idxCase):
        """

        :param binst:
        :param idxCase:
        :return:
        """
        # --------------------------------------------------------------------------
        self.aQuiLeTour['text'] = str(self.Tour.auTourDe()[0] + " choisis la pièce")
        self.aQuiLeTour.grid(row=6, column=0)

        print(idxCase)
        self.idxCase = idxCase
        binst['text'] = self.pieceStby['text']
        binst['bg'] = 'red'
        if self.Tablier.poserPiece(self.Joueur2, idxCase, self.Pioche) == 1:
            self.popup(1)

        if self.Tour.tour > 2:
            self.vict()

# --------------------------------------------------------------------------
    def vict(self):
        """

        :return:
        """
        # on appelle les fonctions seulement au bout de 4 tours
        if self.Tablier.isQuarto():
            self.victoire = True
            self.aQuiLeTour['text'] = ""
            self.win['text'] = "QUARTO !!! " + self.Tour.auTourDe()[0] + " à gagné la partie"
            update_partie_joueur(self.conn, (1, 0, self.Tour.auTourDe()[0])) # on met à jour les données de chaque partie
            update_partie_joueur(self.conn, (0, 1, self.Tour.auTourDe()[1]))
            self.mon_audio.play(-1)
            self.popup(2)
# --------------------------------------------------------------------------
    def popup(self, code):
        """

        :param code:
        :return:
        """
        self.fInfos = Toplevel()  # Popup -> Toplevel()
        # ----------------------------------------------------
        if code == 1:
            self.fInfos.title('Infos')
            Button(self.fInfos, text='Ok je fais pas le teubé...', command=self.fInfos.destroy).pack(padx=10, pady=10)
        # ----------------------------------------------------
        elif code == 2:
            self.fInfos.title('Infos')
            Button(self.fInfos, text='Nouvelle partie', command=self.new_game).pack(padx=10, pady=10)
            Button(self.fInfos, text='Quitter', command=self.fenetre.destroy).pack(padx=10, pady=10)
        # ----------------------------------------------------
        elif code == 3:
            self.fInfos.title('Infos')
            Label(self.fInfos, text='Veuiller entrer les joueurs dans la BDD').pack(padx=10, pady=10)
            Button(self.fInfos, text='OK', command=self.fInfos.destroy).pack(padx=10, pady=10)
        # ----------------------------------------------------
        # ----------------------------------------------------
        self.fInfos.transient(self.fenetre)  # Réduction popup impossible
        self.fInfos.grab_set()  # Interaction avec fenetre jeu impossible
        self.fenetre.wait_window(self.fInfos)  # Arrêt script principal
# --------------------------------------------------------------------------

    def new_game(self):
        """

        :return:
        """
        # photo = PhotoImage(file=r"Z.png")
        self.pieceStby = Label(self.frameCentre, text='test')
        self.pieceStby.grid(row=4, column=0)
        # --------------------------------------------------------------------------
        self.win = Label(self.frameCentre, text=' ... ')
        self.win.grid(row=5, column=0)
        # --------------------------------------------------------------------------
        self.createPioche()
        self.createPlateau()
        self.cases: list = []
        self.idxCase = ''
        # --------------------------------------------------------------------------
        self.aQuiLeTour = Label(self.frameCentre, text=str(self.Tour.auTourDe()[0] + " choisis la pièce"))
        self.aQuiLeTour.grid(row=6, column=0)
        # --------------------------------------------------------------------------
        pygame.mixer.init()
        self.mon_audio = pygame.mixer.Sound("clap.wav")
        # --------------------------------------------------------------------------
        self.mon_audio.stop()
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# ==============================================================================
if __name__ == '__main__':

    j1 = Joueur()
    j2 = Joueur()
    fenetre = Tk()
    q = Quarto(fenetre, j1, j2)
    fenetre.mainloop()
    # q.show()
# ==============================================================================
