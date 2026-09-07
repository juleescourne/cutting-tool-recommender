from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Usure_outil(Base):
    """Classe du modèle représentant l'usure de l'outil"""
    __tablename__ = 'usure_outil'

    # Attributs de la table
    id_usure_outil = Column(Integer, primary_key=True)
    temps_usinage = Column(Float)
    vb = Column(Float)
    er = Column(Float)
    kt = Column(Float)

    # Table parent
    id_entree_outil = Column(Integer, ForeignKey("entree_outil.id_entree_outil"))
    entree_outil = relationship("Entree_outil", back_populates="usure_outil", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe Usure_outil"""
        if not len(args) == 0:
            self.temps_usinage = args[0]
            self.vb = args[1]
            self.er = args[2]
            self.kt = args[3]
            self.entree_outil = args[4]

    def __eq__(self, other):
        """Fonction qui compare deux objets usure_outil

        Parameters
        ----------
        other : Usure_outil
            L'objet usure_outil à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_outil is None:
            if self.temps_usinage != other.temps_usinage or self.vb != other.vb or \
                    self.er != other.er or self.kt != other.kt:
                return False
        else:
            if self.temps_usinage != other.temps_usinage or self.vb != other.vb or \
                    self.er != other.er or self.kt != other.kt:
                return False
            else:
                if self.entree_outil is not None:
                    if not self.entree_outil.__eq__(other.entree_outil):
                        return False
        return True

    @property
    def __temps_usinage__(self):
        return self.temps_usinage

    @__temps_usinage__.setter
    def __temps_usinage__(self, temps_usinage):
        self.temps_usinage = temps_usinage

    @property
    def __vb__(self):
        return self.vb

    @__vb__.setter
    def __vb__(self, vb):
        self.vb = vb

    @property
    def __er__(self):
        return self.er

    @__er__.setter
    def __er__(self, er):
        self.er = er

    @property
    def __kt__(self):
        return self.kt

    @__kt__.setter
    def __kt__(self, kt):
        self.kt = kt

    @property
    def __entree_outil__(self):
        return self.entree_piece

    @__entree_outil__.setter
    def __entree_outil__(self, entree_outil):
        self.entree_outil = entree_outil
