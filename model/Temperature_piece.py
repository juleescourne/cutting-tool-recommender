from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Temperature_piece(Base):
    """Classe du modèle représentant les temperature à la pièce"""
    __tablename__ = 'temperature_piece'

    # Attributs de la table
    id_temperature_piece = Column(Integer, primary_key=True)
    temps_temperature_piece = Column(Float)
    temperature_piece = Column(Float)

    # Table parent
    id_entree_piece = Column(Integer, ForeignKey("entree_piece.id_entree_piece"))
    entree_piece = relationship("Entree_piece", back_populates="temperature_piece", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe temperature_piece"""
        if not len(args) == 0:
            self.temps_temperature_piece = args[0]
            self.temperature_piece = args[1]
            self.entree_piece = args[2]

    def __eq__(self, other):
        """Fonction qui compare deux objets temperature_piece

        Parameters
        ----------
        other : Temperature_piece
            L'objet temperature_piece à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_piece is None:
            if self.temps_temperature_piece != other.temps_temperature_piece or \
                    self.temperature_piece != other.temps_temperature_piece:
                return False
        else:
            if self.temps_temperature_piece != other.temps_temperature_piece or \
                    self.temperature_piece != other.temps_temperature_piece:
                return False
            elif self.entree_piece.type_matiere != other.entree_piece.type_matiere or \
                    self.entree_piece.materiaux != other.entree_piece.materiaux or \
                    self.entree_piece.procede_elaboration != other.entree_piece.procede_elaboration or \
                    self.entree_piece.impression_3d != other.entree_piece.impression_3d or \
                    self.entree_piece.longueur_usinee != other.entree_piece.longueur_usinee or \
                    self.entree_piece.num_passe != other.entree_piece.num_passe:
                return False
        return True

    @property
    def __temps_temperature_piece__(self):
        return self.temps_temperature_piece

    @__temps_temperature_piece__.setter
    def __temps_temperature_piece__(self, temps_temperature_piece):
        self.temps_temperature_piece = temps_temperature_piece

    @property
    def __temperature_piece__(self):
        return self.temperature_piece

    @__temperature_piece__.setter
    def __temperature_piece__(self, temperature_piece):
        self.temperature_piece = temperature_piece

    @property
    def __entree_piece__(self):
        return self.entree_piece

    @__entree_piece__.setter
    def __entree_piece__(self, entree_piece):
        self.entree_piece = entree_piece
