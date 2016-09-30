import pytest
from eve import Eve
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestSuite:

    def test_myview(self):
        assert self.client.get(url_for('accounts')).status_code == 200


app = Eve(settings='settings.py')

if __name__ == '__main__':
    app.run(debug=True)
