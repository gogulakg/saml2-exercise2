from setuptools import setup, find_packages

setup(
    name='saml2_exercise',
    version="0.1",
    author='GEANT',
    author_email='swd@geant.org',
    description='SAML2 Devops Assessment',
    url='https://github.com/erik-geant/saml2_exercise',
    packages=find_packages(include=['flask_saml2*']),
    install_requires=[
        'attrs>=18.1.0',
        'Flask>=1.0.0',
        'signxml>=2.4.0',
        'lxml>=3.8.0',
        'pyopenssl<18',
        'defusedxml>=0.5.0',
        'pytz>=0',
        'iso8601~=0.1.12',
        'flask_saml2'
    ]
)
