""" Secret (Private Key) Resolver. Required for the usage of DIDComm. Stores private keys in local files. """

import json
import logging

from multiprocessing import Lock
from pathlib import Path
from typing import List, Optional

from didcomm.common.types import DID_URL
from didcomm.secrets.secrets_resolver import Secret
from didcomm.secrets.secrets_resolver_editable import SecretsResolverEditable
from didcomm.secrets.secrets_util import jwk_to_secret, secret_to_jwk_dict

lock = Lock()


class SecretsResolverLocal(SecretsResolverEditable):

  def __init__(self, file_path="secrets.json"):
    self.file_path = file_path
    self._init_secrets_file()

  def _init_secrets_file(self):
    logging.info('Initializing secrets file: Waiting to acquire lock')
    lock.acquire()
    try:
      if not Path(self.file_path).exists():
        Path(self.file_path).touch()
        logging.info('Created secrets file: {}'.format(self.file_path))
      else:
        logging.info('Secrets file already created.')
    finally:
      logging.info('Releasing lock')
      lock.release()

  def _read_secrets(self):
    with open(self.file_path) as f:
      try:
        jwk_keys = json.load(f)
      except json.decoder.JSONDecodeError:
        jwk_keys = []
      return {jwk_key["kid"]: jwk_to_secret(jwk_key) for jwk_key in jwk_keys}

  def _write_secrets(self, secrets_dict):
    with open(self.file_path, 'w') as f:
      secrets_as_jwk = [secret_to_jwk_dict(s) for s in secrets_dict.values()]
      json.dump(secrets_as_jwk, f)

  def _save_new_secret(self, secret):
    secrets_dict = self._read_secrets()
    secrets_dict[secret.kid] = secret
    self._write_secrets(secrets_dict)

  async def add_key(self, secret: Secret):
    lock.acquire()
    try:
      self._save_new_secret(secret)
    finally:
      lock.release()

  async def get_kids(self) -> List[str]:
    lock.acquire()
    try:
      secrets_dict = self._read_secrets()
      res = list(secrets_dict.keys())
    finally:
      lock.release()
    return res

  async def get_key(self, kid: DID_URL) -> Optional[Secret]:
    lock.acquire()
    try:
      secrets_dict = self._read_secrets()
      res = secrets_dict.get(kid)
    finally:
      lock.release()
    return res

  async def get_keys(self, kids: List[DID_URL]) -> List[DID_URL]:
    lock.acquire()
    try:
      secrets_dict = self._read_secrets()
      res = [s.kid for s in secrets_dict.values() if s.kid in kids]
    finally:
      lock.release()
    return res
