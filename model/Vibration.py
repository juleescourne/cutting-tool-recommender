from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Vibration(Base):
    """Classe du modèle représentant les vibration entre la pièce et l'outil"""
    __tablename__ = 'vibration'

    # Attributs de la table
    temps_vibration = Column(Float, primary_key=True)
    frequence = Column(Float)
    amplitude = Column(Float)

    # Tables parents
    id_entree_piece = Column(Integer, ForeignKey('entree_piece.id_entree_piece'), primary_key=True)
    id_entree_outil = Column(Integer, ForeignKey('entree_outil.id_entree_outil'), primary_key=True)
    entree_outil = relationship("Entree_outil", back_populates="vibration")
    entree_piece = relationship("Entree_piece", back_populates="vibration")

    def __init__(self, *args):
        """Constructeur de la classe Vibration"""
        if not len(args) == 0:
            if len(args) == 3:
                self.temps_vibration = args[0]
                self.frequence = args[1]
                self.amplitude = args[2]
            if len(args) == 5:
                self.temps_vibration = args[0]
                self.frequence = args[1]
                self.amplitude = args[2]
                self.entree_outil = args[3]
                self.entree_piece = args[4]

    def __eq__(self, other):
        """Fonction qui compare deux objets Vibration

        Parameters
        ----------
        other : Vibration
            L'objet Vibration à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.entree_piece is None and self.entree_outil is None:
            if self.temps_vibration != other.temps_vibration or self.frequence != other.frequence or self.amplitude != other.amplitude:
                return False
        if self.entree_piece is not None and self.entree_outil is None:
            if self.entree_piece.type_matiere != other.entree_piece.type_matiere or \
                    self.entree_piece.materiaux != other.entree_piece.materiaux or \
                    self.entree_piece.procede_elaboration != other.entree_piece.procede_elaboration or \
                    self.entree_piece.impression_3d != other.entree_piece.impression_3d or \
                    self.entree_piece.longueur_usinee != other.entree_piece.longueur_usinee or \
                    self.entree_piece.num_passe != other.entree_piece.num_passe:
                return False
            elif self.temps_vibration != other.temps_vibration or self.frequence != other.frequence or self.amplitude != other.amplitude:
                return False
        if self.entree_piece is None and self.entree_outil is not None:
            if self.entree_outil.type_outil != other.entree_outil.type_outil or self.entree_outil.matiere != other.entree_outil.matiere or self.entree_outil.nb_dents_util != other.entree_outil.nb_dents_util or self.entree_outil.revetement != \
                    other.entree_outil.revetement or self.entree_outil.diametre != other.entree_outil.diametre or self.entree_outil.rayon_arrete != other.entree_outil.rayon_arrete or self.entree_outil.angle_radial != other.entree_outil.angle_radial or \
                    self.entree_outil.angle_axial != other.entree_outil.angle_axial or self.entree_outil.angle_attaque != other.entree_outil.angle_attaque or self.entree_outil.angle_depouille != other.entree_outil.angle_depouille or \
                    self.entree_outil.angle_listel1 != other.entree_outil.angle_listel1 or self.entree_outil.angle_listel2 != other.entree_outil.angle_listel2:
                return False
            elif self.temps_vibration != other.temps_vibration or self.frequence != other.frequence or self.amplitude != other.amplitude:
                return False
        if self.entree_piece is not None and self.entree_outil is not None:
            if self.entree_piece.type_matiere != other.entree_piece.type_matiere or \
                    self.entree_piece.materiaux != other.entree_piece.materiaux or \
                    self.entree_piece.procede_elaboration != other.entree_piece.procede_elaboration or \
                    self.entree_piece.impression_3d != other.entree_piece.impression_3d or \
                    self.entree_piece.longueur_usinee != other.entree_piece.longueur_usinee or \
                    self.entree_piece.num_passe != other.entree_piece.num_passe:
                return False
            elif self.entree_outil.type_outil != other.entree_outil.type_outil or self.entree_outil.matiere != other.entree_outil.matiere or self.entree_outil.nb_dents_util != other.entree_outil.nb_dents_util or self.entree_outil.revetement != \
                    other.entree_outil.revetement or self.entree_outil.diametre != other.entree_outil.diametre or self.entree_outil.rayon_arrete != other.entree_outil.rayon_arrete or self.entree_outil.angle_radial != other.entree_outil.angle_radial or \
                    self.entree_outil.angle_axial != other.entree_outil.angle_axial or self.entree_outil.angle_attaque != other.entree_outil.angle_attaque or self.entree_outil.angle_depouille != other.entree_outil.angle_depouille or \
                    self.entree_outil.angle_listel1 != other.entree_outil.angle_listel1 or self.entree_outil.angle_listel2 != other.entree_outil.angle_listel2:
                return False
            elif self.temps_vibration != other.temps_vibration or self.frequence != other.frequence or self.amplitude != other.amplitude:
                return False
        return True

    @property
    def __temps_vibration__(self):
        return self.temps_vibration

    @__temps_vibration__.setter
    def __temps_vibration__(self, temps_vibration):
        self.temps_vibration = temps_vibration

    @property
    def __frequence__(self):
        return self.frequence

    @__frequence__.setter
    def __frequence__(self, frequence):
        self.frequence = frequence

    @property
    def __amplitude__(self):
        return self.amplitude

    @__amplitude__.setter
    def __amplitude__(self, amplitude):
        self.amplitude = amplitude

    @property
    def __entree_outil__(self):
        return self.entree_outil

    @__entree_outil__.setter
    def __entree_outil__(self, entree_outil):
        self.entree_outil = entree_outil

    @property
    def __entree_piece__(self):
        return self.entree_piece

    @__entree_piece__.setter
    def __entree_piece__(self, entree_piece):
        self.entree_piece = entree_piece
