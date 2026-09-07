from model import session
from model.Usure_outil import Usure_outil
from model.Entree_outil import Entree_outil
from model import mydb


class Usure_outilController:
    """Classe qui gère l'ajout d'un objet usure_outil dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Usure_outilController"""
        self.usure_outil = Usure_outil()
        self.mycursor = mydb.cursor()

    def create_usure_outil(self, temps_usinage, vb, er, kt, entree_outil):
        """fonction qui ajoute un objet usure_outil à la base de données

        Parameters
        ----------
        temps_usinage : float
            valeur de l'attribut 'temps_usinage' de la table usure_outil
        vb : float
            valeur de l'attribut 'vb' de la table usure_outil
        er : float
            valeur de l'attribut 'er' de la table usure_outil
        kt : Entree_piece
           valeur de l'attribut 'kt' de la table usure_outil
        entree_outil : Entree_outil
           Objet Entree_outil associé à la table usure_outil
        """
        self.usure_outil.temps_usinage = temps_usinage
        self.usure_outil.vb = vb
        self.usure_outil.er = er
        self.usure_outil.kt = kt

        # Récupération de l'objet entree_outil dans la base de données
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
                self.usure_outil.entree_outil = entree[-1]
        else:
            self.usure_outil.entree_outil = None

        session.add(self.usure_outil)
        session.commit()
        session.close()
