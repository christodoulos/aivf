from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required

from requests import get, post, codes

from .forms import QueryPatientForm, EditPatientForm
from .utils import fetch_existing, fetch_welldata, push_missing

patient = Blueprint("patient", __name__, template_folder="templates")

API = "http://localhost:8000/api/patient/"
API_ALLCASES = API + "allcases/{}"
API_CASE = API + "case/{}/{}/{}"
API_MISSING = API + "missing/{}/{}/{}"


@patient.route("/query", methods=["GET", "POST"])
@login_required
def patient_query():
    form = QueryPatientForm()
    if form.validate_on_submit():
        patient_id = form.patient_id.data
        cases = get(API_ALLCASES.format(patient_id))
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
    if request.method == "GET":
        data = fetch_existing(patient_id, slide_id, well)
        form = EditPatientForm(data=data)
    else:
        form = EditPatientForm()
    if form.validate_on_submit():
        print("==============================================================")
        print(form.data)
        print("==============================================================")
        action = push_missing(patient_id, slide_id, well, form.data)
        print(action)
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
    )


@patient.route("/display/<string:patient_id>/<string:slide_id>/<string:well>")
@login_required
def case_display(patient_id, slide_id, well):
    request = get(API_CASE.format(patient_id, slide_id, well))
    data = request.json()
    return render_template(
        "patient/patient_case_details.html",
        patient_id=patient_id,
        slide_id=slide_id,
        well=int(well),
        welldata=data["fertilized"],
        have_images=data["have_images"],
        image=data["image"],
        medical=data["medical"],
    )
