""" Utility functions for DIDComm and  Peer DIDs """


def get_service_endpoint_of_did_document(did_doc):
  if 'service' not in did_doc or not did_doc['service']:
    return None
  service = did_doc['service'][0]
  if 'serviceEndpoint' not in service:
    return None
  return service['serviceEndpoint']


def validate_peer_did_doc(did_doc):
  """ Validates the DID Document of a Peer DID """
  service_endpoint = get_service_endpoint_of_did_document(did_doc)
  return service_endpoint is not None
