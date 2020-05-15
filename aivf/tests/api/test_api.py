from flask import url_for


class TestApi(object):
    def test_patient_collection(self, client):
        assert True


class TestPage(object):
    def test_home_page(self, client):
        """ Home page should respond with a success 200. """
        response = client.get(url_for('page.home'))
        assert response.status_code == 200
