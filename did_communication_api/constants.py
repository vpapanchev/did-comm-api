import os
import re

# General service-wide constants
SERVICE_NAME = "did_communication_api"
LOGGING_CNF_PATH_ENV_VAR = 'LOGGING_CNF_PATH'
CONFIG_FILE_PATH_ENV_VARIABLE = 'CONFIG_PATH'
PROJECT_DIRECTORY = os.path.dirname(__file__)

# Configuration structure
CONF_SERVICES_NAME = "services"

# API Endpoints
API_EXTERNAL_INBOX = '/did_comm/inbox/'

# Regexes
VALID_COMPONENT_NAME_REGEX = re.compile('[a-z_]+')

# Messages
LOG_CNF_NO_SERVICES = 'Invalid configuration - No services defined'
LOG_CNF_UNAVAIL_SERVICE = f'Invalid configuration - The service configuration ({SERVICE_NAME}) is missing.'
LOG_CNF_COMPONENT_MISSING = 'Unavailable component configuration: %s. ' \
                            'Provide its configuration in the config.yml.'
LOG_INVALID_COMP_NAME = 'Invalid component name: %s. Component names have the following pattern: %s'
LOG_YAML_PARSE_FAIL = 'YAML file {} could not be parsed - {}'
LOG_EXTERNAL_CON_REQ_VALID = 'Received external connection request with valid content: ' \
                             'Received DID: {} DID Document: {}'
LOG_EXTERNAL_CON_REQ_INVALID = 'Received external connection request with INVALID content: ' \
                               'Received DID: {} DID Document: {}'
LOG_EXTERNAL_CON_RESPONSE_VALID = 'Service {} responded to connection request with valid content: ' \
                                  'Received DID: {} DID Document: {}'
LOG_EXTERNAL_CON_RESPONSE_INVALID = 'Service {} responded to connection request with INVALID content: ' \
                                    'Received DID: {} DID Document: {}'
LOG_CON_EST_TO_SERVICE_FAILED = 'Connection establishment to service {} failed due to: {}'

# HTTP STATUS CODES
HTTP_SUCCESS_STATUS = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# HTTP Error Messages:
HTTP_MSG_INVALID_CON_REQ = "Invalid Connection Request: {}"

# User Request Types
REQUEST_DIDCOMM = "DIDComm"

# DIDComm User Request Message Types
DIDCOMM_INITIAL_REQUEST_MSG_TYPE = "https://uwmbv.solid.aifb.kit.edu/ssi-acs/didcomm/messages/initial-request"
DIDCOMM_REQUEST_PRESENTATION_MSG_TYPE = "https://didcomm.org/present-proof/2.0/request-presentation"
DIDCOMM_PRESENTATION_MSG_TYPE = "https://didcomm.org/present-proof/2.0/presentation"
DIDCOMM_ERROR_MSG_TYPE = "https://uwmbv.solid.aifb.kit.edu/ssi-acs/didcomm/messages/error-message"
DIDCOMM_AUTHORIZATION_DECISION_MSG_TYPE = "http://example.aifb.org/autorization-decision/"

# Attachment formats:
PRESENTATION_REQUEST_ATTACHMENT_FORMAT_PE_DEFINITION = "dif/presentation-exchange/definitions@v1.0"
PRESENTATION_REQUEST_ATTACHMENT_FORMAT_SHACL = "https://uwmbv.solid.aifb.kit.edu/ssi-acs/didcomm/attachments/" \
                                               "required-credentials/SHACL/presentation-request"
PRESENTATION_ATTACHMENT_FORMAT_SHACL = "https://uwmbv.solid.aifb.kit.edu/ssi-acs/didcomm/attachments/" \
                                       "required-credentials/SHACL/presentation"

# Logging
INVALID_REQUEST_RECEIVED = "Received Invalid Request: {}"
DIDCOMM_MESSAGE_RECEIVED = "Received DIDComm Request: Message_ID: {msg_id} Message Type: {msg_type}. " \
                           "Notifying Webhook.."
SENDING_RESPONSE = "Sending HTTP Response: Request_Message_ID: {req_msg_id} " \
                   "Response_Message_Type: {resp_msg_type} Response_HTTP_Code: {resp_http_code}"
