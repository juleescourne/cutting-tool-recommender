from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from model.__init__ import Base


class Sortie_piece(Base):
    """Classe du modèle représentant les sorties de la pièce"""
    __tablename__ = 'sortie_piece'

    # Attributs de la table
    id_sortie_piece = Column(Integer, primary_key=True)
    rugosite = Column(Float)
    durete = Column(Float)
    limite_endurance = Column(Float)
    contrainte_residuelle = Column(Float)

    # Table parent
    id_entree_piece = Column(Integer, ForeignKey("entree_piece.id_entree_piece"))
    entree_piece = relationship("Entree_piece", back_populates="sortie_piece", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe sortie_piece"""
        if not len(args) == 0:
            self.rugosite = args[0]
            self.durete = args[1]
            self.limite_endurance = args[2]
            self.contrainte_residuelle = args[3]
            self.entree_piece = args[4]

    @property
    def __rugosite__(self):
        return self.rugosite

    @__rugosite__.setter
    def __rugosite__(self, rugosite):
        self.rugosite = rugosite

    @property
    def __durete__(self):
        return self.temperature_piece

    @__durete__.setter
    def __durete__(self, durete):
        self.durete = durete

    @property
    def __limite_endurance__(self):
        return self.temperature_piece

    @__limite_endurance__.setter
    def __limite_endurance__(self, limite_endurance):
        self.limite_endurance = limite_endurance

    @property
    def __contrainte_residuelle__(self):
        return self.temperature_piece

    @__contrainte_residuelle__.setter
    def __contrainte_residuelle__(self, contrainte_residuelle):
        self.contrainte_residuelle = contrainte_residuelle

    @property
    def __entree_piece__(self):
        return self.entree_piece

    @__entree_piece__.setter
    def __entree_piece__(self, entree_piece):
        self.entree_piece = entree_piece
