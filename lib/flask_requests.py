from flask import url_for
from requests import get, post, codes, exceptions


def secure_get(flask_route_string, **kwargs):
    endpoint = url_for(flask_route_string, _external=True, _scheme="https", **kwargs)
    try:
        r = get(endpoint)
    except exceptions.SSLError:
        r = get(endpoint, verify="cert.pem")
    # TODO: What happens if r==None?
    return r.json()


def flask_get(flask_route_string, **kwargs):
    endpoint = url_for(flask_route_string, _external=True, **kwargs)
    print(endpoint)
    #  r = get(endpoint)
    #  if r.status_code == codes.not_found:
    #      return {"message": "Not Found!"}, 404
    #  return r
    return get(endpoint)
