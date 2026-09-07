from model import session
from model.Entree_outil import Entree_outil
from model.Entree_piece import Entree_piece
from model import mydb
from model.Vibration import Vibration


class VibrationController:
    """Classe qui gère l'ajout d'un objet vibration dans la base de données"""

    def __init__(self):
        """Constructeur de la classe VibrationController"""
        self.vibration = Vibration()
        self.mycursor = mydb.cursor()

    def create_vibration(self, temps_vibration, frequence, amplitude, entree_outil, entree_piece):
        """fonction qui ajoute un objet vibration à la base de données

        Parameters
        ----------
        temps_vibration : float
            valeur de l'attribut 'temps_vibration' de la table vibration
        frequence : float
            valeur de l'attribut 'frequence' de la table vibration
        amplitude : float
            valeur de l'attribut 'amplitude' de la table vibration
        entree_outil : Entree_outil
           Objet Entree_outil associé à la table vibration
        entree_piece : Entree_piece
           Objet Entree_piece associé à la table vibration
        """

        self.vibration.temps_vibration = temps_vibration
        self.vibration.frequence = frequence
        self.vibration.amplitude = amplitude

        # Récupération des objets entree_piece et entree_outil dans la base de données
        if entree_outil is not None and entree_piece is not None:
            entree_o = session.query(Entree_outil).filter_by(type_outil=entree_outil.type_outil,
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

            entree_p = session.query(Entree_piece).filter_by(type_matiere=entree_piece.type_matiere,
                                                             materiaux=entree_piece.materiaux,
                                                             procede_elaboration=entree_piece.procede_elaboration
                                                             , impression_3d=entree_piece.impression_3d,
                                                             longueur_usinee=entree_piece.longueur_usinee
                                                             , num_passe=entree_piece.num_passe).all()
            if len(entree_o) != 0 and len(entree_p) != 0:
                self.vibration.entree_outil = entree_o[-1]
                self.vibration.entree_piece = entree_p[-1]
        else:
            self.vibration.entree_outil = None
            self.vibration.entree_piece = None

        session.add(self.vibration)
        session.commit()
        session.close()
