from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from model.__init__ import Base


class Effort_outil(Base):
    """Classe du modèle représentant les efforts à l'outil d'une experience"""
    __tablename__ = 'effort_outil'

    # Attribut de la table
    id_effort_outil = Column(Integer, primary_key=True)
    temps_effort_outil = Column(Float)
    fx = Column(Float)
    fy = Column(Float)
    fz = Column(Float)

    # Table parent
    id_entree_outil = Column(Integer, ForeignKey("entree_outil.id_entree_outil"))
    entree_outil = relationship("Entree_outil", back_populates="effort_outil", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe effort_outil"""
        if not len(args) == 0:
            self.temps_effort_outil = args[0]
            self.fx = args[1]
            self.fy = args[2]
            self.fz = args[3]
            self.entree_outil = args[4]

    def __eq__(self, other):
        """Fonction qui compare deux objets effort_outil

        Parameters
        ----------
        other : Effort_outil
            L'objet effort_outil à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_outil is None:
            if self.fx != other.fx or self.fy != other.fy or self.fz != other.fz or self.temps_effort_outil != other.temps_effort_outil:
                return False
        else:
            if self.fx != other.fx or self.fy != other.fy or self.fz != other.fz or self.temps_effort_outil != other.temps_effort_outil:
                return False
            else:
                if not self.entree_outil.__eq__(other.entree_outil):
                    return False
        return True

    @property
    def __temps_effort_outil__(self):
        return self.temps_effort_outil

    @__temps_effort_outil__.setter
    def __temps_effort_outil__(self, temps_effort_outil):
        self.temps_effort_outil = temps_effort_outil

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
    def __entree_outil__(self):
        return self.entree_outil

    @__entree_outil__.setter
    def __entree_outil__(self, entree_outil):
        self.entree_outil = entree_outil

