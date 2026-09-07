from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Entree_piece(Base):
    """Classe du modèle représentant les paramètres d'entrée concernant les pieces d'une expérience"""
    __tablename__ = 'entree_piece'

    # Attributs de la table
    id_entree_piece = Column(Integer, primary_key=True)
    type_matiere = Column(VARCHAR(15))
    materiaux = Column(VARCHAR(15))
    procede_elaboration = Column(VARCHAR(15))
    impression_3d = Column(VARCHAR(15))
    longueur_usinee = Column(Float)
    num_passe = Column(Integer)

    # Table parent
    id_experience = Column(Integer, ForeignKey('experience.id_experience'))
    experience = relationship("Experience", back_populates="entree_piece", cascade="all, delete")

    # Tables enfants
    effort_piece = relationship("Effort_piece", back_populates="entree_piece")
    temperature_piece = relationship("Temperature_piece",back_populates="entree_piece")
    sortie_piece = relationship("Sortie_piece",back_populates="entree_piece")
    vibration = relationship("Vibration", back_populates="entree_piece")

    def __init__(self, *args):
        """Constructeur de la classe entree_piece"""
        if not len(args) == 0:
            if len(args) == 1:
                self.type_matiere = args[0]
            if len(args) == 2:
                self.type_matiere = args[0]
                self.materiaux = args[1]
            else:
                self.type_matiere = args[0]
                self.materiaux = args[1]
                self.procede_elaboration = args[2]
                self.impression_3d = args[3]
                self.longueur_usinee = args[4]
                self.num_passe = args[5]
                self.temperature_piece = args[6]
                self.effort_piece = args[7]
                self.sortie_piece = args[8]
                self.vibration = args[9]
                self.experience = args[10]

    def __eq__(self, other):
        """Fonction qui compare deux objets entree_piece

        Parameters
        ----------
        other : Entree_piece
            L'objet entree_piece à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.temperature_piece is None and self.effort_piece is None and self.sortie_piece is None and self.experience is None and self.vibration is None:
            if self.type_matiere != other.type_matiere or self.materiaux != other.materiaux or \
                    self.procede_elaboration != other.procede_elaboration or self.impression_3d != other.impression_3d or \
                    self.longueur_usinee != other.longueur_usinee or self.num_passe != other.num_passe :
                return False
        else:
            if self.temperature_piece is not None :
                for i in range(len(self.temperature_piece)):
                    if not self.temperature_piece[i].__eq__(other.temperature_piece[i]):
                        return False
            if self.sortie_piece is not None:
                for i in range(len(self.sortie_piece)):
                    if not self.sortie_piece[i].__eq__(other.sortie_piece[i]):
                        return False
            if self.effort_piece is not None:
                for i in range(len(self.effort_piece)):
                    if not self.effort_piece[i].__eq__(other.effort_piece[i]):
                        return False
            if self.vibration is not None:
                for i in range(len(self.vibration)):
                    if not self.vibration[i].__eq__(other.vibration[i]):
                        return False
            if self.experience is not None:
                if not self.experience.__eq__(other.experience):
                    return False
        return True

    @property
    def __type_matiere__(self):
        return self.type_matiere

    @__type_matiere__.setter
    def __type_matiere__(self, type_matiere):
        self.type_matiere = type_matiere

    @property
    def __materiaux__(self):
        return self.materiaux

    @__materiaux__.setter
    def __materiaux__(self, materiaux):
        self.materiaux = materiaux

    @property
    def __procede_elaboration__(self):
        return self.procede_elaboration

    @__procede_elaboration__.setter
    def __procede_elaboration__(self, procede_elaboration):
        self.procede_elaboration = procede_elaboration

    @property
    def __impression_3d__(self):
        return self.impression_3d

    @__impression_3d__.setter
    def __impression_3d__(self, impression_3d):
        self.impression_3d = impression_3d

    @property
    def __longueur_usinee__(self):
        return self.longueur_usinee

    @__longueur_usinee__.setter
    def __longueur_usinee__(self, longueur_usinee):
        self.longueur_usinee = longueur_usinee

    @property
    def __num_passe__(self):
        return self.num_passe

    @__num_passe__.setter
    def __num_passe__(self, num_passe):
        self.num_passe = num_passe

    @property
    def __effort_piece__(self):
        return self.effort_piece

    @__effort_piece__.setter
    def __effort_piece__(self, effort_piece):
        self.effort_piece = effort_piece

    @property
    def __temperature_piece__(self):
        return self.temperature_piece

    @__temperature_piece__.setter
    def __temperature_piece__(self, temperature_piece):
        self.temperature_piece = temperature_piece

    @property
    def __vibration__(self):
        return self.vibration

    @__vibration__.setter
    def __vibration__(self, vibration):
        self.vibration = vibration

    @property
    def __sortie_piece__(self):
        return self.sortie_piece

    @__sortie_piece__.setter
    def __sortie_piece__(self, sortie_piece):
        self.sortie_piece = sortie_piece

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
