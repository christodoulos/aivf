from bson import json_util
import json


def bsondate(d):
    # Awful hack to convert bson date to python datetime
    a = str(d).replace("'", '"')
    return json.loads('{}'.format(a),
                      object_hook=json_util.object_hook).strftime('%d/%m/%Y')
