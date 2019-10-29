from Piece import Piece

class Case(object):

    def __init__(self, idPiece: str, color: str=None, shape: str=None, size: str=None, dug: int=None ):
        self.idPiece: str = idPiece
        self.couleur: str = color
        self.shape: str = shape
        self.size: str = size
        self.dug: int = dug
        self.occuped: bool = False

    def pieceAttrToCase(self, pieceAttr: Piece):
    # méthode à revoir avec une boucle ou autre itérations pour chaque val
        self.couleur: str = pieceAttr.getColor()
        self.shape: str = pieceAttr.getShape()
        self.size: str = pieceAttr.getSize()
        self.dug: int = pieceAttr.getDug()

    def isCaseLibre(self):
        return self.occuped

    def showId(self):
        return self.idPiece

    # def showCase(self):
    #     print("Couleur : ", self.couleur,
    #     "Forme : ", self.shape,
    #     "Taille : ", self.size,
    #     "Creux : ", self.dug,
    #     "Occupée : ", self.occuped
    #     )