import sys
import os
import re
import logging
import asyncio
from yaml import safe_load, YAMLError

from did_communication_api import constants


def load_component_configuration(component_name):
  if not re.fullmatch(constants.VALID_COMPONENT_NAME_REGEX, component_name):
    logging.error(constants.LOG_INVALID_COMP_NAME,
                  component_name, constants.VALID_COMPONENT_NAME_REGEX)
    return

  if component_name == 'server':
    # Exception for server config due to env variables (dirty fix)
    return get_server_configuration()

  service_config = load_service_config()
  if component_name not in service_config:
    logging.error(constants.LOG_CNF_COMPONENT_MISSING, component_name)
    return
  return service_config[component_name]


def load_service_config():
  def terminate_program_with_message(message):
    print(message)
    sys.exit(1)

  config_file_path = os.getenv(constants.CONFIG_FILE_PATH_ENV_VARIABLE,
                               os.path.join(constants.PROJECT_DIRECTORY, 'config/config.yml'))
  project_config = get_yaml_content(config_file_path, terminate_program_with_message)
  if constants.CONF_SERVICES_NAME not in project_config:
    logging.error(constants.LOG_CNF_NO_SERVICES)
    terminate_program_with_message(constants.LOG_CNF_NO_SERVICES)
  services_config = project_config[constants.CONF_SERVICES_NAME]
  if constants.SERVICE_NAME not in services_config:
    logging.error(constants.LOG_CNF_UNAVAIL_SERVICE)
    terminate_program_with_message(constants.LOG_CNF_UNAVAIL_SERVICE)
  return services_config[constants.SERVICE_NAME]


def get_yaml_content(file_path, callback_on_error=None):
  with open(os.path.join(file_path), 'r') as file:
    try:
      return safe_load(file)
    except YAMLError as error:
      error_msg = constants.LOG_YAML_PARSE_FAIL.format(file, error)
      if callback_on_error:
        callback_on_error(error_msg)
      logging.error(error_msg)


def get_server_configuration():
  server_local_config = load_service_config()['server']
  host = os.getenv('API_HOST', server_local_config['host'])
  port = os.getenv('API_PORT', server_local_config['port'])
  debug = os.getenv('API_DEBIG', server_local_config['debug'])

  return {
    'host': host,
    'port': port,
    'debug': debug
  }


def get_or_create_eventloop():
  try:
    return asyncio.get_event_loop()
  except RuntimeError as ex:
    if "There is no current event loop in thread" in str(ex):
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      return asyncio.get_event_loop()


def generate_err_resp(error_msg, http_code):

  return {
    'error': error_msg
  }, http_code
