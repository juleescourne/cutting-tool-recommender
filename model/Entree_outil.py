from sqlalchemy import Column, Integer, VARCHAR, Float, ForeignKey
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Entree_outil(Base):
    """Classe du modèle représentant les paramètres d'entrée concernant les outils d'une expérience"""
    __tablename__ = 'entree_outil'

    # Attributs de la table
    id_entree_outil = Column(Integer, primary_key=True)
    type_outil = Column(VARCHAR(15))
    matiere = Column(VARCHAR(15))
    diametre = Column(Float)
    nb_dents_util = Column(Integer)
    revetement = Column(VARCHAR(15))
    rayon_arrete = Column(Float)
    angle_depouille = Column(Float)
    angle_axial = Column(Float)
    angle_radial = Column(Float)
    angle_attaque = Column(Float)
    angle_listel1 = Column(Float)
    angle_listel2 = Column(Float)

    # Table parent
    id_experience = Column(Integer, ForeignKey('experience.id_experience'))
    experience = relationship("Experience", back_populates="entree_outil", cascade="all, delete")

    # Table enfant
    effort_outil = relationship("Effort_outil", back_populates="entree_outil", cascade="all, delete")
    temperature_outil = relationship("Temperature_outil", back_populates="entree_outil", cascade="all, delete")
    usure_outil = relationship("Usure_outil", back_populates="entree_outil", cascade="all, delete")
    vibration = relationship("Vibration", back_populates="entree_outil")

    def __init__(self, *args):
        """Constructeur de la classe entree_outil"""
        if not len(args) == 0:
            if len(args) == 1:
                self.type_outil = args[0]
            if len(args) == 2:
                self.type_outil = args[0]
                self.matiere = args[1]
            else:
                self.type_outil = args[0]
                self.matiere = args[1]
                self.nb_dents_util = args[2]
                self.revetement = args[3]
                self.diametre = args[4]
                self.rayon_arrete = args[5]
                self.angle_depouille = args[6]
                self.angle_axial = args[7]
                self.angle_radial = args[8]
                self.angle_attaque = args[9]
                self.angle_listel1 = args[10]
                self.angle_listel2 = args[11]
                self.effort_outil = args[12]
                self.temperature_outil = args[13]
                self.usure_outil = args[14]
                self.vibration = args[15]
                self.experience = args[16]

    def __eq__(self, other):
        """Fonction qui compare deux objets entree_outil

        Parameters
        ----------
        other : Entree_outil
            L'objet entree_outil à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.experience is None and self.usure_outil is None and self.effort_outil is None and self.temperature_outil and self.vibration is None:
            if self.type_outil != other.type_outil or self.matiere != other.matiere or self.nb_dents_util != other.nb_dents_util or self.revetement != \
                    other.revetement or self.diametre != other.diametre or self.rayon_arrete != other.rayon_arrete or self.angle_radial != other.angle_radial or \
                    self.angle_axial != other.angle_axial or self.angle_attaque != other.angle_attaque or self.angle_depouille != other.angle_depouille or \
                    self.angle_listel1 != other.angle_listel1 or self.angle_listel2 != other.angle_listel2:
                return False
        else:
            if self.type_outil != other.type_outil or self.matiere != other.matiere or self.nb_dents_util != other.nb_dents_util or self.revetement != \
                    other.revetement or self.diametre != other.diametre or self.rayon_arrete != other.rayon_arrete or self.angle_radial != other.angle_radial or \
                    self.angle_axial != other.angle_axial or self.angle_attaque != other.angle_attaque or self.angle_depouille != other.angle_depouille or \
                    self.angle_listel1 != other.angle_listel1 or self.angle_listel2 != other.angle_listel2 :
                return False
            else:
                if self.experience is not None:
                    if not self.experience.__eq__(other.experience):
                        return False
                if self.temperature_outil is not None:
                    for i in range(len(self.temperature_outil)):
                        if not self.temperature_outil[i].__eq__(other.temperature_outil[i]):
                            return False
                if self.effort_outil is not None:
                    for i in range(len(self.effort_outil)):
                        if not self.effort_outil[i].__eq__(other.effort_outil[i]):
                            return False
                if self.usure_outil is not None:
                    for i in range(len(self.usure_outil)):
                        if not self.usure_outil[i].__eq__(other.usure_outil[i]):
                            return False
                if self.vibration is not None:
                    for i in range(len(self.vibration)):
                        if not self.vibration[i].__eq__(other.vibration[i]):
                            return False
        return True

    @property
    def __type_outil__(self):
        return self.type_outil

    @__type_outil__.setter
    def __type_outil__(self, type_outil):
        self.type_lubrifiant = type_outil

    @property
    def __matiere__(self):
        return self.vitesse_coupe

    @__matiere__.setter
    def __matiere__(self, matiere):
        self.matiere = matiere

    @property
    def __diametre__(self):
        return self.vitesse_avance

    @__diametre__.setter
    def __diametre__(self, diametre):
        self.diametre = diametre

    @property
    def __nb_dents_util__(self):
        return self.profondeur_passe

    @__nb_dents_util__.setter
    def __nb_dents_util__(self, nb_dents_util):
        self.nb_dents_util = nb_dents_util

    @property
    def __revetement__(self):
        return self.temps

    @__revetement__.setter
    def __revetement__(self, revetement):
        self.revetement = revetement

    @property
    def __rayon_arrete__(self):
        return self.rayon_arrete

    @__rayon_arrete__.setter
    def __rayon_arrete__(self, rayon_arrete):
        self.rayon_arrete = rayon_arrete

    @property
    def __angle_depouille__(self):
        return self.angle_depouille

    @__angle_depouille__.setter
    def __angle_depouille__(self, angle_depouille):
        self.angle_depouille = angle_depouille

    @property
    def __angle_axial__(self):
        return self.angle_axial

    @__angle_axial__.setter
    def __angle_axial__(self, angle_axial):
        self.angle_axial = angle_axial

    @property
    def __angle_radial__(self):
        return self.experience

    @__angle_radial__.setter
    def __angle_radial__(self, angle_radial):
        self.angle_radial = angle_radial

    @property
    def __angle_attaque__(self):
        return self.experience

    @__angle_attaque__.setter
    def __angle_attaque__(self, angle_attaque):
        self.angle_attaque = angle_attaque

    @property
    def __angle_listel1__(self):
        return self.angle_listel1

    @__angle_listel1__.setter
    def __angle_listel1__(self, angle_listel1):
        self.angle_listel1 = angle_listel1

    @property
    def __angle_listel2__(self):
        return self.angle_listel2

    @__angle_listel2__.setter
    def __angle_listel2__(self, angle_listel2):
        self.angle_listel2 = angle_listel2

    @property
    def __effort_outil__(self):
        return self.effort_outil

    @__effort_outil__.setter
    def __effort_outil__(self, effort_outil):
        self.effort_outil = effort_outil

    @property
    def __temperature_outil__(self):
        return self.temperature_outil

    @__temperature_outil__.setter
    def __temperature_outil__(self, temperature_outil):
        self.temperature_outil = temperature_outil

    @property
    def __usure_outil__(self):
        return self.usure_outil

    @__usure_outil__.setter
    def __usure_outil__(self, usure_outil):
        self.usure_outil = usure_outil

    @property
    def __vibration__(self):
        return self.vibration

    @__vibration__.setter
    def __vibration__(self, vibration):
        self.vibration = vibration

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
