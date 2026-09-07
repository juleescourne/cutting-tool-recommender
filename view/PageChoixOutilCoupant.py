from tkinter import Frame, Label, Entry, Button, ttk, StringVar, Toplevel
from tkinter.messagebox import showerror
from controller.Usure_outilController import Usure_outilController
from controller.Effort_outilController import Effort_outilController
from controller.ProcedeController import ProcedeController
from controller.Temperature_pieceController import Temperature_pieceController
from controller.Entree_pieceController import Entree_pieceController
from controller.Entree_outilController import Entree_outilController
from view.Popup import CreatePopup


def validate_float(text):
    """fonction utilisée pour valider une entrée de nombre flottant

    Parameters
    ----------
    text : any
        texte d'entree

    Returns:
        -boolean: True si text peut etre converti en flottant, False sinon
    """
    if text.strip() == "":
        return True
    try:
        float(text)
        return True
    except ValueError:
        showerror(title="Erreur",
                  message=text + " doit être un nombre.")
        return False


def validate_string(text):
    """fonction utilisée pour valider une entrée de chaîne de caractères

    Parameters
    ----------
    text : any
        texte d'entree

    Returns:
        -boolean: True si text est une instance string, False sinon
    """
    if text.strip() == "":
        showerror(title="Erreur",
                  message="Champs vide.")
        return False
    elif not isinstance(text, str):
        showerror(title="Erreur",
                  message=text + " doit être une chaine de caractère.")
    else:
        return True

