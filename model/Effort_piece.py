from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from model.__init__ import Base


class Effort_piece(Base):
    """Classe du modèle représentant les efforts à la pièce d'une experience"""
    __tablename__ = 'effort_piece'

    # Attributs de la table
    id_effort_piece = Column(Integer, primary_key=True)
    temps_effort_piece = Column(Float)
    fx = Column(Float)
    fy = Column(Float)
    fz = Column(Float)

    # Table parent
    id_entree_piece = Column(Integer, ForeignKey("entree_piece.id_entree_piece"))
    entree_piece = relationship("Entree_piece", back_populates="effort_piece", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe effort_piece"""
        if not len(args) == 0:
            self.temps_effort_piece = args[0]
            self.fx = args[1]
            self.fy = args[2]
            self.fz = args[3]
            self.entree_piece = args[4]

    def __eq__(self, other):
        """Fonction qui compare deux objets effort_piece

        Parameters
        ----------
        other : Effort_piece
            L'objet effort_piece à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_piece is None:
            if self.fx != other.fx or self.fy != other.fy or self.fz != other.fz or self.temps_effort_piece != other.temps_effort_piece:
                return False
        else:
            if self.fx != other.fx or self.fy != other.fy or self.fz != other.fz or self.temps_effort_piece != other.temps_effort_piece:
                return False
            else:
                if self.entree_piece.type_matiere != other.entree_piece.type_matiere or \
                        self.entree_piece.materiaux != other.entree_piece.materiaux or \
                        self.entree_piece.procede_elaboration != other.entree_piece.procede_elaboration or \
                        self.entree_piece.impression_3d != other.entree_piece.impression_3d or \
                        self.entree_piece.longueur_usinee != other.entree_piece.longueur_usinee or \
                        self.entree_piece.num_passe != other.entree_piece.num_passe:
                    return False
        return True

    @property
    def __temps_effort_piece__(self):
        return self.temps_effort_piece

    @__temps_effort_piece__.setter
    def __temps_effort_piece__(self, temps_effort_piece):
        self.temps_effort_piece = temps_effort_piece

    @property
    def __fx__(self):
        return self.fx

    @__fx__.setter
    def __fx__(self, fx):
        self.fx = fx

    @property
    def __fy__(self):
        return self.fy

    @__fy__.setter
    def __fy__(self, fy):
        self.fy = fy

    @property
    def __fz__(self):
        return self.fz

    @__fz__.setter
    def __fz__(self, fz):
        self.fz = fz

    @property
    def __entree_piece__(self):
        return self.entree_piece

    @__entree_piece__.setter
    def __entree_piece__(self, entree_piece):
        self.entree_piece = entree_piece

