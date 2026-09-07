from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Experience(Base):
    """Classe du modèle représentant une expérience"""
    __tablename__ = 'experience'

    # Attributs de la table
    id_experience = Column(Integer, primary_key=True)
    nom = Column(VARCHAR(100))

    # Tables enfants
    procede = relationship("Procede", back_populates="experience", cascade="all, delete")
    copeaux = relationship("Copeaux", back_populates="experience", cascade="all, delete")
    entree_outil = relationship("Entree_outil", back_populates="experience", cascade="all, delete")
    entree_piece = relationship("Entree_piece", back_populates="experience", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe experience"""
        if not len(args) == 0:
            if len(args) == 1:
                self.nom = args[0]
            else:
                self.nom = args[0]
                self.procede = args[1]
                self.copeaux = args[2]
                self.entree_piece = args[3]
                self.entree_outil = args[4]

    def __eq__(self, other):
        """Fonction qui compare deux objets experience

        Parameters
        ----------
        other : Experience
            L'objet expérience à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if len(self.entree_outil) != len(other.entree_outil):
            return False
        else:
            for i in range(len(self.entree_outil)):
                if self.entree_outil[i].type_outil != other.outil[i].entree_outil[i].type_outil or self.entree_outil[i].matiere != other.entree_outil[
                    i].matiere or self.entree_outil[i].diametre != other.entree_outil[i].diametre or self.entree_outil[i].duree_de_vie != \
                        other.entree_outil[i].duree_de_vie or self.entree_outil[i].nb_dents_util != other.entree_outil[i].nb_dents_util or \
                        self.entree_outil[i].revetement != other.entree_outil[i].revetement or self.entree_outil[i].rayon_arrete != other.entree_outil[i].rayon_arrete or \
                        self.entree_outil[i].angle_depouille != other.entree_outil[i].angle_depouille or \
                        self.entree_outil[i].angle_axial != other.entree_outil[i].angle_axial or self.entree_outil[i].angle_radial != other.entree_outil[i].angle_radial or \
                        self.entree_outil[i].angle_attaque != other.entree_outil[i].angle_attaque or self.entree_outil[i].angle_listel1 != other.entree_outil[i].angle_liste1 or \
                        self.entree_outil[i].angle_listel2 != other.entree_outil[i].angle_listel2 :
                    return False

        if len(self.entree_piece) != len(other.entree_piece):
            return False
        else:
            for i in range(len(self.entree_piece)):
                if self.entree_piece[i].type_matiere != other.entree_piece[i].type_matiere or self.entree_piece[i].materiaux != other.entree_piece[i].materiaux or \
                        self.entree_piece[i].procede_elaboration != other.entree_piece[i].procede_elaboration or self.entree_piece[i].impression_3d != \
                        other.entree_piece[i].impression_3d or self.entree_piece[i].longueur_usinee != other.entree_piece[i].longueur_usinee or \
                        self.entree_piece[i].num_passe != other.entree_piece[i].num_passe :
                    return False

        if len(self.copeaux) != len(other.copeaux):
            return False
        else:
            for i in range(len(self.copeaux)):
                if self.copeaux[i].epaisseur != other.copeaux[i].epaisseur:
                    return False
        if len(self.procede) != len(other.procede):
            return False
        else:
            for i in range(len(self.procede)):
                if self.procede[i].type_procede != other.procede[i].type_procede or self.procede[i].type_operation != other.procede[i].type_operation or \
                        self.procede[i].assistance != other.procede[i].assistance or self.procede[i].vitesse_coupe != other.procede[i].vitesse_coupe or \
                        self.procede[i].debit_cryo != other.procede[i].debit_cryo or self.procede[i].debit_mql != other.procede[i].debit_mql or \
                        self.procede[i].emuslion != other.procede[i].emuslion or self.procede[i].vitesse_avance_dent != other.procede[i].vitesse_avance_dent or \
                        self.procede[i].profondeur_passe != other.procede[i].profondeur_passe or self.procede[i].engagement != other.procede[i].engagement or \
                        self.procede[i].vitesse_avance_min != other.procede[i].vitesse_avance_min or self.procede[i].frequence_rotation != other.procede[i].frequence_rotation :
                    return False

        return self.nom == other.nom

    @property
    def __nom__(self):
        return self.nom

    @__nom__.setter
    def __nom__(self, nom):
        self.nom = nom

    @property
    def __procede__(self):
        return self.procede

    @__procede__.setter
    def __procede__(self, procede):
        self.procede = procede

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

    @property
    def __copeaux__(self):
        return self.copeaux

    @__copeaux__.setter
    def __copeaux__(self, copeaux):
        self.copeaux = copeaux
