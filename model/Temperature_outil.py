from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Temperature_outil(Base):
    """Classe du modèle représentant les temperature à l'outil'"""
    __tablename__ = 'temperature_outil'

    # Attributs de la table
    id_temperature_outil = Column(Integer, primary_key=True)
    temps_temperature_outil = Column(Float)
    temperature_outil = Column(Float)

    # Table parent
    id_entree_outil = Column(Integer, ForeignKey("entree_outil.id_entree_outil"))
    entree_outil = relationship("Entree_outil", back_populates="temperature_outil",cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe temperature_outil"""
        if not len(args) == 0:
            self.temps_temperature_outil = args[0]
            self.temperature_outil = args[1]
            self.entree_outil = args[2]

    def __eq__(self, other):
        """Fonction qui compare deux objets temperature_outil

        Parameters
        ----------
        other : Temperature_outil
            L'objet temperature_outil à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_outil is None:
            if self.temps_temperature_outil != other.temps_temperature_outil or \
                    self.temperature_outil != other.temps_temperature_outil:
                return False
        else:
            if self.temps_temperature_outil != other.temps_temperature_outil or \
                    self.temperature_outil != other.temps_temperature_outil:
                return False
            elif not self.entree_outil.__eq__(other.entree_outil):
                return False
        return True

    @property
    def __temps_temperature_outil__(self):
        return self.temps_temperature_outil

    @__temps_temperature_outil__.setter
    def __temps_temperature_outil__(self, temps_temperature_outil):
        self.temps_temperature_outil = temps_temperature_outil

    @property
    def __temperature_outil__(self):
        return self.temperature_outil

    @__temperature_outil__.setter
    def __temperature_outil__(self, temperature_outil):
        self.temperature_outil = temperature_outil

    @property
    def __entree_outil__(self):
        return self.entree_piece

    @__entree_outil__.setter
    def __entree_outil__(self, entree_outil):
        self.entree_outil = entree_outil
