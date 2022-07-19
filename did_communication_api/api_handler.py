import logging
import requests
import sys

from did_communication_api import utils, constants
from did_communication_api.errors import MyDIDCommError


class ApiHandler:

  def __init__(self, did_comm, server_did):
    self.did_comm = did_comm
    self.server_did = server_did

  def __respond_with_error_encrypted(self, error_msg, http_code, didcomm_receiver):
    response_message_encrypted = self.did_comm.pack(
      msg_body={'error': error_msg},
      to=didcomm_receiver,
      frm=self.server_did,
      msg_type=constants.DIDCOMM_ERROR_MSG_TYPE,
      msg_id=None
    )
    return {'didcomm_msg': response_message_encrypted}, http_code

  def handle_message_received(self, didcomm_packed_msg, http_method):
    # Unpack message
    try:
      message_unpacked_dict = self.did_comm.unpack(didcomm_packed_msg)
    except MyDIDCommError:
      logging.warning(constants.INVALID_REQUEST_RECEIVED.format(
        "Could not decrypt/authenticate DIDComm Message"))
      return utils.generate_err_resp('Invalid DIDComm Message', constants.HTTP_BAD_REQUEST)

    # logging.info(constants.DIDCOMM_MESSAGE_RECEIVED.format(
    #   msg_id=message_unpacked_dict['msg_id'], msg_type=message_unpacked_dict['msg_type']
    # ))

    # Notify ADP
    webhook_response = webhook_new_request_received(
      sender=message_unpacked_dict['frm'],
      http_request_method=http_method,
      msg_body=message_unpacked_dict['msg_body'],
      msg_type=message_unpacked_dict['msg_type'],
      msg_id=message_unpacked_dict['msg_id'],
      attachments=message_unpacked_dict['attachments']
    )

    if not is_webhook_response_valid(webhook_response):
      logging.error("Received an invalid response from Webhook. Responding to client with HTTP 500")
      return self.__respond_with_error_encrypted(
        'Internal Server Error', constants.HTTP_INTERNAL_ERROR, message_unpacked_dict['frm'])

    if 'error' in webhook_response:
      logging.error("Received an Error response from Webhook. Responding to client with HTTP 500")
      return self.__respond_with_error_encrypted(
        'Internal Server Error', constants.HTTP_INTERNAL_ERROR, message_unpacked_dict['frm'])

    # Encrypt + Authenticate Response
    response_didcomm_parsed = parse_didcomm_webhook_response(webhook_response)
    response_message_encrypted = self.did_comm.pack(
      msg_body=response_didcomm_parsed['body'],
      to=message_unpacked_dict['frm'],
      frm=self.server_did,
      msg_type=response_didcomm_parsed['type'],
      msg_id=response_didcomm_parsed['id']
    )

    # logging.info(constants.SENDING_RESPONSE.format(
    #   req_msg_id=message_unpacked_dict['msg_id'],
    #   resp_msg_type=response_didcomm_parsed['type'],
    #   resp_http_code=response_didcomm_parsed['http_code']
    # ))
    return {'didcomm_msg': response_message_encrypted}, response_didcomm_parsed['http_code']


def is_webhook_response_valid(webhook_response):
  """
  Validates whether the response of the Webhook is of expected format.

  Expected Webhook response structure:
  {
    'response': {
      'http_code': <response_http_code>,
      'type': 'DIDComm',
      'message': {
        'id': <Response DIDComm Message ID>,
        'type': <Response DIDComm Message Type>,
        'body': <Response DIDComm Message Body>
      }
    }
  }
  or
  {
    'error': '<Error>'
  }

  :param webhook_response: The webhook response
  :return: True iff response valid
  """
  if not webhook_response:
    return False

  if 'error' in webhook_response:
    return True

  if (
    'response' not in webhook_response or
    'type' not in webhook_response['response'] or
    'http_code' not in webhook_response['response']
  ):
    logging.error('Unexpected response from Received_message_webhook!')
    return False

  if webhook_response['response']['type'] == constants.REQUEST_DIDCOMM:
    if (
      'message' not in webhook_response['response'] or
      'id' not in webhook_response['response']['message'] or
      'type' not in webhook_response['response']['message'] or
      'body' not in webhook_response['response']['message']
    ):
      logging.error('Unexpected response from Received_message_webhook!')
      return False
    return True

  logging.error('Webhook requested unsupported communication protocol: {}'.format(
    webhook_response['response']['type']))
  return False


def parse_didcomm_webhook_response(webhook_response):
  """
  Webhook Response Structure:
  {
    'response': {
      'http_code': <response_http_code>,
      'type': 'DIDComm',
      'message': {
        'id': <Response DIDComm Message ID>,
        'type': <Response DIDComm Message Type>,
        'body': <Response DIDComm Message Body>
      }
    }
  }
  :param webhook_response:
  :return:
  """
  return {
    'http_code': webhook_response['response']['http_code'],
    'body': webhook_response['response']['message']['body'],
    'id': webhook_response['response']['message']['id'],
    'type': webhook_response['response']['message']['type'],
  }


def webhook_new_request_received(sender, http_request_method, msg_body, msg_type, msg_id, attachments):
  """
  Sends a POST Request to the configured webhook for received requests.
  The body of the request is:
  {
    'sender': <sender_peer_did>,
    'request': {
      'type': 'DIDComm',
      'http_request_method': <http_request_method>,
      'message': {
        'id': <Message ID>,
        'type': <Message Type>,
        'body': <Message Body>,
        'attachments': <List of DIDComm attachments>
      }
    },
  }

  :param sender: sender_peer_did
  :param http_request_method: The HTTP Request Method of the Client's Request
  :param msg_body: Message Body
  :param msg_type: Message Type
  :param msg_id: Message ID
  :param attachments: List of DIDComm attachments
  :return: Webhook's response json data
  """

  webhooks_configuration = utils.load_component_configuration("webhooks")
  if not webhooks_configuration or 'request_received' not in webhooks_configuration:
    logging.error("Invalid Configuration: Missing webhooks configuration")
    sys.exit(1)
  webhook_url = webhooks_configuration['request_received']

  received_request_data = {
    'sender': sender,
    'request': {
      'type': constants.REQUEST_DIDCOMM,
      'http_request_method': http_request_method,
      'message': {
        'id': msg_id,
        'type': msg_type,
        'body': msg_body,
        'attachments': attachments
      }
    }
  }

  return __post_to_webhook(webhook_url, received_request_data)


def __post_to_webhook(url, request_data):
  try:
    response = requests.post(url, json=request_data)
  except requests.exceptions.RequestException as requests_error:
    logging.error(f'Got RequestException when posting to webhook: {str(requests_error)}')
    return None
  return response.json()
