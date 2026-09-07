from tkinter import BOTH, YES, Tk
from tkinter.messagebox import showerror
from controller.ChoixOutilCoupant import ChoixOutilCoupant
from controller.DashboardController import DashboardController
from controller.ImportExperience import ImportExperience
from model import session
from model.Experience import Experience
from view.MenuView import MenuView
from view.PageChoixOutilCoupant import PageChoixOutilCoupant, validate_float, validate_string
from view.PageResultatsChoixOutilCoupant import PageResultatsChoixOutilCoupant


def back_to_home(new_frame, old_frame):
    """fonction qui permet de changer de page

    Parameters
    ----------
    new_frame : frame
        La frame à afficher
    old_frame : frame
        La frame à enlever

    """
    old_frame.forget()
    new_frame.pack(fill=BOTH, expand=YES)


class MainController:
    """Classe qui centrale qui appelle les autres classes de l'application"""

    def __init__(self):
        """Constructeur"""

        # creation fenetre
        self.window = Tk()

        # liste des vues
        self.experiences = session.query(Experience).all()
        self.menu_view = MenuView(self.window)

        self.page_choix_outil_coupant = PageChoixOutilCoupant(self.window)

        self.page_resultats_choix_outil_coupant = PageResultatsChoixOutilCoupant(self.window)

        self.controller_choix_outil_coupant = ChoixOutilCoupant()

        self.form_datas = {}  # données du formulaire choix outil coupant

        # configuration action bouton
        self.menu_view.butt_import.config(command=self.import_data)
        self.menu_view.butt_outil.config(command=self.display_page_choix_outil_coupant)
        self.configure_action_buttons_page_choix_outil_coupant()
        self.configure_action_buttons_page_resultats_choix_outil_coupant()

        # afficher fenetre
        self.window.mainloop()

    def import_data(self):
        """
        Importe les données d'experience issue d'un fichier excel
        """
        self.import_exp = ImportExperience()
        self.import_exp.main_import()

    def display_page_choix_outil_coupant(self):
        """fonction qui affiche la page choix outil coupant"""
        # titre fenetre
        self.window.title("Choix outil coupant")
        self.menu_view.frame_menu.forget()

        self.page_choix_outil_coupant.frame_choix_outil.pack(fill=BOTH, expand=YES)

    def validate_page_resultats_choix_outil_coupant_form(self):
        """fonction qui vérifie si le formulaire a été correctement rempli
        avant d'afficher la page des résultats du choix de l'outil coupant"""

        self.determine_checked_attributes()

        # vérifier s'il y a suffisament de données pour réaliser l'ACP.
        copy_data_without_combobox = self.form_datas.copy()
        if 'procede' in self.form_datas:
            del copy_data_without_combobox['procede']
        if 'materiau' in self.form_datas:
            del copy_data_without_combobox['materiau']
        if len(copy_data_without_combobox) < 3:
            showerror(title="Erreur",
                      message="Le formulaire doit contenir au moins 3 attributs afin de réaliser une ACP"
                              + "\nHors champs materiau et procede")
            self.form_datas.clear()
            return
        else:
            self.display_page_resultats_choix_outil_coupant()

    def display_page_resultats_choix_outil_coupant(self):
        """fonction qui affiche la page des résulats choix outil coupant"""

        # titre fenetre
        self.window.title("Résultats Choix outil coupant")

        tab = self.controller_choix_outil_coupant.compute_pca(self.form_datas)

        n_components_str = "Nombre de composantes : {}".format(self.controller_choix_outil_coupant.pca.n_components)
        self.page_resultats_choix_outil_coupant.n_components_str.set(n_components_str)

        for element in tab:
            self.page_resultats_choix_outil_coupant.treeview.insert('', 'end', values=element)

        self.page_choix_outil_coupant.frame_choix_outil.forget()
        self.page_resultats_choix_outil_coupant.frame_resultats.pack(fill=BOTH, expand=YES)

    def determine_checked_attributes(self):
        """Méthode déterminant les varaibles cochés pendant la page choix outil coupant"""

        if self.page_choix_outil_coupant.temps_usinage_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.temps_usinage_entry.get()):
            self.form_datas['temps_usinage'] = self.page_choix_outil_coupant.temps_usinage_entry.get()
        if self.page_choix_outil_coupant.contraintes_residuelles_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.contraintes_residuelles_entry.get()):
            self.form_datas[
                'contraintes_residuelles'] = self.page_choix_outil_coupant.contraintes_residuelles_entry.get()
        if self.page_choix_outil_coupant.durete_max_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.durete_max_entry.get()):
            self.form_datas['durete'] = self.page_choix_outil_coupant.durete_max_entry.get()
        if self.page_choix_outil_coupant.fatigue_max_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.fatigue_max_entry.get()):
            self.form_datas['fatigue'] = self.page_choix_outil_coupant.fatigue_max_entry.get()
        if self.page_choix_outil_coupant.rugosite_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.rugosite_entry.get()):
            self.form_datas['rugosite'] = self.page_choix_outil_coupant.rugosite_entry.get()
        if self.page_choix_outil_coupant.fx_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.fx_entry.get()):
            self.form_datas['fx'] = self.page_choix_outil_coupant.fx_entry.get()
        if self.page_choix_outil_coupant.fy_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.fy_entry.get()):
            self.form_datas['fy'] = self.page_choix_outil_coupant.fy_entry.get()
        if self.page_choix_outil_coupant.fz_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.fz_entry.get()):
            self.form_datas['fz'] = self.page_choix_outil_coupant.fz_entry.get()
        if self.page_choix_outil_coupant.procede_entry.get() != "" and validate_string(
                self.page_choix_outil_coupant.procede_entry.get()):
            self.form_datas['procede'] = self.page_choix_outil_coupant.procede_entry.get()
        else:
            showerror(title="Erreur",
                      message="Le champs procédé doit être rempli")
        if self.page_choix_outil_coupant.materiau_entry.get() != "" and validate_string(
                self.page_choix_outil_coupant.materiau_entry.get()):
            self.form_datas['materiau'] = self.page_choix_outil_coupant.materiau_entry.get()
        else:
            showerror(title="Erreur",
                      message="Le champs matériau doit être rempli")
        if self.page_choix_outil_coupant.temperature_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.temperature_entry.get()):
            self.form_datas['temperature'] = self.page_choix_outil_coupant.temperature_entry.get()
        if self.page_choix_outil_coupant.longueur_usine_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.longueur_usine_entry.get()):
            self.form_datas['longueur_usine'] = self.page_choix_outil_coupant.longueur_usine_entry.get()
        if self.page_choix_outil_coupant.amplitude_entry.get() != "" and validate_float(
                self.page_choix_outil_coupant.amplitude_entry.get()):
            self.form_datas['amplitude'] = self.page_choix_outil_coupant.amplitude_entry.get()


    def back_from_page_choix_outil_coupant_to_menu_view(self):
        """fonction permettant de passer de la page choix outil coupant au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_choix_outil_coupant.frame_choix_outil)
        self.page_choix_outil_coupant.__init__(self.window)
        self.configure_action_buttons_page_choix_outil_coupant()

    def back_from_resultats_page_choix_outil_coupant_to_menu_view(self):
        """fonction permettant de passer de la page resultat choix outil coupant au menu"""
        self.window.title("Accueil")
        back_to_home(self.menu_view.frame_menu, self.page_resultats_choix_outil_coupant.frame_resultats)
        self.page_resultats_choix_outil_coupant.__init__(self.window)

        self.form_datas.clear()

        self.configure_action_buttons_page_resultats_choix_outil_coupant()

    def back_from_resultats_page_choix_outil_coupant_to_page_choix_outil_coupant(self):
        """fonction permettant de passer de la page resultat choix outil coupant à un nouveau choix de l'outil coupant"""

        self.back_from_resultats_page_choix_outil_coupant_to_menu_view()
        self.display_page_choix_outil_coupant()


    def configure_action_buttons_page_choix_conditions_coupe(self):
        """fonction qui configure les actions des boutons de la page choix conditions coupe"""
        self.page_choix_conditions_coupe.butt_selectionner_fichier.config(
            command=lambda: self.import_file(True))
        self.page_choix_conditions_coupe.butt_accueil.config(
            command=self.back_from_page_choix_conditions_coupe_to_menu_view)
        self.page_choix_conditions_coupe.butt_valider.config(command=self.display_page_resultats)
        self.page_choix_conditions_coupe.button_aide.config(command=self.display_aide)


    def configure_action_buttons_page_choix_outil_coupant(self):
        """fonction qui configure les actions des boutons de la page choix outil coupant"""
        # Boutons
        self.page_choix_outil_coupant.button_accueil.config(
            command=self.back_from_page_choix_outil_coupant_to_menu_view)
        self.page_choix_outil_coupant.button_valider.config(
            command=self.validate_page_resultats_choix_outil_coupant_form)

    def configure_action_buttons_page_resultats_choix_outil_coupant(self):
        """fonction qui configure les actions des boutons de la page résultats choix outil coupant"""
        # Boutons
        self.page_resultats_choix_outil_coupant.butt_acp_2d.config(command=lambda:
        self.controller_choix_outil_coupant.create_and_display_fig_2d(with_variable=True))
        self.page_resultats_choix_outil_coupant.butt_acp_3d.config(
            command=self.controller_choix_outil_coupant.create_and_display_fig_3d)

        self.page_resultats_choix_outil_coupant.treeview.bind('<Double-Button-1>', DashboardController(
            self.page_resultats_choix_outil_coupant.treeview, self.form_datas).ouvrir_dash_interface)

        self.page_resultats_choix_outil_coupant.butt_accueil.config(command=self.back_from_resultats_page_choix_outil_coupant_to_menu_view)
        self.page_resultats_choix_outil_coupant.butt_retour.config(command=self.back_from_resultats_page_choix_outil_coupant_to_page_choix_outil_coupant)

