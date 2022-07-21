### Parent project

This project was developed as a Microservice in the design of an [Interoperable SSI-based Access Control System](https://github.com/vpapanchev/ssi-acs).

# DID Communication API

## Description

DID Communication API (**DID-Comm-API**) is a Python project built using the Flask framework. \
It provides an HTTP endpoint on which SSI-Clients can send HTTP Requests containing DIDComm Messages.

Functionality of DID-Comm-API:
- Generate and resolve static [Peer-DIDs](https://identity.foundation/peer-did-method-spec/);
- DIDComm Messages: Send and receive encrypted and authenticated messages using the [DIDComm Messaging Protocol](https://identity.foundation/didcomm-messaging/spec/);
- Notification of received messages: Notify other services configured as webhooks whenever a new HTTP Request with a DIDComm Message is received;
- Respond to requests: Receive instructions from other services and respond to the received HTTP requests accordingly.

## How to run locally

1. Open the configuration file (/did_communication_api/config/config.yml) and set the server host, port and the Webhook API.
2. Create and activate a new virtual environment:\
`python3 -m venv ./venv`\
`source venv/bin/activate`
3. Install the project requirements\
`pip3 install -r requirements_dev.txt`
4. Run \
`python3 -m did_communication_api`

## How to run using Docker

1. Open the configuration file (/did_communication_api/config/config.yml) and set the server host, port and the Webhook API.
2. Run \
`docker build -f docker/DockerFile --tag didcommv2-image .`\
`docker run -p <port>:<port> --env API_PORT=<port> --name=didcommv2 didcommv2-image:latest`
3. To see the logs of the container:\
`docker logs didcommv2`
4. To stop the container:\
`docker stop didcommv2`

## Usage

To use the DID_Comm_API an SSI-Client application with the following functionalties:
- Peer-DIDs: Create and Resolve Peer-DIDs
- DIDComm Messaging: Pack and Unpack authenticated+encrypted DIDComm Messages
- HTTP Requests: Pack the created DIDComm Messages in HTTP Requests as described below

is required. For a reference implementation see the example [SSI Client](https://github.com/vpapanchev/ssi-acs-client) implementation.

The SSI-Client should send HTTP Requests on the `/did_comm/inbox/` API

Furthermore, a service to be configured as a *Message-received Webhook* is also required. This service is notified whenever DID-Comm-API receives a new request and instructs DID-Comm-API on how to respond to the sender of the request. The formats of the notification and its response are given below. An example implementation of this functionality is contained in the [SSI Access Decision Point](https://github.com/vpapanchev/ssi-adp).

### Packing DIDComm Messages in HTTP Requests and Responses:

Currently, the DID_Comm_API packs DIDComm Messages in the message bodies of HTTP Requests and Responses:
```json
{
  "didcomm_msg": "<encrypted and authenticated DIDComm Messsage>"
}
```

### Message-Received Webhook API Formats

DID-Comm-API notifies the received webhook by sending an HTTP POST Request with the body: 
```json
{
  "sender": "<sender_peer_did>",
  "request": {
    "type": "DIDComm",
    "http_request_method": "<http_request_method>",
    "message": {
      "id": "<Message ID>",
      "type": "<Message Type>",
      "body": "<Message Body>",
      "attachments": ["<List of DIDComm attachments>"]
    }
  }
}
```

The Webhook responds with instructions on how DID-Comm-API should respond. The instructions are sent as an HTTP Response with the following body:
```json
{
  "response": {
    "http_code": "<response_http_code>",
    "type": "DIDComm",
    "message": {
      "id": "<Response DIDComm Message ID>",
      "type": "<Response DIDComm Message Type>",
      "body": "<Response DIDComm Message Body>"
    }
  }
}
```


### General Workflow

0. Configuration:
    - Set Host and Port-number of DID-Comm-API
    - Set Webhook API for notification whenever a new request is received
1. Starting DID-Comm-API
    - DID-Comm-API generates and outputs a fresh Peer-DID
2. SSI-Client sends a new request, by:
    - generating a Peer-DID (or using an existing Peer-DID)
    - creating a DIDComm Message using his Peer-DID and the one of DID-Comm-API
    - packing the DIDComm Message into an HTTP Request
    - sending the HTTP Request on the `/did_comm/inbox/` API of DID-Comm-API
3. DID-Comm-API receives the request:
    - unpack, encrypt and authenticate the DIDComm Message
    - notify the configured webhook
    - receive instructions from the webhook
    - send an HTTP Response back to SSI-Client containing a DIDComm Message
    (the type and content of the DIDComm Message and the HTTP Response status code is defined by the Webhook`s instructions)



## Support

In case of questions about the project use the following contacts:\
Email: vasilpapanchev@gmail.com

## Project status

The project was created as a prototype used for evaluating purposes of the [SSI-based Access Control System](https://github.com/vpapanchev/ssi-acs).
