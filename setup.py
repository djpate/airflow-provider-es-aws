"""Setup.py for ES AWS Provider"""

from setuptools import find_packages, setup

"""Perform the package airflow-provider-sample setup."""
setup(
    name='airflow-provider-es-aws',
    version="0.0.1",
    description='A airflow provider for elasticsearch using aws v4 signature.',
    long_description='A airflow provider for elasticsearch using aws v4 signature.',
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=es_aws_provider.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['es_aws_provider', 'es_aws_provider.hooks'],
    install_requires=[
        'apache-airflow>=2.0',
        'apache-airflow-providers-elasticsearch>=3.0',
        'boto3>=1.21.19',
        'requests-aws4auth>=1.1.1'],
    setup_requires=['setuptools', 'wheel'],
    author='Christophe Verbinnen',
    author_email='christophe@verbinnen.org',
    python_requires='~=3.7',
)
