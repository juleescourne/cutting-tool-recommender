from model import session, mydb
from model.Experience import Experience


class Switcher(object):
    """Classe qui gère l'association entre une chaîne de caractère et une liste de valeurs"""

    def __init__(self):
        """Constructeur"""
        self.mycursor = mydb.cursor()
        self.mycursor.execute("""select * from experience order by id_experience desc limit 1""")
        experiences = self.mycursor.fetchall()
        self.experience = None
        for x in experiences:
            self.experience = x[0]

    def indirect(self, name):
        method_name = str(name)
        method = getattr(self, method_name, lambda: "")
        return method()

    def type_procede(self):
        """Récupération des valeurs de l'attribut type_procede de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select type_procede from procede where id_experience = %s"""
            print(self.experience)
            self.mycursor.execute(sql1, (self.experience,))
            type_procede = self.mycursor.fetchall()
            for x in type_procede:
                result.append(x[0])
        return result

    def type_operation(self):
        """Récupération des valeurs de l'attribut type_operation de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT type_operation FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            type_op = self.mycursor.fetchall()
            for x in type_op:
                result.append(x[0])
        return result

    def assistance(self):
        """Récupération des valeurs de l'attribut assistance de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT assistance FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            assist = self.mycursor.fetchall()
            for x in assist:
                result.append(x[0])
        return result

    def debit_mql(self):
        """Récupération des valeurs de l'attribut debit_mql de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT debit_mql FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            debit = self.mycursor.fetchall()
            for x in debit:
                result.append(x[0])
        return result

    def debit_cryo(self):
        """Récupération des valeurs de l'attribut debit_cryo de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT debit_cryo FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            debit = self.mycursor.fetchall()
            for x in debit:
                result.append(x[0])
        return result

    def emulsion(self):
        """Récupération des valeurs de l'attribut emulsion de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT emulsion FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            emul = self.mycursor.fetchall()
            for x in emul:
                result.append(x[0])
        return result

    def vitesse_coupe(self):
        """Récupération des valeurs de l'attribut vitesse_coupe de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT vitesse_coupe FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            vit = self.mycursor.fetchall()
            for x in vit:
                result.append(x[0])
        return result

    def vitesse_avance_dent(self):
        """Récupération des valeurs de l'attribut vitesse_avance_dent de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT vitesse_avance_dent FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            vit = self.mycursor.fetchall()
            for x in vit:
                result.append(x[0])
        return result

    def vitesse_avance_min(self):
        """Récupération des valeurs de l'attribut vitesse_avance_min de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT vitesse_avance_min FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            vit = self.mycursor.fetchall()
            for x in vit:
                result.append(x[0])
        return result

    def profondeur_passe(self):
        """Récupération des valeurs de l'attribut profondeur_passe de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT profondeur_passe FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            prof = self.mycursor.fetchall()
            for x in prof:
                result.append(x[0])
        return result

    def engagement(self):
        """Récupération des valeurs de l'attribut engagement de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT engagement FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            eng = self.mycursor.fetchall()
            for x in eng:
                result.append(x[0])
        return result

    def frequence_rotation(self):
        """Récupération des valeurs de l'attribut frequence_rotation de la table procede associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT frequence_rotation FROM procede WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            freq = self.mycursor.fetchall()
            for x in freq:
                result.append(x[0])
        return result

    def epaisseur_copeaux(self):
        """Récupération des valeurs de l'attribut epaisseur de la table copeaux associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT epaisseur FROM copeaux WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            cop = self.mycursor.fetchall()
            for x in cop:
                result.append(x[0])
        return result

    def type_matiere_piece(self):
        """Récupération des valeurs de l'attribut type_matiere de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT type_matiere FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            mat = self.mycursor.fetchall()
            for x in mat:
                result.append(x[0])
        return result

    def materiaux_piece(self):
        """Récupération des valeurs de l'attribut materiaux de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT materiaux FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            mat = self.mycursor.fetchall()
            for x in mat:
                result.append(x[0])
        return result

    def procede_elaboration(self):
        """Récupération des valeurs de l'attribut procede_elaboration de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT procede_elaboration FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            proc = self.mycursor.fetchall()
            for x in proc:
                result.append(x[0])
        return result

    def impression_3d(self):
        """Récupération des valeurs de l'attribut impression_3d de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT impression_3d FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            imp = self.mycursor.fetchall()
            for x in imp:
                result.append(x[0])
        return result

    def longueur_usinee(self):
        """Récupération des valeurs de l'attribut longueur_usinee de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT longueur_usinee FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            long = self.mycursor.fetchall()
            for x in long:
                result.append(x[0])
        return result

    def num_passe(self):
        """Récupération des valeurs de l'attribut num_passe de la table entree_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT num_passe FROM entree_piece WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            np = self.mycursor.fetchall()
            for x in np:
                result.append(x[0])
        return result

    def type_outil(self):
        """Récupération des valeurs de l'attribut type_outil de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT type_outil FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            out = self.mycursor.fetchall()
            for x in out:
                result.append(x[0])
        return result

    def matiere_outil(self):
        """Récupération des valeurs de l'attribut matiere_outil de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT matiere FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            mat = self.mycursor.fetchall()
            for x in mat:
                result.append(x[0])
        return result

    def diametre_outil(self):
        """Récupération des valeurs de l'attribut diametre_outil de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT diametre FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            diam = self.mycursor.fetchall()
            for x in diam:
                result.append(x[0])
        return result

    def nb_dents_util_outil(self):
        """Récupération des valeurs de l'attribut nb_dents_util de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT nb_dents_util FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            nb_dents = self.mycursor.fetchall()
            for x in nb_dents:
                result.append(x[0])
        return result

    def revetement_outil(self):
        """Récupération des valeurs de l'attribut revetement de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT revetement FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            rev = self.mycursor.fetchall()
            for x in rev:
                result.append(x[0])
        return result

    def rayon_arrete_outil(self):
        """Récupération des valeurs de l'attribut rayon_arrete de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT rayon_arrete FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            rayon = self.mycursor.fetchall()
            for x in rayon:
                result.append(x[0])
        return result

    def angle_depouille_outil(self):
        """Récupération des valeurs de l'attribut angle_depouille de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_depouille FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            angle = self.mycursor.fetchall()
            for x in angle:
                result.append(x[0])
        return result

    def angle_axial_outil(self):
        """Récupération des valeurs de l'attribut angle_axial de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_axial FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            angle = self.mycursor.fetchall()
            for x in angle:
                result.append(x[0])
        return result

    def angle_radial(self):
        """Récupération des valeurs de l'attribut angle_radial de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_radial FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            out = self.mycursor.fetchall()
            for x in out:
                result.append(x[0])
        return result

    def angle_attaque(self):
        """Récupération des valeurs de l'attribut angle_attaque de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_attaque FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            out = self.mycursor.fetchall()
            for x in out:
                result.append(x[0])
        return result

    def angle_listel1(self):
        """Récupération des valeurs de l'attribut angle_listel1 de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_listel1 FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            out = self.mycursor.fetchall()
            for x in out:
                result.append(x[0])
        return result

    def angle_listel2(self):
        """Récupération des valeurs de l'attribut angle_listel2 de la table entree_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql = """SELECT angle_listel2 FROM entree_outil WHERE id_experience = %s"""
            self.mycursor.execute(sql, (self.experience,))
            out = self.mycursor.fetchall()
            for x in out:
                result.append(x[0])
        return result

    def rugosite(self):
        """Récupération des valeurs de l'attribut rugosite de la table sortie_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select rugosite from sortie_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                rug = self.mycursor.fetchall()
                for x in rug:
                    result.append(x[0])
        return result

    def durete(self):
        """Récupération des valeurs de l'attribut durete de la table sortie_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select durete from sortie_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                durete = self.mycursor.fetchall()
                for x in durete:
                    result.append(x[0])
        return result

    def limite_endurance(self):
        """Récupération des valeurs de l'attribut limite_endurance de la table sortie_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select limite_endurance from sortie_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                lim_end = self.mycursor.fetchall()
                for x in lim_end:
                    result.append(x[0])
        return result

    def contrainte_residuelle(self):
        """Récupération des valeurs de l'attribut contrainte_residuelle de la table sortie_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select contrainte_residuelle from sortie_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                contr_res = self.mycursor.fetchall()
                for x in contr_res:
                    result.append(x[0])
        return result

    def temps_temperature_piece(self):
        """Récupération des valeurs de l'attribut temps_temperature_piece de la table temperature_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select temps_temperature_piece from temperature_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def temperature_piece(self):
        """Récupération des valeurs de l'attribut temperature_piece de la table temperature_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select temperature_piece from temperature_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def temps_effort_piece(self):
        """Récupération des valeurs de l'attribut temps_effort_piece de la table effort_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select temps_effort_piece from effort_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def fx_piece(self):
        """Récupération des valeurs de l'attribut fx de la table effort_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select fx from effort_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fx = self.mycursor.fetchall()
                for x in fx:
                    result.append(x[0])
        return result

    def fy_piece(self):
        """Récupération des valeurs de l'attribut fy de la table effort_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select fy from effort_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fy = self.mycursor.fetchall()
                for x in fy:
                    result.append(x[0])
        return result

    def fz_piece(self):
        """Récupération des valeurs de l'attribut fz de la table effort_piece associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_piece:
                sql2 = """select fz from effort_piece where id_entree_piece = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fz = self.mycursor.fetchall()
                for x in fz:
                    result.append(x[0])
        return result

    def temps_effort_outil(self):
        """Récupération des valeurs de l'attribut temps_effort_outil de la table effort_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select temps_effort_outil from effort_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def fx_outil(self):
        """Récupération des valeurs de l'attribut fx de la table effort_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select fx from effort_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fx = self.mycursor.fetchall()
                for x in fx:
                    result.append(x[0])
        return result

    def fy_outil(self):
        """Récupération des valeurs de l'attribut fy de la table effort_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select fy from effort_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fy = self.mycursor.fetchall()
                for x in fy:
                    result.append(x[0])
        return result

    def fz_outil(self):
        """Récupération des valeurs de l'attribut fz de la table effort_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select fz from effort_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                fz = self.mycursor.fetchall()
                for x in fz:
                    result.append(x[0])
        return result

    def temps_temperature_outil(self):
        """Récupération des valeurs de l'attribut temps_temperature_outil de la table temperature_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select temps_temperature_outil from temperature_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def temperature_outil(self):
        """Récupération des valeurs de l'attribut temperature_outil de la table temperature_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select temperature_outil from temperature_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def temps_usinage(self):
        """Récupération des valeurs de l'attribut temps_usinage de la table usure_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select temps_usinage from usure_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                temp = self.mycursor.fetchall()
                for x in temp:
                    result.append(x[0])
        return result

    def vb(self):
        """Récupération des valeurs de l'attribut vb de la table usure_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select vb from usure_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                vb = self.mycursor.fetchall()
                for x in vb:
                    result.append(x[0])
        return result

    def er(self):
        """Récupération des valeurs de l'attribut er de la table usure_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select Er from usure_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                er = self.mycursor.fetchall()
                for x in er:
                    result.append(x[0])
        return result

    def kt(self):
        """Récupération des valeurs de l'attribut kt de la table usure_outil associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            for i in entree_outil:
                sql2 = """select Kt from usure_outil where id_entree_outil = %s"""
                self.mycursor.execute(sql2, (i[0],))
                kt = self.mycursor.fetchall()
                for x in kt:
                    result.append(x[0])
        return result

    def temps_vibration(self):
        """Récupération des valeurs de l'attribut temps_vibration de la table vibration associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            sql2 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql2, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_outil:
                for j in entree_piece:
                    sql2 = """select temps_vibration from vibration where (id_entree_outil = %s AND id_entree_piece = %s)"""
                    self.mycursor.execute(sql2, (i[0],j[0]))
                    temp = self.mycursor.fetchall()
                    for x in temp:
                        result.append(x[0])
        return result

    def frequence(self):
        """Récupération des valeurs de l'attribut frequence de la table vibration associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            sql2 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql2, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_outil:
                for j in entree_piece:
                    sql2 = """select frequence from vibration where (id_entree_outil = %s AND id_entree_piece = %s)"""
                    self.mycursor.execute(sql2, (i[0],j[0]))
                    freq = self.mycursor.fetchall()
                    for x in freq:
                        result.append(x[0])
        return result

    def amplitude(self):
        """Récupération des valeurs de l'attribut amplitude de la table vibration associés à l'experience"""
        result = []
        if self.experience is not None:
            sql1 = """select * from entree_outil where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql1, (self.experience,))
            entree_outil = self.mycursor.fetchall()
            sql2 = """select * from entree_piece where id_experience = %s order by id_experience"""
            self.mycursor.execute(sql2, (self.experience,))
            entree_piece = self.mycursor.fetchall()
            for i in entree_outil:
                for j in entree_piece:
                    sql2 = """select amplitude from vibration where (id_entree_outil = %s AND id_entree_piece = %s)"""
                    self.mycursor.execute(sql2, (i[0],j[0]))
                    ampl = self.mycursor.fetchall()
                    for x in ampl:
                        result.append(x[0])
        return result
