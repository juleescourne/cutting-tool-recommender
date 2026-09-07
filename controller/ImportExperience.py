import os
from tkinter.filedialog import askopenfile
import pandas as pd
from sqlalchemy import event
from controller.CopeauxController import CopeauxController
from controller.Effort_outilController import Effort_outilController
from controller.Effort_pieceController import Effort_pieceController
from controller.Entree_outilController import Entree_outilController
from controller.Entree_pieceController import Entree_pieceController
from controller.ExperienceController import ExperienceController
from controller.ProcedeController import ProcedeController
from controller.Sortie_pieceController import Sortie_pieceController
from controller.Temperature_outilController import Temperature_outilController
from controller.Temperature_pieceController import Temperature_pieceController
from controller.Usure_outilController import Usure_outilController
from model import mydb, engine
from utils import convert_effort
from tkinter.messagebox import showerror, showinfo


class ImportExperience:
    """Classe qui permet d'importer les données d'une expérience d'usinage dans la base de données"""

    def __init__(self):
        """Constructeur"""
        self.freq = None
        self.angle_attaque = None
        self.angle_radial = None
        self.angle_axial = None
        self.rep_file = None

        # On initialise les controllers necessaires
        self.experienceController = ExperienceController()
        self.entree_pieceController = Entree_pieceController()
        self.procedeController = ProcedeController()
        self.effort_pieceController = Effort_pieceController()
        self.temperature_pieceController = Temperature_pieceController()
        self.sortie_pieceController = Sortie_pieceController()
        self.copeauxController = CopeauxController()
        self.entree_outilController = Entree_outilController()
        self.temperature_outilController = Temperature_outilController()
        self.effort_outilController = Effort_outilController()
        self.usure_outilController = Usure_outilController()

        # path du fichier contenant les experiences
        self.chemin = ""

    def build_entree_outil(self, index, value):
        """Fonction qui recupère les valeurs a inserer dans entree_outil en fonction de l'index du fichier

        Parameters
        ----------
        index : int
            index du fichier csv contenant les données
        value : any
            La valeur de la cellule a l'index

        """
        if index == 0:
            self.entree_outilController.entree_outil.type_outil = value
        if index == 1:
            self.entree_outilController.entree_outil.matiere = value
        if index == 2:
            self.entree_outilController.entree_outil.diametre = value
        if index == 3:
            self.entree_outilController.entree_outil.nb_dents_util = value
        if index == 4:
            self.entree_outilController.entree_outil.revetement = value
        if index == 5:
            self.entree_outilController.entree_outil.rayon_arrete = value.split(' ')[0]
        if index == 6:
            self.entree_outilController.entree_outil.angle_depouille = value
        if index == 7:
            self.entree_outilController.entree_outil.angle_axial = value
        if index == 8:
            self.entree_outilController.entree_outil.angle_radial = value
        if index == 9:
            self.entree_outilController.entree_outil.angle_attaque = value
        if index == 10:
            self.entree_outilController.entree_outil.angle_listel1 = value
        if index == 11:
            self.entree_outilController.entree_outil.angle_listel2 = value

    def build_entree_piece(self, index, value):
        """Fonction qui recupère les valeurs a inserer dans entree_piece en fonction de l'index du fichier

        Parameters
        ----------
        index : int
            index du fichier csv contenant les données
        value : any
            La valeur de la cellule a l'index

        """
        if index == 0:
            self.entree_pieceController.entree_piece.type_matiere = value
        if index == 1:
            self.entree_pieceController.entree_piece.materiaux = value
        if index == 2:
            self.entree_pieceController.entree_piece.procede_elaboration = value
        if index == 3:
            self.entree_pieceController.entree_piece.impression_3d = value
        if index == 4:
            self.entree_pieceController.entree_piece.longueur_usinee = value
        if index == 5:
            self.entree_pieceController.entree_piece.num_passe = value

    def build_procede(self, index, value):
        """Fonction qui recupère les valeurs a inserer dans procede en fonction de l'index du fichier

        Parameters
        ----------
        index : int
            index du fichier csv contenant les données
        value : any
            La valeur de la cellule a l'index

        """
        if index == 0:
            self.procedeController.procede.type_procede = value
        if index == 1:
            self.procedeController.procede.type_operation = value
        if index == 2:
            self.procedeController.procede.assistance = value
        if index == 3:
            self.procedeController.procede.debit_mql = value
        if index == 4:
            self.procedeController.procede.debit_cryo = value
        if index == 5:
            self.procedeController.procede.emulsion = value
        if index == 6:
            self.procedeController.procede.vitesse_coupe = value
        if index == 7:
            self.procedeController.procede.vitesse_avance_dent = value
        if index == 8:
            self.procedeController.procede.profondeur_passe = value
        if index == 9:
            self.procedeController.procede.engagement = value
        if index == 10:
            self.procedeController.procede.frequence_rotation = value
        if index == 11:
            self.procedeController.procede.vitesse_avance_min = value

    def build_entree(self):
        """Fonction qui insère en base de données les entrees de l'experience (piece, outil et procede) """

        # on insere une experience en base de données avec le nom du fichier
        self.experienceController.create_experience(os.path.basename(self.chemin)[0:-5])

        mycursor = mydb.cursor()

        # on recupere l'id de l'experience
        id_exp = None
        # mycursor.execute("""select * from experience order by id_experience desc limit 1""")
        mycursor.execute("""select id_experience from experience""")
        experience = mycursor.fetchall()
        print(experience[-1][0])
        id_exp = experience[-1][0]
        # print(id_exp)

        # lecture du fichier
        xl_file = pd.read_excel(self.chemin, sheet_name='NEW2', skiprows=1, na_filter=False)
        xl_file = xl_file.replace('', None)

        # construction des donnees d'entrees
        for index, row in xl_file.iterrows():
            if row.values[1] is not None and index <= 11:
                self.build_entree_outil(index, row.values[1])
            if row.values[4] is not None and index <= 5:
                self.build_entree_piece(index, row.values[4])
            if row.values[6] is not None and index <= 11:
                self.build_procede(index, row.values[6])


        # insertion de l'objet entree_piece en base de donnees
        entree_p = pd.DataFrame({
            'type_matiere': [self.entree_pieceController.entree_piece.type_matiere],
            'materiaux': [self.entree_pieceController.entree_piece.materiaux],
            'procede_elaboration': [self.entree_pieceController.entree_piece.procede_elaboration],
            'impression_3d': [self.entree_pieceController.entree_piece.impression_3d],
            'longueur_usinee': [self.entree_pieceController.entree_piece.longueur_usinee],
            'num_passe': [self.entree_pieceController.entree_piece.num_passe],
            'id_experience': [id_exp]
        })
        entree_p.to_sql('entree_piece', engine, index=False, if_exists="append")

        # insertion de l'objet entree_outil en base de donnees
        entree_o = pd.DataFrame({
            'type_outil': [self.entree_outilController.entree_outil.type_outil],
            'matiere': [self.entree_outilController.entree_outil.matiere],
            'diametre': [self.entree_outilController.entree_outil.diametre],
            'nb_dents_util': [self.entree_outilController.entree_outil.nb_dents_util],
            'revetement': [self.entree_outilController.entree_outil.revetement],
            'rayon_arrete': [self.entree_outilController.entree_outil.rayon_arrete],
            'angle_depouille': [self.entree_outilController.entree_outil.angle_depouille],
            'angle_axial': [self.entree_outilController.entree_outil.angle_axial],
            'angle_radial': [self.entree_outilController.entree_outil.angle_radial],
            'angle_attaque': [self.entree_outilController.entree_outil.angle_attaque],
            'angle_listel1': [self.entree_outilController.entree_outil.angle_listel1],
            'angle_listel2': [self.entree_outilController.entree_outil.angle_listel2],
            'id_experience': [id_exp]
        })
        entree_o.to_sql('entree_outil', engine, index=False, if_exists="append")

        # insertion de l'objet procede en base de donnees
        procede = pd.DataFrame({
            'type_procede': [self.procedeController.procede.type_procede],
            'type_operation': [self.procedeController.procede.type_operation],
            'assistance': [self.procedeController.procede.assistance],
            'debit_mql': [self.procedeController.procede.debit_mql],
            'debit_cryo': [self.procedeController.procede.debit_cryo],
            'emulsion': [self.procedeController.procede.emulsion],
            'vitesse_coupe': [self.procedeController.procede.vitesse_coupe],
            'vitesse_avance_dent': [self.procedeController.procede.vitesse_avance_dent],
            'profondeur_passe': [self.procedeController.procede.profondeur_passe],
            'engagement': [self.procedeController.procede.engagement],
            'vitesse_avance_min': [self.procedeController.procede.vitesse_avance_min],
            'frequence_rotation': [self.procedeController.procede.frequence_rotation],
            'id_experience': [id_exp]
        })
        procede.to_sql('procede', engine, index=False, if_exists="append")

        mydb.commit()

    def convert(self, value):
        """
        Convertie une valeur en float
        :param value: la valeur à convertir
        :return: value: la valeur flottante
        """
        if isinstance(value, str):
            return float(value.replace(',', '.'))
        return value

    def get_angle_in_radian(self):
        """ Récupère les valeurs des angles en radians"""
        xl_file = pd.read_excel(self.chemin, sheet_name='NEW2', skiprows=1, na_filter=False)
        xl_file = xl_file.replace('', None)
        for index, row in xl_file.iterrows():
            if row.values[2] is not None and index == 7:
                self.angle_axial = self.convert(row.values[2])
            if row.values[2] is not None and index == 8:
                self.angle_radial = self.convert(row.values[2])
            if row.values[2] is not None and index == 9:
                self.angle_attaque = self.convert(row.values[2])
            if row.values[6] is not None and index == 10:
                self.freq = self.convert(row.values[6])

    def build_sorties(self):
        """Fonction qui insère en base de données les valeurs de sorties contenu dans le fichier excel"""

        mycursor = mydb.cursor()

        # On récupère l'id de l'objet entree_piece en base de données
        mycursor.execute("""select id_entree_piece from entree_piece order by id_entree_piece desc limit 1""")
        piece = mycursor.fetchall()
        id_entree_piece = piece[-1]

        # On récupère l'id de l'objet entree_outil en base de données
        mycursor.execute("""select id_entree_outil from entree_outil order by id_entree_outil desc limit 1""")
        outil = mycursor.fetchall()
        id_entree_outil = outil[-1]

        # On récupère l'id de l'objet experience en base de données
        mycursor.execute("""select id_experience from experience order by id_experience desc limit 1""")
        experience = mycursor.fetchall()
        id_exp = experience[-1]

        # on lit le fichier contenant les données
        data = pd.read_excel(self.chemin, sheet_name='NEW2', skiprows=18, na_filter=False)
        data = data.replace('', None)

        # tableaux contenant les données à insérer
        temps_effort_piece = []
        fx = []
        fy = []
        fz = []

        # on récupère les valeurs des attributs de la table effort_piece
        for i, j, k, p in zip(data.iloc[:, 0].tolist(), data.iloc[:, 1].tolist(), data.iloc[:, 2].tolist(),
                              data.iloc[:, 3].tolist()):
            if i is not None and j is not None and p is not None and k is not None:
                if self.convert(j) != 0 or self.convert(k) != 0 or self.convert(p) != 0:
                    temps_effort_piece.append(self.convert(i))
                    fx.append(self.convert(j))
                    fy.append(self.convert(k))
                    fz.append(self.convert(p))

        # creation du dataframe contenant les valeurs des efforts a la piece
        effort_p = pd.DataFrame({
            'temps_effort_piece': temps_effort_piece,
            'fx': fx,
            'fy': fy,
            'fz': fz,
            'id_entree_piece': [id_entree_piece for _ in range(len(temps_effort_piece))]
        })

        # insertion en base de données des efforts à la piece
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        effort_p.to_sql('effort_piece', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        temps_effort_outil = []
        fx = []
        fy = []
        fz = []
        self.get_angle_in_radian()

        # on récupère les valeurs des attributs de la table effort_outil
        for i, j, k, p in zip(data.iloc[:, 0].tolist(), data.iloc[:, 1].tolist(), data.iloc[:, 2].tolist(),
                              data.iloc[:, 3].tolist()):
            if i is not None and j is not None and p is not None and k is not None:
                if self.convert(j) != 0 or self.convert(k) != 0 or self.convert(p) != 0:
                    temps_effort_outil.append(self.convert(i))
                    x, y, z = convert_effort(self.convert(j), self.convert(p), self.convert(k), self.freq,
                                             self.angle_radial, self.angle_axial, self.angle_attaque)
                    fx.append(x)
                    fy.append(y)
                    fz.append(z)

        # creation du dataframe contenant les valeurs des efforts a l'outil
        effort_o = pd.DataFrame({
            'temps_effort_outil': temps_effort_outil,
            'fx': fx,
            'fy': fy,
            'fz': fz,
            'id_entree_outil': [id_entree_outil for _ in range(len(temps_effort_outil))]
        })

        # insertion en base de données des efforts à l'outil
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        effort_o.to_sql('effort_outil', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        temps_temperature_piece = []
        temperature_piece = []

        # on récupère les valeurs des attributs de la table temperature_piece
        for i, j in zip(data.iloc[:, 4].tolist(), data.iloc[:, 5].tolist()):
            if i is not None and j is not None:
                temps_temperature_piece.append(self.convert(i))
                temperature_piece.append(self.convert(j))

        # creation du dataframe contenant les valeurs des temperatures a la piece
        temp_p = pd.DataFrame({
            'temps_temperature_piece': temps_temperature_piece,
            'temperature_piece': temperature_piece,
            'id_entree_piece': [id_entree_piece] * len(temps_temperature_piece)
        })

        # insertion en base de données des temperatures a la piece
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        temp_p.to_sql('temperature_piece', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        rugosite = []
        durete = []
        limite_endurance = []
        contrainte_residuelle = []

        # on récupère les valeurs des attributs de la table sortie_piece
        for i, j, p, k in zip(data.iloc[:, 9].tolist(), data.iloc[:, 8].tolist(), data.iloc[:, 7].tolist(),
                              data.iloc[:, 6].tolist()):
            if i is not None or j is not None or p is not None or k is not None:
                rugosite.append(self.convert(i))
                durete.append(self.convert(j))
                limite_endurance.append(self.convert(p))
                contrainte_residuelle.append(self.convert(k))

        # creation du dataframe contenant les valeurs des sorties a la piece
        sortie_p = pd.DataFrame({
            'rugosite': rugosite,
            'durete': durete,
            'limite_endurance': limite_endurance,
            'contrainte_residuelle': contrainte_residuelle,
            'id_entree_piece': [id_entree_piece for _ in range(
                max(len(rugosite), len(durete), len(limite_endurance),
                    len(contrainte_residuelle)))]
        })

        # insertion en base de données des sorties a la piece
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        sortie_p.to_sql('sortie_piece', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        temps_usinage = []
        vb = []
        er = []
        kt = []

        # on récupère les valeurs des attributs de la table usure_outil
        for i, j, p, k in zip(data.iloc[:, 10].tolist(), data.iloc[:, 11].tolist(), data.iloc[:, 12].tolist(),
                              data.iloc[:, 13].tolist()):
            if i is not None or j is not None or p is not None or k is not None:
                temps_usinage.append(self.convert(i))
                vb.append(self.convert(j))
                er.append(self.convert(p))
                kt.append(self.convert(k))

        # creation du dataframe contenant les valeurs d'usure à l'outil
        usure_o = pd.DataFrame({
            'temps_usinage': temps_usinage,
            'vb': vb,
            'Er': er,
            'Kt': kt,
            'id_entree_outil': [id_entree_outil for _ in range(
                max(len(vb), len(er), len(kt), len(temps_usinage)))]
        })

        # insertion en base de données des valeurs d'usure à l'outil
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        usure_o.to_sql('usure_outil', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        temps_temperature_outil = []
        temperature_outil = []

        # on récupère les valeurs des attributs de temperature a l'outil
        for i, j in zip(data.iloc[:, 14].tolist(), data.iloc[:, 15].tolist()):
            if i is not None and j is not None:
                temps_temperature_outil.append(self.convert(i))
                temperature_outil.append(self.convert(j))

        # creation du dataframe contenant les valeurs de temperature a l'outil
        temp_o = pd.DataFrame({
            'temps_temperature_outil': temps_temperature_outil,
            'temperature_outil': temperature_outil,
            'id_entree_outil': [id_entree_outil for _ in range(len(temps_temperature_outil))]
        })

        # insertion en base de données des valeurs de temperature a l'outil
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        temp_o.to_sql('temperature_outil', engine, index=False, if_exists="append")

        # tableau contenant les données à insérer
        epaisseur = []

        # on récupère les valeurs des attributs concernant les copeaux
        for i in data.iloc[:, 16].tolist():
            if i is not None:
                epaisseur.append(self.convert(i))

        # creation du dataframe contenant les valeurs concernant les copeaux
        copeaux = pd.DataFrame({
            'epaisseur': epaisseur,
            'id_experience': [id_exp] * len(epaisseur)
        })
        copeaux.to_sql('copeaux', engine, index=False, if_exists="append")

        # tableaux contenant les données à insérer
        temps_vibration = []
        frequence = []
        amplitude = []

        # on récupère les valeurs des attributs de vibration
        for i, j, k in zip(data.iloc[:, 17].tolist(), data.iloc[:, 18].tolist(), data.iloc[:, 19].tolist()):
            if i is not None and (j is not None or k is not None):
                temps_vibration.append(self.convert(i))
                frequence.append(self.convert(j))
                amplitude.append(self.convert(k))

        # creation du dataframe contenant les valeurs de vibration
        vib = pd.DataFrame({
            'temps_vibration': temps_vibration,
            'frequence': frequence,
            'amplitude': amplitude,
            'id_entree_outil': [id_entree_outil] * max(len(temps_vibration), len(frequence), len(amplitude)),
            'id_entree_piece': [id_entree_piece] * max(len(temps_vibration), len(frequence), len(amplitude))
        })

        # insertion en base de données des valeurs de vibration
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(
                conn, cursor, statement, params, context, executemany
        ):
            if executemany:
                cursor.fast_executemany = True
        vib.to_sql('vibration', engine, index=False, if_exists="append")

        mydb.commit()

    def main_import(self):
        """ouverture de la boite de dialogue pour selection du fichier rep_file"""
        self.rep_file = askopenfile(mode="r", filetypes=[("Fichiers excel", ".xlsx")], defaultextension=".xlsx",
                                    title="Lire un fichier excel")
        if self.rep_file is None:  # si appuie sur annuler
            pass
        else:
            try:
                self.chemin = os.path.abspath(self.rep_file.name)
                self.build_entree()
                self.build_sorties()
                showinfo(title="Info", message="Experience importé")
            except:
                showerror(title="Erreur", message="Mauvais format de fichier")
