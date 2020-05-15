from mongoengine import StringField, DynamicField, DynamicDocument


class Medical(DynamicDocument):
    _id = StringField(primary_key=True)
    patient_id = DynamicField(db_field='Patient ID')
    slide_id = DynamicField(db_field='Slide ID')
    well = DynamicField(db_field='Well')
    fetal_heart_beat = DynamicField(db_field='Fetal Heart Beat')
    live_born = DynamicField(db_field='Live Born')
    morphological_grade_value = DynamicField(
        db_field='Morphological Grade - Value')


class Missing(DynamicDocument):
    _id = StringField(primary_key=True)
    patient_id = DynamicField(db_field='Patient ID')
    slide_id = DynamicField(db_field='Slide ID')
    well = DynamicField(db_field='Well')
    fetal_heart_beat = DynamicField(db_field='Fetal Heart Beat')
    live_born = DynamicField(db_field='Live Born')
    morphological_grade_value = DynamicField(
        db_field='Morphological Grade - Value')


class Metamedical(DynamicDocument):
    _id = StringField(primary_key=True)
    patient_id = DynamicField(db_field='Patient ID')
    slide_id = DynamicField(db_field='Slide ID')
    fwells = DynamicField(db_field='Fertilized Wells')


def Patient(patient_id):
    return type(
        patient_id, (DynamicDocument, ), {
            'meta': {
                'collection': patient_id
            },
            'slide_id': DynamicField(db_field='Slide ID'),
            'well': DynamicField(db_field='Well'),
            'run': DynamicField(db_field='Run'),
        })
