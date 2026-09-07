from model import session
from model.Effort_piece import Effort_piece
from model.Entree_piece import Entree_piece
from model import mydb


class Effort_pieceController:
    """Classe qui gère l'ajout d'un objet Effort_piece dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Effort_pieceController"""
        self.effort_piece = Effort_piece()
        self.mycursor = mydb.cursor()

    def create_effort_piece(self, temps_effort_piece, fx, fy, fz, entree_piece):
        """fonction qui ajoute des efforts à la piece à la base de données

        Parameters
        ----------
        temps_effort_piece : float
            valeur de l'attribut 'temps_effort_piece' de la table Effort_piece
        fx : float
            valeur de l'attribut 'fx' de la table Effort_piece
        fy : float
            valeur de l'attribut 'fy' de la table Effort_piece
        fz : float
            valeur de l'attribut 'fz' de la table Effort_piece
        entree_piece : Entree_piece
            Objet entree_piece associe à la table Effort_piece
        """

        # On remplit les propriétés de l'objet Effort_piece avec les valeurs passées en paramètre
        self.effort_piece.temps_effort_piece = temps_effort_piece
        self.effort_piece.fx = fx
        self.effort_piece.fy = fy
        self.effort_piece.fz = fz

        if entree_piece is not None:
            entree = session.query(Entree_piece).filter_by(type_matiere=entree_piece.type_matiere,
                                                               materiaux=entree_piece.materiaux, procede_elaboration=entree_piece.procede_elaboration
                                                               , impression_3d=entree_piece.impression_3d, longueur_usinee=entree_piece.longueur_usinee, num_passe = entree_piece.num_passe).all()
            if len(entree) != 0:
                self.effort_piece.entree_piece = entree[-1]
        else:
            self.effort_piece.entree_piece = None

        session.add(self.effort_piece)
        session.commit()
        session.close()
