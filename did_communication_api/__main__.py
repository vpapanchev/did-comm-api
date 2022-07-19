# -*- coding: utf-8 -*-

"""Main module."""

import logging

from flask import request

from did_communication_api import app_configurer, utils, constants
from did_communication_api.api_handler import ApiHandler
from did_communication_api.did_comm.did_comm import DIDComm
from did_communication_api.did_comm.secret_resolver import SecretsResolverLocal

# Initialize Flask Application
flask_app = app_configurer.initialize_flask_app(__name__)

# Initialize Secret Resolver and DIDComm
secret_resolver = SecretsResolverLocal()
did_comm = DIDComm(secret_resolver)

# Generate the Server's Peer DID
server_did = app_configurer.create_server_did(did_comm)
logging.info(f'Server DID: {server_did}')

# Initialize the API Handler
api_handler = ApiHandler(did_comm, server_did)


@flask_app.route('/-system/liveness')
def check_system_liveness():
  return 'ok', constants.HTTP_SUCCESS_STATUS


@flask_app.route(constants.API_EXTERNAL_INBOX, methods=['GET', 'POST', 'PUT', 'DELETE'])
def receive_message():
  # Used by other systems to send HTTP Requests with encrypted (DIDComm) Payload
  http_method = request.method
  packed_msg = request.form.get('didcomm_msg')
  if not packed_msg:
    logging.warning("Received HTTP Request with invalid body structure. Missing didcomm_msg attribute")
    return utils.generate_err_resp('Missing didcomm_msg', constants.HTTP_BAD_REQUEST)

  return api_handler.handle_message_received(packed_msg, http_method)


if __name__ == '__main__':
  server_config = utils.load_component_configuration('server')
  flask_app.run(debug=server_config['debug'], port=server_config['port'], host=server_config['host'])
