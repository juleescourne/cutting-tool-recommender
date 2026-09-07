from model import session
from model.Temperature_piece import Temperature_piece
from model.Entree_piece import Entree_piece
from model import mydb


class Temperature_pieceController:
    """Classe qui gère l'ajout d'un objet temperature_piece dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Temperature_pieceController"""
        self.temperature_piece = Temperature_piece()
        self.mycursor = mydb.cursor()

    def create_temperature_piece(self, temps_temperature_piece, temperature_piece, entree_piece):
        """fonction qui ajoute un objet temperature_piece à la base de données

        Parameters
        ----------
        temps_temperature_piece : float
            valeur de l'attribut 'temps_temperature_piece' de la table temperature_piece
        temperature_piece : float
            valeur de l'attribut 'temperature_piece' de la table temperature_piece
        entree_piece : Entree_piece
           Objet Entree_piece associé à la table temperature_piece
        """
        # Affectation des attributs de la table temperature_piece
        self.temperature_piece.temps_temperature_piece = temps_temperature_piece
        self.temperature_piece.temperature_piece = temperature_piece

        # Récupération de l'objet entree_piece dans la base de données
        if entree_piece is not None:
            entree = session.query(Entree_piece).filter_by(type_matiere=entree_piece.type_matiere,
                                                           materiaux=entree_piece.materiaux,
                                                           procede_elaboration=entree_piece.procede_elaboration,
                                                           impression_3d=entree_piece.impression_3d,
                                                           longueur_usinee=entree_piece.longueur_usinee,
                                                           num_passe=entree_piece.num_passe).all()
            if len(entree) != 0:
                self.temperature_piece.entree_piece = entree[-1]
        else:
            self.temperature_piece.entree_piece = None

        # Ajout de l'objet temperature_piece dans la base de données
        session.add(self.temperature_piece)
        session.commit()
        session.close()



