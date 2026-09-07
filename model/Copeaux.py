from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Copeaux(Base):
    """Classe du modèle représentant les copeaux d'une expérience"""
    __tablename__ = 'copeaux'

    # Attributs de la table
    id_copeaux = Column(Integer, primary_key=True)
    epaisseur = Column(Float)

    # Table parent
    id_experience = Column(Integer, ForeignKey('experience.id_experience'))
    experience = relationship("Experience", back_populates="copeaux", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe Copeaux"""
        if not len(args) == 0:
            if len(args) == 1:
                self.epaisseur = args[0]
            else:
                self.epaisseur = args[0]
                self.experience = args[1]

    def __eq__(self, other):
        """Fonction qui compare deux objets copeaux

            Parameters
            ----------
            other : Copeaux
                L'objet copeaux à comparer avec self

            Returns
            -------
            Boolean
                boolean qui indique si les deux objets sont égaux ou pas
            """
        if self.experience is None:
            return self.copeaux == other.copeaux
        else:
            return self.copeaux == other.copeaux and self.experience.nom == other.experience.nom

    @property
    def __epaisseur__(self):
        return self.epaisseur

    @__epaisseur__.setter
    def __epaisseur__(self, epaisseur):
        self.epaisseur = epaisseur

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
