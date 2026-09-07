from tkinter import Frame, Label, Button, ttk, LabelFrame, StringVar
from tkinter.constants import *


class PageResultatsChoixOutilCoupant:
    """Classe qui gère la vue de la page des résultats du choix de l'outil coupant"""

    def __init__(self, window):
        """Constructeur de la page des résultats du choix de l'outil coupant

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        """

        # creer la frame principale
        self.frame_resultats = Frame(window)

        # TOP
        self.frame_top = Frame(self.frame_resultats)
        self.frame_top_left = Frame(self.frame_top)
        self.frame_top_right = Frame(self.frame_top)
        self.frame_top.pack(side=TOP)
        self.frame_top_left.pack(side=LEFT, padx=40)
        self.frame_top_right.pack(side=RIGHT, padx=40)

        self.frame_right = Frame(self.frame_resultats)
        self.frame_right_bottom = Frame(self.frame_right)
        self.frame_right.pack(side=RIGHT)
        self.frame_right_bottom.pack(side=BOTTOM, padx=10)

        # BOTTOM
        self.frame_bot = Frame(self.frame_resultats)
        self.frame_bot_left = Frame(self.frame_bot)

        self.frame_bot_left = LabelFrame(self.frame_bot, text="Listes des expériences les plus similaires", font=("Arial", 15))
        self.frame_bot.pack(side=BOTTOM)
        self.frame_bot_left.pack(side=LEFT, padx=40)

        # variable servant à afficher le nombre de composantes principales de l'ACP
        self.n_components_str = StringVar()

        # label qui affiche le nombre de composant de l'ACP
        self.label_componnets = Label(self.frame_top_left, textvariable=self.n_components_str)
        self.label_componnets.pack()

        self.butt_acp_2d = Button(self.frame_top_left, text="Afficher l'ACP en 2D", font=("Arial", 15),
                                  bg='white', fg='black')
        self.butt_acp_2d.pack(side=RIGHT, pady=50)

        # Boutton permettant d'afficher le graphe de l'ACP en 3D
        self.butt_acp_3d = Button(self.frame_top_left, text="Afficher l'ACP en 3D", font=("Arial", 15),
                                  bg='white', fg='black')
        self.butt_acp_3d.pack(side=RIGHT, pady=50, padx=10)

        self.butt_retour = Button(self.frame_resultats, text="Retour", font=("Arial", 15), bg='white', fg='black')
        self.butt_retour.pack(side=LEFT, pady=10, padx=5)

        # Boutton Accueil
        self.butt_accueil = Button(self.frame_resultats, text="Accueil", font=("Arial", 15), bg='white', fg='black')
        self.butt_accueil.pack(side=LEFT, pady=10, padx=5)

        # Label above and to the right of the treeview
        self.label_outil = LabelFrame(self.frame_right_bottom, text="Outils coupant conseillé", font=("Arial", 14, "bold"), fg="black", bg="#9C9C9C")
        self.label_outil.pack(side=BOTTOM, pady=10, padx=5)

        # Créer un label pour le texte en dessous
        mon_outil_coupant = Label(self.label_outil, text="Carbure monobloc", font=("Arial", 12), bg="#9C9C9C")
        mon_outil_coupant.pack(pady=10)


        # Tableau récapitulatif des expériences similaires
        self.treeview = ttk.Treeview(self.frame_bot_left, columns=("id_exp", "nom_exp",
                                                                   "type_proc", "type_op", "assistance", "debit_mql",
                                                                   "debit_cryo",
                                                                   "emulsion_HP", "vitesse_coupe", "vitesse_avance",
                                                                   "profondeur_passe", "engagement", "type_mat",
                                                                   "mat_p", "procede_elab",
                                                                   "imp_3d", "long_usi", "num_pa",
                                                                   "fx_p", "fy_p", "fz_p", "tmp_p", "rug", "dure",
                                                                   "lim_end", "contr_res",
                                                                   "type_out", "mat_o", "diam", "nb_dent",
                                                                   "revete", "fx_o", "fy_o", "fz_o", "tmp_o", "vb",
                                                                   "er", "kt", "epaiss",
                                                                   "freq", "ampl", "dist"), show="headings", )


        # header experience
        self.treeview.heading("id_exp", text="ID")
        self.treeview.heading("nom_exp", text="Nom Expérience")

        # header procede
        self.treeview.heading("type_proc", text="Type Procédé")
        self.treeview.heading("type_op", text="Type d'Opération")
        self.treeview.heading("assistance", text="Assistance")
        self.treeview.heading("debit_mql", text="Débit MQL (ml/h)")
        self.treeview.heading("debit_cryo", text="Débit Cryo (ml/h)")
        self.treeview.heading("emulsion_HP", text="Émulsion HP (bar)")
        self.treeview.heading("vitesse_coupe", text="Vitesse de Coupe (mm/min)")
        self.treeview.heading("vitesse_avance", text="Vitesse d'Avance (mm/dent)")
        self.treeview.heading("profondeur_passe", text="Profondeur de Passe (mm)")
        self.treeview.heading("engagement", text="Engagement")

        # header piece
        self.treeview.heading("type_mat", text="Type Matière Pièce")
        self.treeview.heading("mat_p", text="Matière Pièce")
        self.treeview.heading("procede_elab", text="Procédé élaboration")
        self.treeview.heading("imp_3d", text="Impression 3D")
        self.treeview.heading("long_usi", text="Longueur Usinée (mm)")
        self.treeview.heading("num_pa", text="Numéro de passe")
        self.treeview.heading("fx_p", text="Fx pièce Max (N)")
        self.treeview.heading("fy_p", text="Fy pièce Max (N)")
        self.treeview.heading("fz_p", text="Fz pièce Max (N)")
        self.treeview.heading("tmp_p", text="Température pièce Max (°C)")
        self.treeview.heading("rug", text="Rugosité (µm)")
        self.treeview.heading("dure", text="Dureté (MPa)")
        self.treeview.heading("lim_end", text="Limite endurance (MPa)")
        self.treeview.heading("contr_res", text="Contraintes résiduelles (MPa)")

        # header outil
        self.treeview.heading("type_out", text="Type Outil")
        self.treeview.heading("mat_o", text="Matière Outil")
        self.treeview.heading("diam", text="Diamètre Outil (mm)")
        self.treeview.heading("nb_dent", text="Nombre de dents")
        self.treeview.heading("revete", text="Revêtement")
        self.treeview.heading("fx_o", text="Fx outil Max (N)")
        self.treeview.heading("fy_o", text="Fy outil Max (N)")
        self.treeview.heading("fz_o", text="Fz outil Max (N)")
        self.treeview.heading("tmp_o", text="Température outil Max (°C)")
        self.treeview.heading("vb", text="Vb (mm)")
        self.treeview.heading("er", text="Er")
        self.treeview.heading("kt", text="Kt")

        # header vibration
        self.treeview.heading("freq", text="Fréquence de Vibration")
        self.treeview.heading("ampl", text="Amplitude de fréquence")

        # header copeaux
        self.treeview.heading("epaiss", text="Epaisseur copeaux (mm)")

        # header distance
        self.treeview.heading("dist", text="Distance")

        # Scrollbar vertical et horizontal
        vsb = ttk.Scrollbar(self.frame_bot_left, orient="vertical", command=self.treeview.yview)
        hsb = ttk.Scrollbar(self.frame_bot_left, orient="horizontal", command=self.treeview.xview)

        # attacher le scrollbar au tableau récapitulatif
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # positionnement des élements du tableau
        self.treeview.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")

        for column in self.treeview["columns"]:
            self.treeview.column(column, anchor=CENTER)

        # définir les dimensions de la grille
        self.frame_bot_left.grid_columnconfigure(0, weight=1)
        self.frame_bot_left.grid_rowconfigure(0, weight=1)
