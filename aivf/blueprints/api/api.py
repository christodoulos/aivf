from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource
from base64 import b64encode

from aivf.blueprints.api.models import Metamedical, Medical, Patient, Missing

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    version="1.0",
    title="AIVF API",
    description="An API for AIVF transactions",
)
patient = api.namespace("patient", description="PATIENT operations")


@patient.route("/allcases/<string:patient_id>")
@patient.param("patient_id", "The patient identifier")
class PatientAllCases(Resource):
    def get(self, patient_id):
        """ Retrieves all cases of <patient_id> Patient """
        cases = Metamedical.objects(patient_id=patient_id)
        if cases:
            return jsonify(cases)
        else:
            return {"message": "Patient not found"}, 404


@patient.route("/case/<string:patient_id>/<string:slide_id>/<string:well>")
@patient.param("patient_id", "The patient identifier")
@patient.param("slide_id", "The slide identifier")
@patient.param("well", "The well identifier")
class PatientCase(Resource):
    def get(self, patient_id, slide_id, well):
        """ Retrives a specific <patient_id> <slide_id> case """
        case = Metamedical.objects.get(patient_id=patient_id, slide_id=slide_id)
        try:
            have_images = case.have_images
            image_id = "{}:{}:1:0".format(slide_id, well)
            #  image = base64.b64encode(
            #      Patient(patient_id).objects.get(
            #          _id=image_id).Image).decode('utf-8')
            raw = Patient(patient_id).objects.only("Image").get(_id=image_id)
            image = b64encode(raw.Image).decode("utf-8")
        except AttributeError:
            have_images = False
            image = None
        medical = Medical.objects.get(
            patient_id=patient_id, slide_id=slide_id, well=well
        )
        return jsonify(
            {
                "fertilized": case.fwells,
                "have_images": have_images,
                "medical": medical,
                "image": image,
            }
        )


@patient.route("/fromsteve/<string:case_id>")
class FromSteve(Resource):
    def get(self, case_id):
        try:
            case = Missing.objects.get(_id=case_id)
        except Missing.DoesNotExist:
            case = None
        print("In FromSteve", jsonify(case))
        return jsonify(case)


@patient.route("/missing/<string:patient_id>/<string:slide_id>/<string:well>")
class PatientMissing(Resource):
    def get(self, patient_id, slide_id, well):
        cases = Medical.objects.only(
            "Fetal Heart Beat",
            "Live Born",
            "tPB2",
            "tPNa",
            "tPNf",
            "t2",
            "t3",
            "t4",
            "t5",
            "t6",
            "t7",
            "t8",
            "t9",
            "tSC",
            "tM",
            "tSB",
            "tB",
            "tEB",
            "tHB",
            "tDead",
            "Morphological Grade - Value",
        ).get(patient_id=patient_id, slide_id=slide_id, well=well)
        return jsonify(cases)

    def post(self, patient_id, slide_id, well):
        data = request.form.to_dict(flat=True)
        not_empty = {k: v for k, v in data.items() if v}
        doc = Missing(**not_empty)
        return jsonify(doc.save())
