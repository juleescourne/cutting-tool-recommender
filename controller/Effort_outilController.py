from model import session
from model.Effort_outil import Effort_outil
from model.Entree_outil import Entree_outil
from model import mydb


class Effort_outilController:
    """Classe qui gère l'ajout d'un objet procede dans la base de données"""

    def __init__(self):
        """Constructeur de la classe createexperience"""
        self.effort_outil = Effort_outil()
        self.mycursor = mydb.cursor()

    def create_effort_outil(self, temps_effort_outil, fx, fy, fz, entree_outil):
        """fonction qui ajoute des efforts à la piece à la base de données

        Parameters
        ----------
        temps_effort_outil : float
            valeur de l'attribut 'temps_effort_outil' de la table Effort_outil
        fx : float
            valeur de l'attribut 'fx' de la table Effort_outil
        fy : float
            valeur de l'attribut 'fy' de la table Effort_outil
        fz : float
            valeur de l'attribut 'fz' de la table Effort_outil
        entree_outil : Entree_outil
            Objet entree_outil associe à la table Effort_outil
        """

        # On remplit les propriétés de l'objet Effort_outil avec les valeurs passées en paramètre
        self.effort_outil.temps_effort_outil = temps_effort_outil
        self.effort_outil.fx = fx
        self.effort_outil.fy = fy
        self.effort_outil.fz = fz

        if entree_outil is not None:
            entree = session.query(Entree_outil).filter_by(type_outil=entree_outil.type_outil,
                                                           matiere=entree_outil.matiere,
                                                           nb_dent_util=entree_outil.nb_dents_util,
                                                           revetement=entree_outil.revetement,
                                                           diametre=entree_outil.diametre,
                                                           rayon_arrete=entree_outil.rayon_arrete,
                                                           rayon_depouille=entree_outil.rayon_depouille,
                                                           angle_axial=entree_outil.angle_axial,
                                                           angle_radial=entree_outil.angle_radial,
                                                           angle_attaque=entree_outil.angle_attaque,
                                                           angle_listel1=entree_outil.angle_listel1,
                                                           angle_listel2=entree_outil.angle_listel2).all()
            if len(entree) != 0:
                self.effort_outil.entree_outil = entree[-1]
        else:
            self.effort_outil.entree_outil = None

        session.add(self.effort_outil)
        session.commit()
        session.close()
