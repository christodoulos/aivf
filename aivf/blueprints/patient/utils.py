from flask import url_for
from requests import get, post
from lib.flask_requests import flask_get


def fetch_existing(patient_id, slide_id, well):
    data = flask_get(
        "api.patient_patient_missing",
        patient_id=patient_id,
        slide_id=slide_id,
        well=well,
    ).json()
    # TODO: convert field names somehow in Model defn ?
    data["fetal_heart_beat"] = data.pop("Fetal Heart Beat")
    data["live_born"] = data.pop("Live Born")
    data["morphological_grade_value"] = data.pop("Morphological Grade - Value")
    return data


def fetch_missing(patient_id, slide_id, well):
    return flask_get(
        "api.patient_from_steve", case_id="{}:{}:{}".format(patient_id, slide_id, well)
    ).json()


def sanitized_form_data(patient_id, slide_id, well, form_data):
    _id = "{}:{}:{}".format(patient_id, slide_id, well)
    form_data["_id"] = _id
    form_data["Fetal Heart Beat"] = form_data.pop("fetal_heart_beat")
    form_data["Live Born"] = form_data.pop("live_born")
    form_data["Morphological Grade - Value"] = form_data.pop(
        "morphological_grade_value"
    )
    form_data.pop("csrf_token")
    print("In sanitized form data")
    print(form_data)
    return form_data


def push_missing(patient_id, slide_id, well, data):
    endpoint = url_for(
        "api.patient_patient_missing",
        _external=True,
        patient_id=patient_id,
        slide_id=slide_id,
        well=well,
    )
    r = post(endpoint, sanitized_form_data(patient_id, slide_id, well, data))
    return r.status_code


def fetch_welldata(patient_id, slide_id, well):
    endpoint = url_for(
        "api.patient_patient_case",
        _external=True,
        _scheme="http",
        patient_id=patient_id,
        slide_id=slide_id,
        well=well,
    )
    r = get(endpoint)
    # TODO: examine if r==None ?
    data = r.json()
    return data["fertilized"]
