from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from model.__init__ import Base


class Procede(Base):
    """Classe du modèle représentant le procede d'une expérience"""
    __tablename__ = 'procede'

    # Attributs de la table
    id_procede = Column(Integer, primary_key=True)
    type_procede = Column(VARCHAR(15))
    type_operation = Column(VARCHAR(15))
    assistance = Column(VARCHAR(15))
    debit_mql = Column(VARCHAR(15))
    debit_cryo = Column(VARCHAR(15))
    emulsion = Column(VARCHAR(15))
    vitesse_coupe = Column(VARCHAR(15))
    vitesse_avance_dent = Column(VARCHAR(15))
    profondeur_passe = Column(VARCHAR(15))
    engagement = Column(VARCHAR(15))
    vitesse_avance_min = Column(VARCHAR(15))
    frequence_rotation = Column(VARCHAR(15))

    # Table parent
    id_experience = Column(Integer, ForeignKey('experience.id_experience'))
    experience = relationship("Experience", back_populates="procede", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe procede"""
        if not len(args) == 0:
            self.type_procede = args[0]
            self.type_operation = args[1]
            self.assistance = args[2]
            self.debit_mql = args[3]
            self.debit_cryo = args[4]
            self.emulsion = args[5]
            self.vitesse_coupe = args[6]
            self.vitesse_avance_dent = args[7]
            self.profondeur_passe = args[8]
            self.engagement = args[9]
            self.vitesse_avance_min = args[10]
            self.frequence_rotation = args[11]
            self.experience = args[12]

    def __eq__(self, other):
        """Fonction qui compare deux objets procede

        Parameters
        ----------
        other : Procede
            L'objet procede à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if self.experience is None:
            if self.type_procede != other.type_procede or self.type_operation != other.type_operation or \
                    self.assistance != other.assistance or self.debit_mql != other.debit_mql or \
                    self.debit_cryo != other.debit_cryo or self.emulsion != other.emulsion or \
                    self.vitesse_coupe != other.vitesse_coupe or self.vitesse_avance_dent != other.vitesse_avance_dent or \
                    self.profondeur_passe != other.profondeur_passe or self.engagement != other.engagement or \
                    self.vitesse_avance_min != other.vitesse_avance_min or self.frequence_rotation != other.frequence_rotation :
                return False
        else:
            if self.type_procede != other.type_procede or self.type_operation != other.type_operation or \
                    self.assistance != other.assistance or self.debit_mql != other.debit_mql or \
                    self.debit_cryo != other.debit_cryo or self.emulsion != other.emulsion or \
                    self.vitesse_coupe != other.vitesse_coupe or self.vitesse_avance_dent != other.vitesse_avance_dent or \
                    self.profondeur_passe != other.profondeur_passe or self.engagement != other.engagement or \
                    self.vitesse_avance_min != other.vitesse_avance_min or self.frequence_rotation != other.frequence_rotation or \
                    self.experience.nom != other.experience.nom:
                return False
        return True

    @property
    def __type_procede__(self):
        return self.type_procede

    @__type_procede__.setter
    def __type_procede__(self, type_procede):
        self.type_procede = type_procede

    @property
    def __type_operation__(self):
        return self.type_operation

    @__type_operation__.setter
    def __type_operation__(self, type_operation):
        self.type_operation = type_operation

    @property
    def __assistance__(self):
        return self.assistance

    @__assistance__.setter
    def __assistance__(self, assistance):
        self.assistance = assistance

    @property
    def __debit_mql__(self):
        return self.debit_mql

    @__debit_mql__.setter
    def __debit_mql__(self, debit_mql):
        self.debit_mql = debit_mql

    @property
    def __debit_cryo__(self):
        return self.debit_cryo

    @__debit_cryo__.setter
    def __debit_cryo__(self, debit_cryo):
        self.debit_cryo = debit_cryo

    @property
    def __emulsion__(self):
        return self.emulsion

    @__emulsion__.setter
    def __emulsion__(self, emulsion):
        self.emulsion = emulsion

    @property
    def __vitesse_coupe__(self):
        return self.vitesse_coupe

    @__vitesse_coupe__.setter
    def __vitesse_coupe__(self, vitesse_coupe):
        self.vitesse_coupe = vitesse_coupe

    @property
    def __vitesse_avance_dent__(self):
        return self.vitesse_avance_dent

    @__vitesse_avance_dent__.setter
    def __vitesse_avance_dent__(self, vitesse_avance_dent):
        self.vitesse_avance_dent = vitesse_avance_dent

    @property
    def __profondeur_passe__(self):
        return self.profondeur_passe

    @__profondeur_passe__.setter
    def __profondeur_passe__(self, profondeur_passe):
        self.profondeur_passe = profondeur_passe

    @property
    def __engagement__(self):
        return self.engagement

    @__engagement__.setter
    def __engagement__(self, engagement):
        self.engagement = engagement

    @property
    def __vitesse_avance_min__(self):
        return self.vitesse_avance_min

    @__vitesse_avance_min__.setter
    def __vitesse_avance_min__(self, vitesse_avance_min):
        self.vitesse_avance_min = vitesse_avance_min

    @property
    def __frequence_rotation__(self):
        return self.frequence_rotation

    @__frequence_rotation__.setter
    def __frequence_rotation__(self, frequence_rotation):
        self.frequence_rotation = frequence_rotation

    @property
    def __experience__(self):
        return self.experience

    @__experience__.setter
    def __experience__(self, experience):
        self.experience = experience
