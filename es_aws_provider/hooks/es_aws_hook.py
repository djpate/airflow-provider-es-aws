#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from typing import Optional

import boto3

from requests_aws4auth import AWS4Auth
from es.elastic.api import Connection as ESConnection, connect

from airflow.hooks.dbapi import DbApiHook
from airflow.models.connection import Connection as AirflowConnection
from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchHook


class EsAWSHook(ElasticsearchHook):
    """
    Interact with Elasticsearch through the elasticsearch-dbapi.
    This hook uses the Elasticsearch conn_id.
    :param elasticsearch_conn_id: The :ref:`ElasticSearch connection id <howto/connection:elasticsearch>`
        used for Elasticsearch credentials.
    """

    conn_name_attr = 'es_aws_conn_id'
    default_conn_name = 'es_aws_default'
    conn_type = 'es_aws'
    hook_name = 'EsAWS'

    @staticmethod
    def get_connection_form_widgets():
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField, BooleanField

        return {
            "extra__es_aws__region": StringField(
                lazy_gettext('AWS Region'), widget=BS3TextFieldWidget()
            ),
            "extra__es_aws__profile": StringField(
                lazy_gettext('AWS Profile Name'), widget=BS3TextFieldWidget()
            ),
            "extra__es_aws__role": StringField(
                lazy_gettext('AWS Role ARN'), widget=BS3TextFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour():
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": [],
            "relabeling": {
              'login': 'AWS Access Key',
              'password': 'AWS Secret Key',
            },
            "placeholders": {
                'host': 'search.example.com',
                'schema': 'https',
                'login': 'AKAIHX2XQZLQ7U...',
                'password': 'Secret key',
                'extra__es_aws__region': 'us-east-1',
                'extra__es_aws__role': 'arn:aws:iam::123456789012:role/role-name',
            },
        }

    def __init__(self, schema: str = "http", connection: Optional[AirflowConnection] = None, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.schema = schema
      self.connection = connection

    def get_conn(self) -> ESConnection:
        """Returns a elasticsearch connection object"""
        conn_id = getattr(self, self.conn_name_attr)
        conn = self.connection or self.get_connection(conn_id)

        session = boto3.Session()
        credentials = session.get_credentials()
        if conn.login and conn.password:
          awsauth = AWS4Auth(conn.login, conn.password, conn.extra__es_aws__region or session.region_name, 'es')
        else:
          awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, conn.extra__es_aws__region or session.region_name, 'es', session_token=credentials.token)

        conn_args = dict(
            host=conn.host,
            port=conn.port,
            http_auth = awsauth,
            scheme=conn.schema or "http",
        )

        if conn.extra_dejson.get('http_compress', False):
            conn_args["http_compress"] = bool(["http_compress"])

        if conn.extra_dejson.get('timeout', False):
            conn_args["timeout"] = conn.extra_dejson["timeout"]

        conn = connect(**conn_args)

        return conn