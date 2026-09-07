from dash import html, dcc
import dash_bootstrap_components as dbc


def _has_value(value):
    """Return True for values that are not empty/None-like strings."""
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {"", "none", "nan", "null"}
    return True


class Dashboard:
    """class contenant la vue du Dashboard"""

    def __init__(self, app, data_exp, data_usr):
        """Constructeur de la classe Dashboard"""

        # attribut contenant l'application Dash
        self.app = app

        # valeurs associees à une experience de la base de données
        self.data = data_exp

        # valeurs des dropdown pour le chart radar
        self.dropdown_values = []

        if 'contraintes_residuelles' in data_usr and _has_value(self.data[25]):
            self.dropdown_values.append({'label': 'Contraintes max', 'value': self.data[25]})
        if 'durete' in data_usr and _has_value(self.data[23]):
            self.dropdown_values.append({'label': 'Dureté max', 'value': self.data[23]})
        if 'fatigue' in data_usr and _has_value(self.data[24]):
            self.dropdown_values.append({'label': 'Fatigue max', 'value': self.data[24]})
        if 'rugosite' in data_usr and _has_value(self.data[22]):
            self.dropdown_values.append({'label': 'Ra max', 'value': self.data[22]})
        if 'fx' in data_usr and _has_value(self.data[31]):
            self.dropdown_values.append({'label': 'Fx dent max', 'value': self.data[31]})
        if 'fy' in data_usr and _has_value(self.data[32]):
            self.dropdown_values.append({'label': 'Fy dent max', 'value': self.data[32]})
        if 'fz' in data_usr and _has_value(self.data[33]):
            self.dropdown_values.append({'label': 'Fz dent max', 'value': self.data[33]})
        if 'temperature' in data_usr and _has_value(self.data[21]):
            self.dropdown_values.append({'label': 'Température pièce max', 'value': self.data[21]})
        if 'longueur_usine' in data_usr and _has_value(self.data[16]):
            self.dropdown_values.append({'label': 'Longueur usinée', 'value': self.data[16]})
        if 'amplitude' in data_usr and _has_value(self.data[len(self.data) - 2]):
            self.dropdown_values.append({'label': 'Amplitude', 'value': self.data[len(self.data) - 2]})



        # valeurs du dropdown pour l'abscisse pour le line chart
        self.abscisse_values = [
            {'label': 'Temps (s)', 'value': 1},
            {'label': 'Fx pièce (N)', 'value': 2},
            {'label': 'Fy pièce (N)', 'value': 3},
            {'label': 'Fz pièce (N)', 'value': 4},
            {'label': 'Fx outil (N)', 'value': 5},
            {'label': 'Fy outil (N)', 'value': 6},
            {'label': 'Fz outil (N)', 'value': 7}
        ]

        # valeurs des dropdowns pour l'ordonnée pour le line chart
        self.ord_values = [
            {'label': 'Fx pièce (N)', 'value': 1},
            {'label': 'Fy pièce (N)', 'value': 2},
            {'label': 'Fz pièce (N)', 'value': 3},
            {'label': 'Fx outil (N)', 'value': 4},
            {'label': 'Fy outil (N)', 'value': 5},
            {'label': 'Fz outil (N)', 'value': 6}
        ]

        self.modes_courbe = [
            {'label': 'Moyenne', 'value': 1},
            {'label': 'Maximum', 'value': 2},
        ]

        # Affichage des données du procede
        self.info_procede = dbc.Row([
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type de procédé", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[2], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='type-procede'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type d'opération", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[3], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='type-operation'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Assistance", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[4], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='assistance'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Débit mql (ml/h)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[5], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='debit-mql'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Débit cryo (ml/h)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[6], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='debit-cryo'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Emulsion HP (bar)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[7], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='emulsion'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Vc (mm/min)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[8], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='vc'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("fz (mm/dent)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[9], style={'text-align': 'center', 'font-size': '18px',
                                                'font-weight': 'bold'}, id='fz_mm'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Ap (mm)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[10], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='ap'),
                ], style={"marginRight": "10px", "border-radius": "10px", "background-color": '#ECECEC',
                          'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Engagement (%)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[11], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='engagement'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
        ], style={"display": "flex", 'overflow-y': 'scroll', "white-space": "nowrap", 'height': '110px'})

        # Affichage des données de l'entree à la piece
        self.info_piece = dbc.Row([

            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type de Matière", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[12], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='type-matiere-piece'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Matière", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[13], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='matiere-piece'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Procédé d'élaboration", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[14], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='procede-elab'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Impression 3D", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[15], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='imp-3d'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Longueur usinée (mm)", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[16], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='lg-usine'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Numéro de passe", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[17], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='num-passe'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
        ], style={"display": "flex", "overflow-x": "hidden", "white-space": "nowrap", 'height': '110px'})

        # Affichage des données de l'entree à l'outil'
        self.info_outil = dbc.Row([
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Code produit", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P("", style={'text-align': 'center', 'font-size': '18px',
                                      'font-weight': 'bold'}, id='code-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Type d'outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[26], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='type-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Matière outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[27], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='matiere-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Diamètre outil", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[28], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='diametre-outil'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Dents utilisées", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[29], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='dents'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            ),
            dbc.Col(
                [
                    html.Div(
                        [
                            html.P("Revêtement", style={'text-align': 'center', 'width': '120px'}),
                        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                                  'height': '50%'}
                    ),
                    html.P(self.data[30], style={'text-align': 'center', 'font-size': '18px',
                                                 'font-weight': 'bold'}, id='revet'),
                ],
                style={"display": "inline-block", "marginRight": "10px", "border-radius": "10px",
                       "background-color": '#ECECEC',
                       'border-color': '#ECECEC', 'margin-bottom': '10px', 'height': '100px'},
            )
        ], style={"display": "flex", "overflow-x": "hidden", "white-space": "nowrap", 'height': '110px'})

        # dropdown pour l'abscisse du line chart
        self.courbe_abs_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-abs', options=self.abscisse_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2)
        ], justify='left', id='var-courbe-abs')

        # dropdowns pour l'ordonnée du line chart
        self.courbe_ord_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown-ord1', options=self.ord_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(dbc.Button("Ajouter", id='btn-add-var-courbe-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Effacer", id='btn-del-var-courbe-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Valider", id='btn-val-var-courbe-ord', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1)
        ], justify='left', id='var-courbe-ord')

        # dropdowns pour le radar chart
        self.radar_var = dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='dropdown1', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown2', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown3', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(
                dcc.Dropdown(id='dropdown4', options=self.dropdown_values,
                             style={'background-color': '#ECECEC', 'border-color': 'black', 'font-size': '12px'}),
                width=2),
            dbc.Col(dbc.Button('Ajouter', id='btn-add-var-radar', n_clicks=0, outline=True, className='mr-2',
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button('Effacer', id='btn-del-var-radar', n_clicks=0, outline=True, className='mr-2',
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1),
            dbc.Col(dbc.Button("Valider", id='btn-val-var-radar', n_clicks=0, outline=True, className="mr-2",
                               style={'background-color': '#ECECEC', 'border-color': 'black'}), width=1)
        ], justify='left', id='var-radar')

        # Menu vertical à gauche
        self.menu = html.Div([
            html.H2('Dashboard',
                    style={'color': 'white', 'background-color': '#363740', 'padding': '10px', 'font-family': 'Abang',
                           'text-align': 'center'}),
            html.Button('Informations générales', id='btn-info', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}),
            html.Button('Visualisation en radar', id='btn-radar', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'}),
            html.Button('Visualisation en bar', id='btn-courbe', n_clicks=0,
                        style={'color': 'white', 'margin-bottom': '10px', 'padding': '10px',
                               'width': '100%',
                               'background-color': '#363740', 'border': 'none', 'font-family': 'Abang'})
        ], className='menu', style={'backgroundColor': '#363740', 'height': '100%', 'width': '200px'})

        # Définition du layout de l'application
        self.app.layout = html.Div([
            dbc.Row([
                dbc.Col([
                    self.menu,
                ], width=2),
                dbc.Col([
                    dbc.Row([
                        html.Div([
                            html.Div(
                                style={
                                    'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'
                                },
                                children=[
                                    html.H2(id='info-title', children="Expérience \'" + self.data[1] + "\'"),
                                    html.Div(
                                        style={'display': 'flex', 'align-items': 'center', 'margin-right': '30px',
                                               "border-radius": "10px",
                                               'border': '1px solid #000000', "background-color": '#ECECEC',
                                               'width': '20vh', 'height': '10vh',
                                               'justify-content': 'center'},
                                        children=[
                                            html.P("Distance", style={'font-weight': 'bold', 'margin-right': '10px'}),
                                            html.P(self.data[len(self.data) - 1])
                                        ]
                                    )
                                ],
                            ),

                            html.Legend("Procédé", style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                                                          'font-size': '20px'}),
                            html.Div(id="content-info-procede", children=[self.info_procede]),
                            html.Legend("Pièce à usiner",
                                        style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                                               'font-size': '20px'}),
                            html.Div(id="content-info-piece", children=[self.info_piece]),
                            html.Legend("Outil d'usinage",
                                        style={'font-family': 'Abang', 'color': 'gray', 'padding': '20px',
                                               'font-size': '20px'}),
                            html.Div(id="content-info-outil", children=[self.info_outil]),
                            html.Button("Exporter experience", id="export", n_clicks=0)
                        ], className='content', id='content_infos', style={'display': 'block', 'width': '80vh'}),
                        html.Div([
                            html.H2(id='title', children="Visualisation en radar", style={'margin-bottom': '20px'}),
                            html.H2(id='sub-title-radar', children="Choix des paramètres", style={'font-size': '12px'}),
                            html.Div(id="content-radar-container", children=[self.radar_var]),
                            dcc.Graph(id='radar-chart', style={'width': '70vh', 'height': '50vh', 'display': 'none'}),
                            html.Div([
                                html.Div([
                                    html.P("Total:", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                    html.P(id='total-value',
                                           style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                                ]),
                                html.Div([
                                    html.P("Variable proche:",
                                           style={'font-weight': 'bold', 'display': 'inline-block'}),
                                    html.P(id='near-value',
                                           style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                                ]),
                                html.Div([
                                    html.P("Variable éloigné:",
                                           style={'font-weight': 'bold', 'display': 'inline-block'}),
                                    html.P(id='far-value',
                                           style={'margin': '0px', 'display': 'inline-block', 'padding-left': '10px'})
                                ])
                            ], id='info-radar', style={
                                'position': 'absolute',
                                'top': '30vh',
                                'right': '20vh',
                                'height': '40vh',
                                'width': '50vh',
                                'padding': '20px',
                                'background-color': '#f9f9f9',
                                'border': '1px solid #d3d3d3',
                                'border-radius': '5px'
                            })
                        ], className='content', id='content_radar', style={'display': 'none'}),
                        html.Div([
                            html.H2(id='courbe-title', children="Visualisation en Bar",
                                    style={'margin-bottom': '20px'}),
                            html.H2(id='sub-title-abs', children="Choix de l'abscisse", style={'font-size': '12px'}),
                            html.Div(id="content-courbe-container-abs", children=[self.courbe_abs_var],
                                     style={'margin-bottom': '20px'}),
                            html.H2(id='sub-title-ord', children="Choix des ordonnées", style={'font-size': '12px'}),
                            html.Div(id="content-courbe-container-ord", children=[self.courbe_ord_var],
                                     style={'margin-bottom': '20px'}),
                            dcc.Graph(id='courbe-chart', style={'width': '100vh', 'height': '60vh'}),
                            html.Div([
                                html.Div([
                                    html.P("Mode ", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                    ]),
                                html.Div([
                                  dcc.Dropdown(id='mode-value', options=self.modes_courbe, style={'display': 'inline-block', 'padding-left': '5vh', 'width': '30vh'})
                                ]),
                                html.Div([
                                    html.P("Formule", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                ]),
                                html.Div([
                                    dcc.Textarea(
                                            id='formula',
                                            value='sqrt(y), ..',
                                            style={'width': '40vh', 'display': 'inline-block', 'padding-left': '5vh'}
                                        ),
                                ]),
                                html.Div([
                                    html.P("Erreurs", style={'font-weight': 'bold', 'display': 'inline-block'}),
                                ]),
                                html.Div([], id='f-output')
                            ], id='info-mode', style={
                                'position': 'absolute',
                                'top': '40vh',
                                'right': '5vh',
                                'height': '40vh',
                                'width': '50vh',
                                'padding': '20px',
                                'background-color': '#f9f9f9',
                                'border': '1px solid #d3d3d3',
                                'border-radius': '5px'
                            })
                        ], className='content', id='content_courbe', style={'display': 'none'})
                    ])
                ], style={'padding-top': '20px', 'padding-bottom': '20px'}),
            ], className='wrapper', style={'height': '100vh'})
        ], style={'overflow-x': 'hidden'})  # Ajout d'un padding pour espacer le contenu du haut et du bas de la page

