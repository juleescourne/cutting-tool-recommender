from model.Entree_piece import Entree_piece
from model import session
from model.Experience import Experience
from model import mydb


class Entree_pieceController:
    """Classe qui gère l'ajout d'un objet procede dans la base de données"""

    def __init__(self):
        """Constructeur de la classe createexperience"""
        self.entree_piece = Entree_piece()
        self.mycursor = mydb.cursor()

    def create_entree_piece(self, type_matiere, materiaux, procede_elaboration, impression_3d, longueur_usinee,
                            num_passe, nom_experience):
        """fonction qui ajoute un procede à la base de données

        Parameters
        ----------
        type_matiere : string
            type de matiere de l'objet entree_piece
        materiaux : string
            materiaux de l'objet entree_piece
        procede_elaboration : string
            procede d'elaboration de l'objet entree_piece
        impression_3d : string
            impression 3d de l'objet entree_piece
        longueur_usinee : float
            longueur de la piece a usinee
        num_passe : int
            numero de passe
        nom_experience : string
            nom de l'experience associe
        """

        # On remplit les propriétés de l'objet entree_piece avec les valeurs passées en paramètre
        self.entree_piece.type_matiere = type_matiere
        self.entree_piece.materiaux = materiaux
        self.entree_piece.procede_elaboration = procede_elaboration
        self.entree_piece.impression_3d = impression_3d
        self.entree_piece.longueur_usinee = longueur_usinee
        self.entree_piece.num_passe = num_passe

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.entree_piece.experience = experience[-1]
        else:
            self.entree_piece.experience = None

        session.add(self.entree_piece)
        session.commit()
        session.close()

    def get_types_matiere(self):
        """Renvoie une liste des différents types de matieres présents dans la base de données cutting

        Returns:
            type_procs : liste des type de procede différent"""

        type_mats = [type_mat[0] for type_mat in session.query(Entree_piece.type_matiere).distinct()]
        session.close()
        return type_mats

    def get_materiaux(self):
        """Renvoie une liste des différents materiaux présents dans la base de données cutting

        Returns:
            type_procs : liste des type de procede différent"""

        mats = [mat[0] for mat in session.query(Entree_piece.materiaux).distinct()]
        session.close()
        return mats

    def get_procede_elaboration(self):
        """Renvoie une liste des différents types de procede présents dans la base de données cutting

        Returns:
            type_procs : liste des type de procede différent"""

        procs = [proc[0] for proc in session.query(Entree_piece.procede_elaboration).distinct()]
        session.close()
        return procs

    def average_temperature(self):
        """Renvoie la moyenne des temperatures a la piece

        Returns:
            average : la temperature moyenne"""

        sql1 = """select id_entree_piece from entree_piece where (type_matiere = %s AND 
        materiaux = %s AND procede_elaboration = %s AND impression_3d = %s AND
        longueur_usinee = %s AND num_passe = %s)"""
        self.mycursor.execute(sql1, (self.entree_piece.type_matiere,self.entree_piece.materiaux, self.entree_piece.procede_elaboration,
                                     self.entree_piece.impression_3d, self.entree_piece.longueur_usinee, self.entree_piece.num_passe))
        id_entree = self.mycursor.fetchall()

        sql2 = """select temperature from temperature_piece where id_entree_piece = %s"""
        self.mycursor.execute(sql2, (id_entree,))
        temps = self.mycursor.fetchall()
        sum_temp = 0
        for temp in temps:
            sum_temp += temp
        average = sum_temp / len(temps)
        return average
