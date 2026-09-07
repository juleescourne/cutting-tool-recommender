from model import session
from model.Temperature_outil import Temperature_outil
from model.Entree_outil import Entree_outil
from model import mydb


class Temperature_outilController:
    """Classe qui gère l'ajout d'un objet temperature_outil dans la base de données"""

    def __init__(self):
        """Constructeur de la classe Temperature_outilController"""
        self.temperature_outil = Temperature_outil()
        self.mycursor = mydb.cursor()

    def create_temperature_outil(self, temps_temperature_outil, temperature_outil, entree_outil):
        """Fonction qui ajoute une température d'outil à la base de données

        Parameters
        ----------
        temps_temperature_outil : float
            Le temps auquel la température d'outil est mesurée (en secondes)
        temperature_outil : float
            La valeur de la température d'outil mesurée (en degrés Celsius)
        entree_outil : Entree_outil
            L'objet Entree_outil correspondant à l'outil utilisé pour l'usinage

        """
        # On remplit les propriétés de l'objet Temperature_outil avec les valeurs passées en paramètre
        self.temperature_outil.temps_temperature_outil = temps_temperature_outil
        self.temperature_outil.temperature_outil = temperature_outil

        # Si un objet Entree_outil est passé en paramètre, on cherche l'objet correspondant dans la base de données
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
                self.temperature_outil.entree_outil = entree[-1]
        else:
            self.temperature_outil.entree_outil = None

        session.add(self.temperature_outil)
        session.commit()
        session.close()
