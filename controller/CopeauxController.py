from model.Copeaux import Copeaux
from model import session
from model.Experience import Experience


class CopeauxController:
    """Classe qui gère l'ajout d'un objet copeaux dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Copeaux"""
        self.copeaux = Copeaux()

    def create_copeaux(self, epaisseur, nom_experience):
        """fonction qui ajoute un copeaux à la base de données

        Parameters:
            -epaisseur: epaisseur du copeaux
            -nom_experience: nom de l'experience associé au copeaux

        """
        self.copeaux.epaisseur = epaisseur

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.copeaux.experience = experience[-1]
        else:
            self.copeaux.experience = None

        session.add(self.copeaux)
        session.commit()
        session.close()
