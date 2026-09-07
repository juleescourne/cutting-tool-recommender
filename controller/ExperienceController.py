from model import mydb
from model.Experience import Experience
from tkinter.messagebox import showinfo
from model import session


class ExperienceController:
    """Classe qui gère l'ajout d'un objet experience dans la base de données"""

    def __init__(self):
        """Constructeur de la classe experiencecontroller"""
        self.experience = Experience()
        self.mycursor = mydb.cursor()

    def create_experience(self, nom):
        """fonction qui ajoute une expérience à la base de données

        Parameters
        ----------
        nom : str
            Le nom de l'expérience

        """
        self.experience.nom = nom
        session.add(self.experience)
        session.commit()
        session.close()

    def delete_experience(self):
        """fonction qui supprime la dernière expérience ajoutée à la base de données"""
        id_exp = None
        self.mycursor.execute("""select * from experience order by id desc limit 1""")
        experience = self.mycursor.fetchall()
        for x in experience:
            id_exp = x[0]

        if id_exp is not None:
            sql1 = """select * from procede where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (id_exp,))
            procedes = self.mycursor.fetchall()
            for x in procedes:
                sql2 = """delete from procede where id_procede = %s"""
                self.mycursor.execute(sql2, (x[0],))

            sql1 = """select * from copeaux where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (id_exp,))
            copeaux = self.mycursor.fetchall()
            for x in copeaux:
                sql2 = """delete from copeaux where id_copeaux = %s"""
                self.mycursor.execute(sql2, (x[0],))

            sql1 = """select * from entree_piece where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (id_exp,))
            entrees_pieces = self.mycursor.fetchall()
            for x in entrees_pieces:
                sql2 = """select * from sortie_piece where id_entree_piece = %s order by id"""
                self.mycursor.execute(sql2, (x[0],))
                sorties = self.mycursor.fetchall()
                for sortie in sorties:
                    sql3 = """delete from sortie_piece where id_sortie_piece = %s"""
                    self.mycursor.execute(sql3, (sortie[0],))

                sql4 = """select * from temperature_piece where id_entree_piece = %s order by id"""
                self.mycursor.execute(sql4, (x[0],))
                temps = self.mycursor.fetchall()
                for temp in temps:
                    sql5 = """delete from temperature_piece where id_temperature_piece = %s"""
                    self.mycursor.execute(sql5, (temp[0],))

                sql6 = """select * from effort_piece where id_entree_piece = %s order by id"""
                self.mycursor.execute(sql6, (x[0],))
                efforts = self.mycursor.fetchall()
                for effort in efforts:
                    sql7 = """delete from effort_piece where id_effort_piece = %s"""
                    self.mycursor.execute(sql7, (effort[0],))

                sql7 = """delete from entree_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql7, (x[0],))

            sql1 = """select * from entree_outil where id_experience = %s order by id"""
            self.mycursor.execute(sql1, (id_exp,))
            entrees_outils = self.mycursor.fetchall()
            for x in entrees_outils:
                sql2 = """select * from usure_outil where id_entree_outil = %s order by id"""
                self.mycursor.execute(sql2, (x[0],))
                usures = self.mycursor.fetchall()
                for usure in usures:
                    sql3 = """delete from usure_outil where id_usure_outil = %s"""
                    self.mycursor.execute(sql3, (usure[0],))

                sql4 = """select * from temperature_outil where id_entree_outil = %s order by id"""
                self.mycursor.execute(sql4, (x[0],))
                temps = self.mycursor.fetchall()
                for temp in temps:
                    sql5 = """delete from temperature_outil where id_temperature_outil = %s"""
                    self.mycursor.execute(sql5, (temp[0],))

                sql6 = """select * from effort_outil where id_entree_outil = %s order by id"""
                self.mycursor.execute(sql4, (x[0],))
                efforts = self.mycursor.fetchall()
                for effort in efforts:
                    sql7 = """delete from effort_outil where id_effort_outil = %s"""
                    self.mycursor.execute(sql7, (effort[0],))

            sql2 = """delete from experience where id = %s"""
            self.mycursor.execute(sql2, (id_exp,))
            mydb.commit()

            showinfo(title=None, message="Expérience supprimée")
        else:
            showinfo(title=None, message="Il n'y a aucune expérience dans la base de données")

    def get_nom_experience(self):
        """Renvoie une liste des noms des exerience dans la base de données cutting

        Returns:
            noms : liste des nom différent"""

        noms = [type_proc[0] for type_proc in session.query(Experience.nom).distinct()]
        session.close()
        return noms
