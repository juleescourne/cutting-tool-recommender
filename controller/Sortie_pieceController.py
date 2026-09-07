from model import session
from model.Sortie_piece import Sortie_piece
from model.Entree_piece import Entree_piece
from model import mydb


class Sortie_pieceController:
    """Classe qui gère l'ajout d'un objet sortie_piece dans la base de données"""

    def __init__(self):
        """Constructeur de la classe sortie_pieceController"""
        self.sortie_piece = Sortie_piece()
        self.mycursor = mydb.cursor()

    def create_sortie_piece(self, rugosite, durete, limite_endurance, contrainte_residuelle, entree_piece):
        """fonction qui ajoute un objet sortie_piece à la base de données

        Parameters
        ----------
        rugosite : float
            valeur de l'attribut 'rugosite' de la table sortie_piece
        durete : float
            valeur de l'attribut 'durete' de la table sortie_piece
        limite_endurance : float
            valeur de l'attribut 'limite_endurance' de la table sortie_piece
        contrainte_residuelle : float
            valeur de l'attribut 'contrainte_residuelle' de la table sortie_piece
        entree_piece : float
            objet entree_piece associé à la table sortie_piece
        """
        self.sortie_piece.rugosite = rugosite
        self.sortie_piecepiece.durete = durete
        self.sortie_piece.limite_endurance = limite_endurance
        self.sortie_piece.contrainte_residuelle = contrainte_residuelle

        # Si un objet Entree_piece est passé en paramètre, on cherche l'objet correspondant dans la base de données
        if entree_piece is not None:
            entree = session.query(Entree_piece).filter_by(type_matiere=entree_piece.type_matiere,
                                                               materiaux=entree_piece.materiaux, procede_elaboration=entree_piece.procede_elaboration
                                                               , impression_3d=entree_piece.impression_3d, longueur_usinee=entree_piece.longueur_usinee
                                                               , num_passe = entree_piece.num_passe).all()
            if len(entree) != 0:
                self.sortie_piece.entree_piece = entree[-1]
        else:
            self.sortie_piece.entree_piece = None

        session.add(self.sortie_piece)
        session.commit()
        session.close()