class PageChoixOutilCoupant:
    """Classe qui gère la vue de la page Choix Outil Coupant"""

    def __init__(self, window):
        """Constructeur de la page choix outil coupant

        Parameters
        ----------
        window : Tk
            La fenêtre principale de l'application
        """
        # Déclaration des controllers nécéssaires
        self.usure_outil_controller = Usure_outilController()
        self.effort_outil_controller = Effort_outilController()
        self.entree_outil_controller = Entree_outilController()
        self.entree_piece_controller = Entree_pieceController()
        self.temperature_piece_controller = Temperature_pieceController()
        self.procede_controller = ProcedeController()

        # creer la frame principale
        self.frame_choix_outil = Frame(window)

        # ajout des trois champs principaux
        self.outil_label = Label(self.frame_choix_outil, text="Paramètres outil usinage", font=("Arial", 15))
        self.piece_label = Label(self.frame_choix_outil, text="Paramètres pièce à usiner", font=("Arial", 15))
        self.interaction_label = Label(self.frame_choix_outil, text="Interaction outil-pièce", font=("Arial", 15))

        # variables verifiant le format des champs
        self.check_string = StringVar()
        self.check_float = StringVar()

        # affectation des variables de verifications aux fonctions de verifications
        self.check_string.trace('w', lambda name, index, mode, sv=self.check_string: validate_string(sv.get()))
        self.check_float.trace('w', lambda name, index, mode, sv=self.check_float: validate_float(sv.get()))

        # creation des entry
        self.temps_usinage_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.contraintes_residuelles_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.durete_max_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.fatigue_max_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.rugosite_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.fx_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.fy_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.fz_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.procede_entry = ttk.Combobox(self.frame_choix_outil, values=self.procede_controller.get_types_procede(),
                                          textvariable=lambda: self.check_string)
        self.materiau_entry = ttk.Combobox(self.frame_choix_outil, values=self.entree_piece_controller.get_materiaux(),
                                           textvariable=lambda: self.check_string)
        self.temperature_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.longueur_usine_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)
        self.amplitude_entry = Entry(self.frame_choix_outil, textvariable=lambda: self.check_float)

        # creation des labels pour chaque entry
        self.temps_usinage_label = Label(self.frame_choix_outil, text="Temps usinage max (min)")
        self.contraintes_residuelles_label = Label(self.frame_choix_outil, text="Contraintes résiduelles max (MPa)")
        self.durete_max_label = Label(self.frame_choix_outil, text="Dureté max (Hv)")
        self.fatigue_max_label = Label(self.frame_choix_outil, text="Fatigue max (MPa)")
        self.rugosite_label = Label(self.frame_choix_outil, text="Ra (µm)")
        self.fx_label = Label(self.frame_choix_outil, text="Fx max à la dent (N)")
        self.fy_label = Label(self.frame_choix_outil, text="Fy max à la dent (N)")
        self.fz_label = Label(self.frame_choix_outil, text="Fz max à la dent (N)")
        self.procede_label = Label(self.frame_choix_outil, text="Procédé d'usinage")
        self.materiau_label = Label(self.frame_choix_outil, text="Matériau usiné")
        self.temperature_label = Label(self.frame_choix_outil, text="Température max (°C)")
        self.longueur_usine_label = Label(self.frame_choix_outil, text="Longueur usinée (mm)")
        self.amplitude_label = Label(self.frame_choix_outil, text="Amplitude de fréquence de vibration")

        # creation du grid pour le champs outil d'usinage
        self.outil_label.grid(row=0, column=0, padx=20, pady=20)
        self.temps_usinage_label.grid(row=1, column=0, pady=20)
        self.temps_usinage_entry.grid(row=2, column=0)
        self.contraintes_residuelles_label.grid(row=3, column=0, pady=20)
        self.contraintes_residuelles_entry.grid(row=4, column=0)
        self.durete_max_label.grid(row=5, column=0, pady=20)
        self.durete_max_entry.grid(row=6, column=0)
        self.fatigue_max_label.grid(row=7, column=0, pady=20)
        self.fatigue_max_entry.grid(row=8, column=0)
        self.rugosite_label.grid(row=9, column=0, pady=20)
        self.rugosite_entry.grid(row=10, column=0)
        self.fx_label.grid(row=11, column=0, pady=20)
        self.fx_entry.grid(row=12, column=0)
        self.fy_label.grid(row=13, column=0, pady=20)
        self.fy_entry.grid(row=14, column=0)
        self.fz_label.grid(row=15, column=0, pady=20)
        self.fz_entry.grid(row=16, column=0)

        # creation du grid pour le champs pièce à usiner
        self.piece_label.grid(row=0, column=1, padx=150, pady=20)
        self.procede_label.grid(row=1, column=1, pady=20)
        self.procede_entry.grid(row=2, column=1)
        self.materiau_label.grid(row=3, column=1, pady=20)
        self.materiau_entry.grid(row=4, column=1)
        self.temperature_label.grid(row=5, column=1, pady=20)
        self.temperature_entry.grid(row=6, column=1)
        self.longueur_usine_label.grid(row=7, column=1, pady=20)
        self.longueur_usine_entry.grid(row=8, column=1)

        # creation du grid pour le interaction outil-piece
        self.interaction_label.grid(row=0, column=2, padx=20, pady=20)
        self.amplitude_label.grid(row=1, column=2, padx=20)
        self.amplitude_entry.grid(row=2, column=2)

        # creation du grid pour les boutons
        self.button_accueil = Button(self.frame_choix_outil, text="Accueil", font=("Arial", 20), bg='white', fg='black')
        self.button_valider = Button(self.frame_choix_outil, text="Valider", font=("Arial", 20), bg='white', fg='black')
        self.button_accueil.grid(row=15, column=1)
        self.button_valider.grid(row=15, column=2)



        # creation des pop-ups d'informations pour chaque champs
        CreatePopup(self.temps_usinage_label, text='Paramètre indiquant le temps maximum que met l\'outil à usiner la pièce\nUnité : minute')
        CreatePopup(self.contraintes_residuelles_label, text='Paramètres indiquant les contraintes maximum qui subsistent dans l\'outil qui ne sont soumises à aucun effort extérieur\nUnité : MégaPascal')
        CreatePopup(self.durete_max_label, text='Paramètre indiquant la résistance mécanique maximum que l\'outil oppose à la pénétration\nUnité : Vickers')
        CreatePopup(self.fatigue_max_label, text='Paramètre indiquant l\'endommagement maximum de l\'outil sous l\'effet de l\'usinage\nUnité : MégaPascal')
        CreatePopup(self.rugosite_label, text='Paramètre indiquant l\'état de surface de l\'outil.\nUnité : Micromètre')
        CreatePopup(self.fx_label, text='Paramètre indiquant l\'effort maximum à la dent sur l\'axe x\nUnité : Newton')
        CreatePopup(self.fy_label, text='Paramètre indiquant l\'effort maximum à la dent sur l\'axe y\nUnité : Newton')
        CreatePopup(self.fz_label, text='Paramètre indiquant l\'effort maximum à la dent sur l\'axe z\nUnité : Newton')
        CreatePopup(self.procede_label, text='Paramètre indiquant le procédé d\'usinage voulu pour usiner la pièce\nUnité : ∅')
        CreatePopup(self.materiau_label, text='Paramètre indiquant le matériau de la pièce à usiner\nUnité : ∅')
        CreatePopup(self.temperature_label, text='Paramètre indiquant la température maximum de la pièce à usiner\nUnité : Degré Celsius')
        CreatePopup(self.longueur_usine_label, text='Paramètre indiquant la longueur de la pièce à usiner\nUnité : millimètre')
        CreatePopup(self.amplitude_label, text='Paramètre indiquant l\'amplitude associé à la fréquence de vibration entre la pièce et l\'outil\nUnité : ∅')
