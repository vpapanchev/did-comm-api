""" Module containing all custom Exceptions of this service. """


class DIDCommAPIError(Exception):
  """ Base exception class for all DID Comm API errors """
  pass


class MyDIDCommError(DIDCommAPIError):
  """ Base exception class for errors when using the DID Comm Implementation """
  pass
