from model.Procede import Procede
from model import session
from model.Experience import Experience
from model import mydb


class ProcedeController:
    """Classe qui gère l'ajout d'un objet procede dans la base de données"""

    def __init__(self):
        """Constructeur de la classe ProcedeController"""
        self.procede = Procede()
        self.mycursor = mydb.cursor()

    def create_procede(self, type_procede, type_operation, assistance, debit_mql, debit_cryo, emulsion,
                       vitesse_coupe, vitesse_avance_dent, vitesse_avance_min, profondeur_passe,
                       engagement, frequence_rotation, nom_experience):
        """fonction qui ajoute un procede à la base de données

        Parameters
        ----------
        type_procede : string
            type de procédé utilisé
        type_operation : string
            type d'opération réalisée avec le procédé
        assistance : string
            assistance utilisée pendant le procédé
        debit_mql : float
            débit du fluide de coupe MQL utilisé pendant le procédé
        debit_cryo : float
            débit du fluide cryogénique utilisé pendant le procédé
        emulsion : float
            type d'émulsion utilisé pendant le procédé
        vitesse_coupe : float
            vitesse de coupe utilisée pendant le procédé
        vitesse_avance_dent : float
            vitesse d'avance par dent utilisée pendant le procédé
        vitesse_avance_min : float
            vitesse d'avance minimale utilisée pendant le procédé
        profondeur_passe : float
            profondeur de passe utilisée pendant le procédé
        engagement : float
            engagement utilisé pendant le procédé
        frequence_rotation : float
            fréquence de rotation utilisée pendant le procédé
        nom_experience : string
            nom de l'expérience associée au procédé.
        """

        # On remplit les propriétés de l'objet procede avec les valeurs passées en paramètre
        self.procede.type_procede = type_procede
        self.procede.type_operation = type_operation
        self.procede.assistance = assistance
        self.procede.debit_mql = debit_mql
        self.procede.debit_cryo = debit_cryo
        self.procede.emulsion = emulsion
        self.procede.vitesse_coupe = vitesse_coupe
        self.procede.vitesse_avance_dent = vitesse_avance_dent
        self.procede.vitesse_avance_min = vitesse_avance_min
        self.procede.profondeur_passe = profondeur_passe
        self.procede.engagement = engagement
        self.procede.frequence_rotation = frequence_rotation

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.procede.experience = experience[-1]
        else:
            self.procede.experience = None

        session.add(self.procede)
        session.commit()
        session.close()

    def get_types_procede(self):
        """Renvoie une liste des différents types de procede présents dans la base de données cutting

        Returns:
            type_procs : liste des type de procede différent"""

        type_procs = [type_proc[0] for type_proc in session.query(Procede.type_procede).distinct()]
        session.close()
        return type_procs

    def get_type_operation(self):
        """Renvoie une liste des différents types d'opération présents dans la base de données cutting

        Returns:
            type_ops : liste des type d'opérations différentes"""

        type_ops = [type_op[0] for type_op in session.query(Procede.type_operation).distinct()]
        session.close()
        return type_ops

    def get_assistance(self):
        """Renvoie une liste des différents types d'assistance présents dans la base de données cutting

        Returns:
            type_asss : liste des type d'assistances différentes"""

        type_asss = [type_ass[0] for type_ass in session.query(Procede.assistance).distinct()]
        session.close()
        return type_asss
