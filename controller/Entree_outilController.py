from model.Vibration import Vibration
from model.Entree_outil import Entree_outil
from model import session, engine
from model.Experience import Experience
from model import mydb


class Entree_outilController:
    """Classe qui gère l'ajout d'un objet Entree_outil dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Entree_outilController"""
        self.entree_outil = Entree_outil()
        self.mycursor = mydb.cursor()

    def create_entree_outil(self, type_outil, matiere, diametre, nb_dents_util, revetement,
                            rayon_arrete, angle_depouille, angle_axial, angle_radial,
                            angle_attaque, angle_listel1, angle_listel2, nom_experience):
        """fonction qui ajoute un procede à la base de données

        Parameters
        ----------
        type_outil : string
            valeur de l'attribut 'type d'outil' de la table Entree_outil
        matiere : string
            valeur de l'attribut 'matiere' de la table Entree_outil
        diametre : float
            valeur de l'attribut 'diametre' de la table Entree_outil
        nb_dents_util : int
            valeur de l'attribut 'nb_dents_util' de la table Entree_outil
        revetement : string
            valeur de l'attribut 'revetement' de la table Entree_outil
        rayon_arrete : float
            valeur de l'attribut 'rayon_arrete' de la table Entree_outil
        angle_depouille : float
            valeur de l'attribut 'angle_depouille' de la table Entree_outil
        angle_axial : float
            valeur de l'attribut 'angle_axial' de la table Entree_outil
        angle_radial : float
            valeur de l'attribut 'angle_radial' de la table Entree_outil
        angle_attaque : float
            valeur de l'attribut 'angle_attaque' de la table Entree_outil
        angle_listel1 : float
            valeur de l'attribut 'angle_listel1' de la table Entree_outil
        angle_listel2 : float
            valeur de l'attribut 'angle_listel2' de la table Entree_outil
        """

        # On remplit les propriétés de l'objet Entree_outil avec les valeurs passées en paramètre
        self.entree_outil.type_outil = type_outil
        self.entree_outil.matiere = matiere
        self.entree_outil.diametre = diametre
        self.entree_outil.nb_dents_util = nb_dents_util
        self.entree_outil.revetement = revetement
        self.entree_outil.rayon_arrete = rayon_arrete
        self.entree_outil.angle_depouille = angle_depouille
        self.entree_outil.angle_axial = angle_axial
        self.entree_outil.angle_radial = angle_radial
        self.entree_outil.angle_attaque = angle_attaque
        self.entree_outil.angle_listel1 = angle_listel1
        self.entree_outil.angle_listel2 = angle_listel2

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.entree_outil.experience = experience[-1]
        else:
            self.entree_outil.experience = None

        session.add(self.entree_outil)
        session.commit()
        session.close()

    def get_types_outil(self):
        """Renvoie une liste des différents types d'outil' présents dans la base de données cutting

        Returns:
            type_outil : liste des type d'outil' différent"""

        types_outil = [type_outil[0] for type_outil in session.query(Entree_outil.type_outil).distinct()]
        session.close()
        return types_outil

    def get_matieres(self):
        """Renvoie une liste des différents types de matieres présents dans la base de données cutting

        Returns:
            type_outil : liste des type de matieres différent"""

        mats = [mat[0] for mat in session.query(Entree_outil.matiere).distinct()]
        session.close()
        return mats

    def get_revetements(self):
        """Renvoie une liste des différents types de revetement présents dans la base de données cutting

        Returns:
            revets : liste des type de revetements différent"""

        revets = [revet[0] for revet in session.query(Entree_outil.revetement).distinct()]
        session.close()
        return revets
