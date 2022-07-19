# -*- coding: utf-8 -*-

import os
import logging
import logging.config

from flask import Flask

from did_communication_api import utils, constants


def initialize_flask_app(name):
  # Do not use server configuration from this service config!
  service_config = utils.load_service_config()

  flask_app = Flask(name)
  configure_logging(service_config)

  logging.info('Flask application initialized')
  return flask_app


def configure_logging(service_config):

  logging_config_path = os.getenv(constants.LOGGING_CNF_PATH_ENV_VAR,
                                  os.path.join(constants.PROJECT_DIRECTORY, 'config/logging.yml'))
  logging_config = utils.get_yaml_content(logging_config_path)
  logging_config['root']['level'] = service_config['logging']['level']
  logging.config.dictConfig(logging_config)


def create_server_did(did_comm):
  # The Service Endpoint used for the Peer DID of this DID_Communication_API
  server_config = utils.load_component_configuration('server')
  my_service_endpoint = 'http://{}:{}{}'.format(
    server_config['host'], server_config['port'], constants.API_EXTERNAL_INBOX)

  # Create new Peer DID
  my_new_did = did_comm.create_peer_did(my_service_endpoint)

  return my_new_did
