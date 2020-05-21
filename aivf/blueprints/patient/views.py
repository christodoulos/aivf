from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required

from requests import codes
from lib.flask_requests import flask_get

from .forms import QueryPatientForm, EditPatientForm
from .utils import fetch_existing, fetch_welldata, push_missing, fetch_missing

patient = Blueprint("patient", __name__, template_folder="templates")


@patient.route("/query", methods=["GET", "POST"])
@login_required
def patient_query():
    form = QueryPatientForm()
    if form.validate_on_submit():
        patient_id = form.patient_id.data
        cases = flask_get("api.patient_patient_all_cases", patient_id=patient_id)
        if cases.status_code == codes.not_found:
            flash("Patient ID not found: {}".format(patient_id), "error")
        else:
            return render_template(
                "patient/patient_cases.html", patient_id=patient_id, cases=cases.json()
            )
    return render_template("patient/patient_query.html", form=form)


@patient.route("/missing", methods=["GET", "POST"])
def patient_missing():
    patient_id = request.args.get("patient_id")
    slide_id = request.args.get("slide_id")
    well = request.args.get("well")
    welldata = fetch_welldata(patient_id, slide_id, well)
    missing = fetch_missing(patient_id, slide_id, well)
    if request.method == "GET":
        data = fetch_existing(patient_id, slide_id, well)
        if missing:
            missing["fetal_heart_beat"] = missing.pop("Fetal Heart Beat", "")
            missing["live_born"] = missing.pop("Live Born", "")
            missing["morphological_grade_value"] = missing.pop(
                "Morphological Grade - Value", ""
            )
            tralala = {k: v for k, v in missing.items() if v}
        else:
            tralala = {}
        print(missing)
        print("======================================================================")
        # tralala is merged with data for form initialization but finally unmerged data
        # is passed to template! SATANIC and by accident
        print({**data, **tralala})
        print("======================================================================")
        form = EditPatientForm(data={**data, **tralala})
    else:
        form = EditPatientForm()
    if form.validate_on_submit():
        action = push_missing(patient_id, slide_id, well, form.data)
        print("======================================================================")
        print(action)
        print("======================================================================")
        flash(
            "Values updated for case {}:{}:{}".format(patient_id, slide_id, well),
            "success",
        )
        return redirect("/patient/display/{}/{}/{}".format(patient_id, slide_id, well))
    return render_template(
        "patient/patient_missing.html",
        patient_id=patient_id,
        slide_id=slide_id,
        data=data,
        welldata=welldata,
        well=int(well),
        form=form,
        missing=missing,
    )


@patient.route("/display/<string:patient_id>/<string:slide_id>/<string:well>")
@login_required
def case_display(patient_id, slide_id, well):
    r = flask_get(
        "api.patient_patient_case", patient_id=patient_id, slide_id=slide_id, well=well
    )
    data = r.json()
    missing = fetch_missing(patient_id, slide_id, well)
    return render_template(
        "patient/patient_case_details.html",
        patient_id=patient_id,
        slide_id=slide_id,
        well=int(well),
        welldata=data["fertilized"],
        have_images=data["have_images"],
        image=data["image"],
        medical=data["medical"],
        missing=missing,
    )
