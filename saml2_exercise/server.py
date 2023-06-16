from flask import Flask, url_for
from pathlib import Path
from flask_saml2.sp import ServiceProvider
from flask_saml2.utils import certificate_from_file, private_key_from_file

KEY_DIR = Path(__file__).parent.parent / 'keys' / 'sample'
print(KEY_DIR)
IDP_CERTIFICATE_FILE = KEY_DIR / 'idp-certificate.pem'
CERTIFICATE_FILE = KEY_DIR / 'sp-certificate.pem'
PRIVATE_KEY_FILE = KEY_DIR / 'sp-private-key.pem'

CERTIFICATE = certificate_from_file(CERTIFICATE_FILE)
PRIVATE_KEY = private_key_from_file(PRIVATE_KEY_FILE)
IDP_CERTIFICATE = certificate_from_file(IDP_CERTIFICATE_FILE)

print(IDP_CERTIFICATE)

class ExampleServiceProvider(ServiceProvider):
    def get_logout_return_url(self):
        return url_for('index', _external=True)

    def get_default_login_return_url(self):
        return url_for('index', _external=True)


sp = ExampleServiceProvider()

app = Flask(__name__)
app.debug = True
app.secret_key = 'hack me'

app.config['SERVER_NAME'] = 'localhost:8989'
app.config['SAML2_SP'] = {
    'certificate': CERTIFICATE,
    'private_key': PRIVATE_KEY,
}

app.config['SAML2_IDENTITY_PROVIDERS'] = [
    {
        'CLASS': 'flask_saml2.sp.idphandler.IdPHandler',
        'OPTIONS': {
            'display_name': 'My Identity Provider',
            'entity_id': 'https://test-idp-o365.geant.org',
            'sso_url': 'https://test-idp-o365.geant.org/saml2/idp/SSOService.php',
            # 'slo_url': 'https://test-idp-o365.geant.org/saml2/idp/SingleLogoutService.php',
            'certificate': IDP_CERTIFICATE,
        },
    },
]


@app.route('/')
def index():
    if sp.is_user_logged_in():
        auth_data = sp.get_auth_data_in_session()

        message = f'''
        <p>You are logged in as <strong>{auth_data.nameid}</strong>.
        The IdP sent back the following attributes:<p>
        '''

        attrs = '<dl>{}</dl>'.format(''.join(
            f'<dt>{attr}</dt><dd>{value}</dd>'
            for attr, value in auth_data.attributes.items()))

        logout_url = url_for('flask_saml2_sp.logout')
        logout = f'<form action="{logout_url}" method="POST"><input type="submit" value="Log out"></form>'

        return message + attrs + logout
    else:
        message = '<p>You are logged out.</p>'

        login_url = url_for('flask_saml2_sp.login')
        link = f'<p><a href="{login_url}">Log in to continue</a></p>'

        return message + link


app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
