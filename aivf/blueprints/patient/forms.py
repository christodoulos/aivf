from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QueryPatientForm(FlaskForm):
    patient_id = StringField('Patient ID', [DataRequired()])
    submit = SubmitField('Submit')


class EditPatientForm(FlaskForm):
    #  steve = [
    #      'Fetal Heart Beat', 'Live Born', 'tPB2', 'tPNa', 'tPNf', 't2', 't3',
    #      't4', 't5', 't6', 't7', 't8', 't9', 'tSC', 'tM', 'tSB', 'tB', 'tEB',
    #      'tHB', 'tDead', 'Morphological Grade - Value'
    #  ]
    fetal_heart_beat = StringField('Fetal Heart Beat')
    live_born = StringField('Live Born')
    tPB2 = StringField('tPB2')
    tPNa = StringField('tPNa')
    tPNf = StringField('tPNf')
    t2 = StringField('t2')
    t3 = StringField('t3')
    t4 = StringField('t4')
    t5 = StringField('t5')
    t6 = StringField('t6')
    t7 = StringField('t7')
    t8 = StringField('t8')
    t9 = StringField('t9')
    tSC = StringField('tSC')
    tM = StringField('tM')
    tSB = StringField('tSB')
    tB = StringField('tB')
    tEB = StringField('tEB')
    tHB = StringField('tHB')
    tDead = StringField('tDead')
    morphological_grade_value = StringField('Morphological Grade - Value')
