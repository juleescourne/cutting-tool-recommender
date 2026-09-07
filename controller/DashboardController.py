import math
from math import *
import threading
import dash
import numpy as np
from dash import html, dcc
import webbrowser
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from controller.ExportExperience import ExportExperience
from utils import safe_math_expression
from model import mydb
from view.Dashboard import Dashboard
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class DashboardController:
    """
    Classe qui contient les méthodes necessaire à l'utilisation du Dashboard. Le dashboard est une interface plotly
    dash permettant de visualiser les données issues d'une expérience de la base de données.
    """

    def __init__(self, treeview, datas_usr):
        """
        Constructeur de la classe DashboardController
        :param treeview: Objet treeview contenant les données d'une expérience de la base de données
        :param datas_usr: Paramètres d'usinage remplis par l'utilisateur
        """

        # id de l'expérience associé au dashboard
        self.item_id = None

        # données de l'expérience
        self.data_exp = None

        # conteneur de l'ensemble des efforts à la piece pour l'experience
        self.effort_piece = None

        # conteneur de l'ensemble des efforts à l'outil' pour l'experience
        self.effort_outil = None

        # conteneur des paramètres remplis par l'utilisateur
        self.user_data = {}
        self.user_data = datas_usr

        # nombre initial de dropdown pour le chart radar
        self.nb_drop = 4

        # compteurs de clique sur les boutons add et del
        self.cmpt_add_click_courbe = 0
        self.cmpt_del_click_courbe = 0
        self.cmpt_add_click_radar = 0
        self.cmpt_del_click_radar = 0

        # mode d'affichage du graphique en courbe
        self.mode_value = None

        # conteneur des données à afficher pour le graphique en courbe
        # self.df = pd.DataFrame({})

        # contenu des dropdown servant pour le radar chart
        self.df_radar = {
            'dropdown1': None,
            'dropdown2': None,
            'dropdown3': None,
            'dropdown4': None,
            'dropdown5': None,
            'dropdown6': None,
            'dropdown7': None,
            'dropdown8': None
        }

        # contenu des dropdown servant pour le chart bar
        self.df_bar = {
            'dropdown-abs': None,
            'dropdown1': None,
            'dropdown2': None,
            'dropdown3': None,
            'dropdown4': None,
            'dropdown5': None,
            'dropdown6': None
        }

        # Données du treeview associés au dashboard
        self.treeview = treeview

        # Initialisation de l'application dash
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

        # Ensemble des méthodes utilisant le décorateur @self.app.callback
        self.visibility()
        self.color_callbacks()
        self.update_dropdown_radar_callbacks()
        self.update_dropdown_i_radar_callback(5)
        self.update_dropdown_i_radar_callback(6)
        self.update_dropdown_i_radar_callback(7)
        self.update_dropdown_i_radar_callback(8)
        self.update_dropdown_bar_callbacks()
        self.update_dropdown_i_bar_callback(1)
        self.update_dropdown_i_bar_callback(2)
        self.update_dropdown_i_bar_callback(3)
        self.update_dropdown_i_bar_callback(4)
        self.update_dropdown_i_bar_callback(5)
        self.update_dropdown_i_bar_callback(6)
        self.update_radar_callbacks()
        self.export_to_excel()
        self.graph_bar_callback()

    def export_to_excel(self):
        @self.app.callback(
            Output('export', 'n_clicks'),
            [Input('export', 'n_clicks')]
        )
        def export_to_excel(n_clicks):
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'export':
                export = ExportExperience(self.data_exp[0])

            return n_clicks

    def visibility(self):
        @self.app.callback(
            Output('content_infos', 'style'),
            Output('content_radar', 'style'),
            Output('content_courbe', 'style'),
            Input('btn-info', 'n_clicks'),
            Input('btn-radar', 'n_clicks'),
            Input('btn-courbe', 'n_clicks')
        )
        def display_page_infos(n_info_clicks, n_radar_clicks, n_courbe_clicks):
            """
            Méthode permettant de gérer l'affichage de chaque partie en fonction des cliques de l'utilisateur
            :param n_info_clicks: nombre de click sur l'item 'Informations generales'
            :param n_radar_clicks: nombre de click sur l'item 'Graphique en radar'
            :param n_courbe_clicks: nombre de click sur l'item 'Visualisation en courbe'
            :return: style des conteneurs de la partie droite du dashboard
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'btn-info':
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

            elif button_id == 'btn-radar':
                return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

            elif button_id == 'btn-courbe':
                return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

    def color_callbacks(self):
        @self.app.callback(
            Output('btn-info', 'style'),
            Output('btn-radar', 'style'),
            Output('btn-courbe', 'style'),
            Input('btn-info', 'n_clicks'),
            Input('btn-radar', 'n_clicks'),
            Input('btn-courbe', 'n_clicks')
        )
        def update_button_colors(info_clicks, radar_clicks, courbe_clicks):
            """
            Fonction qui color le bouton cliqué en dernier par l'utilisateur
            :param info_clicks: nombre de click sur l'item 'Informations generales'
            :param radar_clicks: nombre de click sur l'item 'Graphique en radar'
            :param courbe_clicks: nombre de click sur l'item 'Visualisation en courbe'
            :return: style des trois items
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'btn-info'
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'btn-info':
                return {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}
            elif button_id == 'btn-radar':
                return {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}
            elif button_id == 'btn-courbe':
                return {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': '#BFC3DC', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}, \
                       {'color': 'white', 'margin-bottom': '10px', 'padding': '10px', 'width': '100%',
                        'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}

    def update_dropdown_radar_callbacks(self):
        @self.app.callback(
            Output('var-radar', 'children'),
            Input('btn-add-var-radar', 'n_clicks'),
            Input('btn-del-var-radar', 'n_clicks'),
            State('var-radar', 'children'),
            Input('dropdown1', 'value'),
            Input('dropdown2', 'value'),
            Input('dropdown3', 'value'),
            Input('dropdown4', 'value')
        )
        def update_dropdown(add_clicks, del_clicks, children, drop_1, drop_2, drop_3, drop_4):
            """
            Méthode permettant à l'utilisateur d'ajouter ou effacer des dropdowns pour la partie chart radar.
            :param add_clicks: nombre de cliques du boutton ajouter
            :param del_clicks: nombre de cliques du boutton Effacer
            :param children: Conteneur des dropdowns
            :param drop_1: valeur du dropdown 1
            :param drop_2: valeur du dropdown 2
            :param drop_3: valeur du dropdown 3
            :param drop_4: valeur du dropdown 4
            :return: Conteneur des dropdowns
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Ajout d'un dropdown
            if button_id == 'btn-add-var-radar':

                # s'il n'y a pas plus de 8 dropdowns (et 3 bouttons)
                if len(children) < 11:

                    # numero et index du dernier dropdown
                    drop_num = add_clicks + 4 - del_clicks - self.cmpt_add_click_radar + self.cmpt_del_click_radar
                    index_add = drop_num - 1

                    # Creation du dropdown a ajouter
                    new_dropdown = dbc.Col(
                        dcc.Dropdown(id='dropdown{}'.format(drop_num), options=self.dashboard.dropdown_values,
                                     style={'background-color': '#ECECEC', 'border-color': 'black',
                                            'font-size': '12px'}),
                        width=2)

                    # insertion du dropdown a l'index dans le conteneur parent
                    children.insert(index_add, new_dropdown)

                    return children

                # S'il y a deja 8 dropdown
                else:
                    self.cmpt_add_click_radar += 1
                    print('Maximum number of dropdowns reached.')

            # Suppression d'un dropdown
            elif button_id == 'btn-del-var-radar':

                # S'il y a plus de 4 dropdowns
                if len(children) >= 8:

                    # numero et index du dropdown a supprimer
                    drop_num = add_clicks + 5 - del_clicks - self.cmpt_add_click_radar + self.cmpt_del_click_radar
                    index_del = drop_num - 1

                    # suppression du dropdown a l'index
                    children.pop(index_del)

                    # On efface les valeurs associé à ce dropdown
                    self.df_radar['dropdown{}'.format(drop_num)] = None

                    return children

                # S'il y a 4 dropdown
                else:
                    self.cmpt_del_click_radar += 1
                    print('No dropdowns to remove.')

            elif button_id == 'dropdown1':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_1), None)
                if option:
                    self.df_radar['dropdown1'] = option

            elif button_id == 'dropdown2':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_2), None)
                if option:
                    self.df_radar['dropdown2'] = option

            elif button_id == 'dropdown3':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_3), None)
                if option:
                    self.df_radar['dropdown3'] = option

            elif button_id == 'dropdown4':
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop_4), None)
                if option:
                    self.df_radar['dropdown4'] = option

            return children

    def update_dropdown_i_radar_callback(self, index):
        @self.app.callback(
            Output('dropdown{}'.format(index), 'value'),
            [Input('dropdown{}'.format(index), 'value')]
        )
        def update(drop):
            """
            Met à jour les dropdowns 5 à 8 pour la partie chart radar. Ces dropdowns peuvent ne pas exister.
            :param drop: la valeur du dropdown cliquer par l'utilisateur
            :return: drop: la valeur du dropdown cliquer par l'utilisateur
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'dropdown{}'.format(index):
                option = next((o for o in self.dashboard.dropdown_values if o['value'] == drop), None)
                if option:
                    self.df_radar['dropdown{}'.format(index)] = option

            return drop

    def update_dropdown_bar_callbacks(self):
        @self.app.callback(
            Output('var-courbe-ord', 'children'),
            Output('dropdown-abs', 'value'),
            Input('btn-add-var-courbe-ord', 'n_clicks'),
            Input('btn-del-var-courbe-ord', 'n_clicks'),
            Input('dropdown-abs', 'value'),
            State('var-courbe-ord', 'children'),
        )
        def update_dropdown(add_clicks, del_clicks, value, children):
            """
            Méthode permettant à l'utilisateur d'ajouter ou effacer des dropdowns pour la partie chart bar.
            :param add_clicks: nombre de cliques du boutton ajouter
            :param del_clicks: nombre de cliques du boutton effacer
            :param value: valeur du dropdown associé à l'abscisse
            :param children: conteneur des dropdowns associé à l'ordonnée.
            :return: children: conteneur des dropdowns associé à l'ordonnée.
            :return: value: valeur du dropdown associé à l'abscisse
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Ajout d'un dropdown
            if button_id == 'btn-add-var-courbe-ord':

                # S'il y a moins de 6 dropdowns (et 3 bouttons)
                if len(children) < 9:

                    # Numero et index du dropdown a ajouter
                    drop_num = add_clicks + 1 - del_clicks + self.cmpt_del_click_courbe - self.cmpt_add_click_courbe
                    index_add = drop_num - 1

                    # creation du nouveaux dropdown
                    new_dropdown = dbc.Col(
                        dcc.Dropdown(id='dropdown-ord{}'.format(drop_num), options=self.dashboard.ord_values,
                                     style={'background-color': '#ECECEC', 'border-color': 'black',
                                            'font-size': '12px'}),
                        width=2)

                    # Insertion dans le conteneur parent
                    children.insert(index_add, new_dropdown)

                # S'il y a deja 6 dropdowns
                else:
                    self.cmpt_add_click_courbe += 1
                    print('Maximum number of dropdowns reached.')

            # Suppression d'un dropdown
            elif button_id == 'btn-del-var-courbe-ord':

                # S'il y a au moins deux dropdowns (et 3 bouttons)
                if len(children) >= 5:

                    # Numero et index du dropdown a effacer
                    drop_num = add_clicks + 2 - del_clicks + self.cmpt_del_click_courbe - self.cmpt_add_click_courbe
                    index_del = drop_num - 1

                    # Mise a jour du conteneur parent
                    children.pop(index_del)

                    # Mise a jour des valeurs du dropdown
                    # self.df_bar['dropdown{}'.format(drop_num)] = None
                    self.df_bar.update({'dropdown{}'.format(drop_num): None})

                # S'il y a un dropdown
                else:
                    self.cmpt_del_click_courbe += 1
                    print('No dropdowns to remove.')

            # Mise a jour de la valeur de l'abscisse
            elif button_id == 'dropdown-abs':
                if value == 1:
                    drop = [t[1] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Temps (s)', 'value': drop}
                if value == 2:
                    drop = [t[2] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fx pièce (N)', 'value': drop}
                if value == 3:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fy pièce (N)', 'value': drop}
                if value == 4:
                    drop = [t[4] for t in self.effort_piece]
                    self.df_bar['dropdown-abs'] = {'label': 'Fz pièce (N)', 'value': drop}
                if value == 5:
                    drop = [t[2] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fx outil (N)', 'value': drop}
                if value == 6:
                    drop = [t[3] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fy outil (N)', 'value': drop}
                if value == 7:
                    drop = [t[4] for t in self.effort_outil]
                    self.df_bar['dropdown-abs'] = {'label': 'Fz outil (N)', 'value': drop}

            return children, value

    def update_dropdown_i_bar_callback(self, index):
        @self.app.callback(
            Output('dropdown-ord{}'.format(index), 'value'),
            [Input('dropdown-ord{}'.format(index), 'value')]
        )
        def update(value):
            """
            Met à jour les dropdowns 2 à 6 pour la partie chart bar. Ces dropdowns peuvent ne pas exister.
            :param value: la valeur du dropdown cliquer par l'utilisateur
            :return: value: la valeur du dropdown cliquer par l'utilisateur
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'dropdown-ord{}'.format(index):
                if value == 1:
                    drop = [t[2] for t in self.effort_piece]
                    # self.df_bar['dropdown{}'.format(index)] = {'label': 'Fx pièce (N)', 'value': drop}
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fx pièce (N)', 'value': drop}})
                    print(self.df_bar['dropdown{}'.format(index)]['label'])
                if value == 2:
                    drop = [t[3] for t in self.effort_piece]
                    self.df_bar['dropdown{}'.format(index)] = {'label': 'Fy pièce (N)', 'value': drop}
                    print(self.df_bar['dropdown{}'.format(index)]['label'])
                if value == 3:
                    drop = [t[4] for t in self.effort_piece]
                    # self.df_bar['dropdown{}'.format(index)] = {'label': 'Fz pièce (N)', 'value': drop}
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fz pièce (N)', 'value': drop}})
                    print(self.df_bar['dropdown{}'.format(index)]['label'])
                if value == 4:
                    drop = [t[2] for t in self.effort_outil]
                    # self.df_bar['dropdown{}'.format(index)] = {'label': 'Fx outil (N)', 'value': drop}
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fx outil (N)', 'value': drop}})
                    print(self.df_bar['dropdown{}'.format(index)]['label'])
                if value == 5:
                    drop = [t[3] for t in self.effort_outil]
                    # self.df_bar['dropdown{}'.format(index)] = {'label': 'Fy outil (N)', 'value': drop}
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fy outil (N)', 'value': drop}})
                    print(self.df_bar['dropdown{}'.format(index)]['label'])
                if value == 6:
                    drop = [t[4] for t in self.effort_outil]
                    # self.df_bar['dropdown{}'.format(index)] = {'label': 'Fz outil (N)', 'value': drop}
                    self.df_bar.update({'dropdown{}'.format(index): {'label': 'Fz outil (N)', 'value': drop}})
                    print(self.df_bar['dropdown{}'.format(index)]['label'])

            return value

    def graph_bar_callback(self):
        @self.app.callback(
            Output('f-output', 'children'),
            Output('courbe-chart', 'style'),
            Output('courbe-chart', 'figure'),
            Input('mode-value', 'value'),
            Input('btn-val-var-courbe-ord', 'n_clicks'),
            [Input('dropdown-abs', 'value')],
            [State('dropdown-abs', 'options')],
            State('formula', 'value')
        )
        def graph_courbe(mode_value, val_clicks, value, options, f_value):
            """
            Méthode permettant de créer le chart bar.
            :param mode_value: valeur du mode d'affichage du graphique
            :param val_clicks: nombre de clique sur le boutton valider
            :param value: valeur du dropdown de l'abscisse
            :param options: options pour le dropdown de l'abscisse
            :param f_value: valeur de la formule entrée par l'utilisateur
            :return: html_p : Objet hmtl.P contenant l'erreur associé à la formule
            :return: style : le style du plotly express bar a afficher
            :return: fig : plotly express bar a afficher
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # initialisation du chart bar
            fig = px.bar()

            # initialisation du conteneur de l'erreur associé a la formule
            html_p = html.P('', style={'font-weight': 'bold', 'display': 'inline-block'})

            # Si l'utilisateur clique sur valider
            if button_id == 'btn-val-var-courbe-ord':
                # verification que l'utilisateur a bien cliquer sur valider
                if val_clicks > 0:

                    # on récupère le label du dropdown pour l'abscisse
                    label = [o['label'] for o in options if o['value'] == value][0]

                    # initialisation des tableaux qui contienent les données a afficher
                    abscissa = []  # valeurs du choix utilisateurs pour l'abscisse
                    fx_piece = []  # valeurs de l'effort fx a la piece
                    fy_piece = []  # valeurs de l'effort fy a la piece
                    fz_piece = []  # valeurs de l'effort fz a la piece
                    fx_outil = []  # valeurs de l'effort fx a l'outil
                    fy_outil = []  # valeurs de l'effort fy a l'outil
                    fz_outil = []  # valeurs de l'effort fz a l'outil
                    ord_name = ''  # nom de l'ordonnée

                    # Si l'utilisateur veut le temps en abscisse
                    if label == 'Temps (s)':
                        # ajout des valeurs du temps
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)

                    # Si l'utilisateur veut l'effort fx piece en abscisse
                    if label == 'Fx pièce (N)':
                        # ajout des valeurs de fx
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fx piece'

                    # Si l'utilisateur veut l'effort fy piece en abscisse
                    if label == 'Fy pièce (N)':
                        # ajout des valeurs de fy
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fy piece'

                    # Si l'utilisateur veut l'effort fz piece en abscisse
                    if label == 'Fz pièce (N)':
                        # ajout des valeurs de fz
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fz piece'

                    # Si l'utilisateur veut l'effort fx outil en abscisse
                    if label == 'Fx outil (N)':
                        # ajout des valeurs de fx
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fx outil'

                    # Si l'utilisateur veut l'effort fy outil en abscisse
                    if label == 'Fy outil (N)':
                        # ajout des valeurs de fy
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fy outil'

                    # Si l'utilisateur veut l'effort fz outil en abscisse
                    if label == 'Fz outil (N)':
                        # ajout des valeurs de fz
                        for i in self.df_bar['dropdown-abs']['value']:
                            abscissa.append(i)
                            ord_name = ' / fz outil'

                    # Pour tous les dropdowns
                    for i in range(1, 6):
                        # Si le dropdown i est associé à une valeur
                        if self.df_bar['dropdown{}'.format(i)] is not None:
                            # Si le dropdown i est associé aux efforts fx a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fx pièce (N)':
                                # ajout des valeurs fx a la piece
                                fx_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fy a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fy pièce (N)':
                                # ajout des valeurs fy a la piece
                                fy_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fz a la piece
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fz pièce (N)':
                                # ajout des valeurs fz a la piece
                                fz_piece = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fx a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fx outil (N)':
                                # ajout des valeurs fx a l'outil
                                fx_outil = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fy a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fy outil (N)':
                                # ajout des valeurs fy a l'outil
                                fy_outil = self.df_bar['dropdown{}'.format(i)]['value']

                            # Si le dropdown i est associé aux efforts fx a l'outil
                            if self.df_bar['dropdown{}'.format(i)]['label'] == 'Fz outil (N)':
                                # ajout des valeurs fz a l'outil
                                fz_outil = self.df_bar['dropdown{}'.format(i)]['value']

                    # nombre de valeurs de l'abscisse
                    size = len(abscissa)

                    # affectation des valeurs du temps
                    temps = [i[1] for i in self.effort_piece]

                    df = pd.DataFrame({})

                    # S'il y a au moins une valeur en abscisse
                    if size > 0:
                        # Si l'utilisateur est en mode moyenne des valeurs.
                        if mode_value == 1:
                            # Si l'abscisse est le temps
                            if label == 'Temps (s)':
                                # Si le nombre de valeurs de l'ordonnée est egale au nombre de valeurs de l'abscisse
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fx pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_mean(fx_piece, temps)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fy pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_mean(fy_piece, temps)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fz pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_mean(fz_piece, temps)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fx pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_mean(fx_outil, temps)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fy pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_mean(fy_outil, temps)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # On calcul et stocke la liste des moyennes des efforts fz pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_mean(fz_outil, temps)[0]

                            # Si l'abscisse n'est pas le temps
                            else:
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_mean(fx, temps)[0]

                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_mean(fy, temps)[0]

                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_piece, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_mean(fz, temps)[0]

                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_mean(fx, temps)[0]

                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_mean(fy, temps)[0]

                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_outil, abscissa)]
                                    # On calcul et stocke la liste des moyennes pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_mean(fz, temps)[0]

                        # si le mode est 'maximum'
                        elif mode_value == 2:
                            # Si l'abscisse est le temps
                            if label == 'Temps (s)':
                                # Si le nombre de valeurs de l'ordonnée est egale au nombre de valeurs de l'abscisse
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_max(fx_piece, temps)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_max(fy_piece, temps)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_max(fz_piece, temps)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_max(fx_outil, temps)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_max(fy_outil, temps)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # Calcul et stocke du max (ou min si abs(min) > abs(max)) pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_max(fz_outil, temps)[0]

                            # si l'abscisse n'est pas le temps
                            else:
                                # si l'ordonnee est fx piece
                                if len(fx_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fx piece{}'.format(ord_name)] = self.get_max(fx, temps)[0]
                                # si l'ordonnee est fy piece
                                if len(fy_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fy piece{}'.format(ord_name)] = self.get_max(fy, temps)[0]
                                # si l'ordonnee est fz piece
                                if len(fz_piece) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_piece, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fz piece{}'.format(ord_name)] = self.get_max(fz, temps)[0]
                                # si l'ordonnee est fx outil
                                if len(fx_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fx = [round(fx / abs, 4) for fx, abs in zip(fx_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fx outil{}'.format(ord_name)] = self.get_max(fx, temps)[0]
                                # si l'ordonnee est fy outil
                                if len(fy_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fy = [round(fy / abs, 4) for fy, abs in zip(fy_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fy outil{}'.format(ord_name)] = self.get_max(fy, temps)[0]
                                # si l'ordonnee est fz outil
                                if len(fz_outil) == size:
                                    # on fait le rapport ordonnee sur abscisse
                                    fz = [round(fz / abs, 4) for fz, abs in zip(fz_outil, abscissa)]
                                    # On calcul et stocke la liste des max pour chaque seconde
                                    df['fz outil{}'.format(ord_name)] = self.get_max(fz, temps)[0]

                        # on stocke chaque seconde
                        df['temps'] = self.get_mean([1 for i in range(size)], temps)[1]

                        # conteneur des nom des colonnes (abscisse et ordonnée)
                        traces = ['temps']
                        for col in df.columns:
                            if col != 'temps':
                                traces.append(col)

                        # Si la formule n'est pas vide ou egale à sa valeur initial
                        if f_value != '' and f_value != 'sqrt(y), ..':
                            try:
                                # pour toutes les colonnes
                                for tr in traces:
                                    result = []
                                    if tr != 'temps':
                                        # pour toutes les valeurs associé à la colonne
                                        for f in self.df[tr]:
                                            f = str(f)
                                            # on stocke le résultat de la formule avec la valeur
                                            result.append(safe_math_expression(f_value, float(f)))
                                        df[tr] = result

                                # # Calcul et stocke des moyennes des efforts à la piece
                                # fx = self.get_mean([t[2] for t in self.effort_piece], temps)[0]
                                # fy = self.get_mean([t[3] for t in self.effort_piece], temps)[0]
                                # fz = self.get_mean([t[4] for t in self.effort_piece], temps)[0]

                                # Calcul des puissances associés aux efforts
                                # puissances = []
                                # v = float(self.data_exp[8]) * 1000 / 60
                                # for i, j, p in zip(fx, fy, fz):
                                #     effort_couple = math.sqrt(i ** 2 + j ** 2 + p ** 2)
                                #     puissance = effort_couple * v
                                #     puissances.append(puissance)
                                #
                                # # Calcul des energies associés aux efforts
                                # energies = []
                                # for i in range(len(puissances)):
                                #     e = np.array([(puissances[j] * temps[j]) for j in range(i)])
                                #     energies.append(e.sum())
                                #
                                # # Construction du chart abr
                                fig = px.bar(df, x='temps', y=traces)
                                #
                                # # Ajout d'une courbe de puissance
                                # puissance_trace = go.Scatter(x=self.df['temps'], y=puissances, mode='lines',
                                #                              name='Puissance (W)')
                                # fig.add_trace(puissance_trace)
                                #
                                # # Ajout d'une courbe d'energie
                                # energie_trace = go.Scatter(x=self.df['temps'], y=energies, mode='lines',
                                #                            name='Energie (J)')
                                # fig.add_trace(energie_trace)

                                # affectation des labels associés aux axes
                                fig.update_xaxes(title='Temps (s)')
                                fig.update_yaxes(title='Efforts (N)')

                                return html_p, {'width': '100vh', 'height': '60vh', 'display': 'flex'}, fig

                            except Exception as e:
                                # affichage de l'erreur
                                html_p = html.P(str(e), style={'font-weight': 'bold', 'display': 'inline-block'})
                                return html_p, {'width': '100vh', 'height': '60vh', 'display': 'flex'}, fig

                        # # Calcul et stocke des moyennes des efforts à la piece
                        # fx = self.get_mean([t[2] for t in self.effort_piece], temps)[0]
                        # fy = self.get_mean([t[3] for t in self.effort_piece], temps)[0]
                        # fz = self.get_mean([t[4] for t in self.effort_piece], temps)[0]
                        #
                        # # Calcul des puissances associés aux efforts
                        # puissances = []
                        # v = float(self.data_exp[8]) * 1000 / 60
                        # for i, j, p in zip(fx, fy, fz):
                        #     effort_couple = math.sqrt(i ** 2 + j ** 2 + p ** 2)
                        #     puissance = effort_couple * v
                        #     puissances.append(puissance)
                        #
                        # # Calcul des energies associés aux efforts
                        # energies = []
                        # for i in range(len(puissances)):
                        #     e = np.array([(puissances[j] * temps[j]) for j in range(i)])
                        #     energies.append(e.sum())

                        # creation du bar chart
                        fig = px.bar(df, x='temps', y=traces)

                        # ajout de la courbe des puissances
                        # puissance_trace = go.Scatter(x=self.df['temps'], y=puissances, mode='lines',
                        #                              name='Puissance (W)')
                        # fig.add_trace(puissance_trace)
                        #
                        # # ajout de la courbe des energies
                        # energie_trace = go.Scatter(x=self.df['temps'], y=energies, mode='lines', name='Energie (J)')
                        # fig.add_trace(energie_trace)

                        # affectation des labels associés aux axes
                        fig.update_xaxes(title='Temps (s)')
                        fig.update_yaxes(title='Efforts (N)')

                return html_p, {'width': '100vh', 'height': '60vh', 'display': 'flex'}, fig
            return [html_p, {'width': '100vh', 'height': '60vh', 'display': 'None'}, fig]

    def update_radar_callbacks(self):
        @self.app.callback(
            Output('total-value', 'children'),
            Output('near-value', 'children'),
            Output('far-value', 'children'),
            Output('radar-chart', 'style'),
            Output('radar-chart', 'figure'),
            Input('btn-val-var-radar', 'n_clicks')
        )
        def update_graph(val_click):
            """
            Construit le chart radar et met a jour les informations sur ce graphe
            :param val_click: nombre de cliques du boutton valider
            :return: le pourcentage total, la distance la plus courte et la plus eloigné
            """
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = ''
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # intialisation de la figure
            fig = go.Figure()

            # Si on clique sur valider
            if button_id == 'btn-val-var-radar' and val_click > 0:

                # initialisation des liste de valeurs
                labels_exp = []  # valeurs des labels des paramètres
                vals_exp = []  # valeurs des paramètres de l'experience
                vals_usr = []  # valeurs des paramètres voulus par l'utilisateur
                usr_df = []  # valeurs normées des paramètres voulus par l'utilisateur
                exp_df = []  # valeurs normées des paramètres de l'experience
                hover_data_exp = []
                hover_data_usr = []

                # initialisation des variables pour les informations du chart radar
                near_value = 99999999  # contient la valeur la plus proche entre experience et utilisateur
                str_near = ''
                far_value = 0  # contient la valeur la plus eloigne entre experience et utilisateur
                str_far = ''
                total_value = 0  # contient le total de ressemblance entre experience et utilisateur

                # pour tous les valeurs de dropdowns
                for i in range(1, len(self.df_radar)):
                    index = 'dropdown{}'.format(i)
                    # Si le dropdown a un selection
                    if self.df_radar[index] is not None and self.df_radar[index]['value'] is not None:
                        # Si la selection du dropdown est un choix utilisateur
                        label = self.map_datas(self.df_radar[index]['label'])
                        if label in self.user_data.keys():
                            if label == 'contraintes_residuelles':
                                hover_data_exp.append('Contraintes résiduelles max = ' + str(
                                    float(self.df_radar[index]['value'])) + ' MPa')
                                hover_data_usr.append('Contraintes résiduelles max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' MPa')
                            if label == 'durete':
                                hover_data_exp.append(
                                    'Dureté max = ' + str(float(self.df_radar[index]['value'])) + ' Hv')
                                hover_data_usr.append('Dureté max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Hv')
                            if label == 'fatigue':
                                hover_data_exp.append(
                                    'Fatigue max = ' + str(float(self.df_radar[index]['value'])) + ' MPa')
                                hover_data_usr.append('Fatigue max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' MPa')
                            if label == 'rugosite':
                                hover_data_exp.append(
                                    'Rugosité max = ' + str(float(self.df_radar[index]['value'])) + ' µm')
                                hover_data_usr.append('Rugosité max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' µm')
                            if label == 'fx':
                                hover_data_exp.append('Effort Fx max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fx max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'fy':
                                hover_data_exp.append('Effort Fy max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fy max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'fz':
                                hover_data_exp.append('Effort Fz max à la dent = ' + str(
                                    float(self.df_radar[index]['value'])) + ' Newton')
                                hover_data_usr.append('Effort Fz max à la dent = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' Newton')
                            if label == 'temperature':
                                hover_data_exp.append(
                                    'Température max à la pièce = ' + str(float(self.df_radar[index]['value'])) + ' °C')
                                hover_data_usr.append('Température max à la pièce = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' °C')
                            if label == 'longueur_usine':
                                hover_data_exp.append(
                                    'Longueur usiné = ' + str(float(self.df_radar[index]['value'])) + ' mm')
                                hover_data_usr.append('Longueur usiné = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])) + ' mm')
                            if label == 'amplitude':
                                hover_data_exp.append(
                                    'Amplitude de fréquence max = ' + str(float(self.df_radar[index]['value'])))
                                hover_data_usr.append('Amplitude de fréquence max = ' + str(
                                    float(self.user_data[self.map_datas(self.df_radar[index]['label'])])))

                            labels_exp.append(self.df_radar[index]['label'])
                            vals_exp.append(float(self.df_radar[index]['value']))
                            vals_usr.append(float(self.user_data[self.map_datas(self.df_radar[index]['label'])]))

                # On norme chaque valeur
                for i, j in zip(vals_usr, vals_exp):
                    if (i + j) != 0:
                        usr_df.append(i / (i + j))
                        exp_df.append(j / (i + j))
                    else:
                        usr_df.append(0)
                        exp_df.append(0)

                # On calcul la variable eloigne
                for i, j, p in zip(usr_df, exp_df, vals_exp):
                    if i > j:
                        if far_value < i - j:
                            far_value = i - j
                            str_far = labels_exp[vals_exp.index(p)]
                    if i < j:
                        if far_value < j - i:
                            far_value = j - i
                            str_far = labels_exp[vals_exp.index(p)]

                # On calcul la variable la plus proche
                for i, j, p in zip(usr_df, exp_df, vals_exp):
                    if i > j:
                        if near_value > i - j:
                            near_value = i - j
                            str_near = labels_exp[vals_exp.index(p)]
                    if i < j:
                        if near_value > j - i:
                            near_value = j - i
                            str_near = labels_exp[vals_exp.index(p)]

                # On calcul le total
                for i, j in zip(usr_df, exp_df):
                    if i > j:
                        if i != 0:
                            total_value += j / i
                        else:
                            total_value += 0
                    elif i < j:
                        if j != 0:
                            total_value += i / j
                        else:
                            total_value += 0
                    else:
                        total_value += 1

                if len(usr_df) != 0:
                    total_value = abs(total_value)
                    total_value /= len(usr_df)
                    total_value = round(total_value * 100, 2)
                else:
                    total_value = 0

                # creation de la trace experience
                fig.add_trace(go.Scatterpolar(
                    r=exp_df,
                    theta=labels_exp,
                    fill='toself',
                    name='Expérience proche',
                    customdata=hover_data_exp
                ))

                # creation de la trace utilisateur
                fig.add_trace(
                    go.Scatterpolar(
                        r=usr_df,
                        theta=labels_exp,
                        fill='toself',
                        name='Choix utilisateur',
                        customdata=hover_data_usr
                    )
                )

                fig.update_traces(
                    hovertemplate='%{customdata}'
                )

                # mis a jour du layout
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                        )),
                    showlegend=True
                )

                return html.P(f'{total_value}%', style={'margin': '0px', 'display': 'inline-block'}), \
                       html.P(f'{str_near}', style={'margin': '0px', 'display': 'inline-block'}), \
                       html.P(f'{str_far}', style={'margin': '0px', 'display': 'inline-block'}), \
                       {'width': '70vh', 'height': '60vh', 'display': 'flex'}, fig

            return html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   html.P('', style={'margin': '0px', 'display': 'inline-block'}), \
                   {'width': '70vh', 'height': '60vh', 'display': 'none'}, fig

    def get_mean(self, list_effort, list_temps):
        """
        Calcul la moyenne des efforts pour une seconde. Permet d'avoir une courbe lisible en vue du grand
        nombre de données.
        :param list_effort: liste des valeurs des efforts
        :param list_temps: liste des valeurs du temps
        :return: liste moyennes des efforts, liste de chaque secondes
        """
        temps = np.array(list_temps)
        effort = np.array(list_effort)
        int_temps = temps.astype(int)
        temps_unique = np.unique(int_temps)
        effort_mean = np.zeros(len(temps_unique))
        for iu, t in enumerate(temps_unique):
            indices = np.where(int_temps == t)[0]
            effort_mean[iu] = np.mean(effort[indices])
        return effort_mean.tolist(), temps_unique.tolist()

    def get_max(self, list_effort, list_temps):
        """
        Calcul du max (ou min si abs(min) > abs(max)) des efforts pour une seconde.
        Permet d'avoir une courbe lisible en vue du grand nombre de données.
        :param list_effort: liste des valeurs des efforts
        :param list_temps: liste des valeurs du temps
        :return: liste max des efforts, liste de chaque secondes
        """
        temps = np.array(list_temps)
        effort = np.array(list_effort)
        int_temps = temps.astype(int)
        temps_unique = np.unique(int_temps)
        effort_mean = np.zeros(len(temps_unique))
        for iu, t in enumerate(temps_unique):
            indices = np.where(int_temps == t)[0]
            effort_mean[iu] = np.max(effort[indices]) if abs(np.max(effort[indices])) > abs(
                np.min(effort[indices])) else np.min(effort[indices])
        return effort_mean.tolist(), temps_unique.tolist()

    def map_datas(self, label):
        """
        Fonction qui mappe le label des dropdowns avec le label des valeurs rempli par l'utilisateur
        :param label: label du dropdown
        :return: string représentant le label
        """
        if label == 'Contraintes max':
            return 'contraintes_residuelles'
        if label == 'Dureté max':
            return 'durete'
        if label == 'Fatigue max':
            return 'fatigue'
        if label == 'Ra max':
            return 'rugosite'
        if label == 'Fx dent max':
            return 'fx'
        if label == 'Fy dent max':
            return 'fy'
        if label == 'Fz dent max':
            return 'fz'
        if label == 'Température pièce max':
            return 'temperature'
        if label == 'Longueur usinée':
            return 'longueur_usine'
        if label == 'Amplitude':
            return 'amplitude'
        return None

    def get_needed_data(self):
        """
        Recupere les efforts et les données de l'experience
        """
        self.data_exp = self.treeview.item(self.item_id)['values']
        mycursor = mydb.cursor()
        sql1 = """select id_entree_piece from entree_piece where id_experience=%s"""
        mycursor.execute(sql1, (self.treeview.item(self.item_id)['values'][0],))
        piece = mycursor.fetchall()

        sql2 = """select * from effort_piece where id_entree_piece=%s"""
        mycursor.execute(sql2, (piece[0][0],))
        self.effort_piece = mycursor.fetchall()

        sql3 = """select id_entree_outil from entree_outil where id_experience=%s"""
        mycursor.execute(sql3, (self.treeview.item(self.item_id)['values'][0],))
        outil = mycursor.fetchall()

        sql4 = """select * from effort_outil where id_entree_outil=%s"""
        mycursor.execute(sql4, (outil[0][0],))
        self.effort_outil = mycursor.fetchall()
        mycursor.close()

    def open_browser(self):
        """
        Ouvre l'application dash sur une page web
        """
        webbrowser.open_new("http://localhost:{}".format(8050))

    def ouvrir_dash_interface(self, event):
        """
        Lance l'application dash
        :param event: evenement de clique de la souris
        """
        self.item_id = self.treeview.identify_row(event.y)
        self.get_needed_data()
        self.dashboard = Dashboard(self.app, self.data_exp, self.user_data)
        t1 = threading.Thread(target=self.app.run, kwargs={'debug': True, 'port': 8050, 'use_reloader': False})
        t1.start()
        self.open_browser()
