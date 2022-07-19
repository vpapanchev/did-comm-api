### Parent project

This project was developed as a Microservice in the design of the [Interoperable SSI Access Control System](https://git.scc.kit.edu/uwmbv/ssi-acs).

# DID Communication API

## Description

DID Communication API (**DID-Comm-API**) is a python project built using the Flask framework. It provides an HTTP API on which SSI Clients can send DIDComm Messages.

Functionality of DID-Comm-API:
- Generate and resolve [Peer-DIDs](https://identity.foundation/peer-did-method-spec/);
- DIDComm Messages: Send and receive encrypted and authenticated messages using the [DIDComm Messaging Protocol](https://identity.foundation/didcomm-messaging/spec/);
- Notification of received messages: Notify other services configured as webhooks whenever a new HTTP Request with a DIDComm Message is received;
- Respond to requests: Receive instructions from other services and respond to the received HTTP requests accordingly.

## How to run locally

1. Copy the configuration file:\
`cp ./did_communication_api/config/config.example.yml ./did_communication_api/config/config.yml`
2. Open the configuration file and set the server host, port and the Webhook API.
3. Create and activate a new virtual environment:\
`python3 -m venv ./venv`\
`source venv/bin/activate`
4. Install the project requirements\
`pip3 install -r requirements_dev.txt`
5. Run \
`python3 -m did_communication_api`

## How to run using Docker

1. Copy the configuration file:\
`cp ./did_communication_api/config/config.example.yml ./did_communication_api/config/config.yml`
2. Open the configuration file and set the server host, port and the Webhook API.
3. Run \
`docker build -f docker/DockerFile --tag didcommv2-image .`\
`docker run -p <port>:<port> --env API_PORT=<port> --name=didcommv2 didcommv2-image:latest`
4. To see the logs of the container:\
`docker logs didcommv2`
5. To stop the container:\
`docker stop didcommv2`

## Usage

To use the DID_Comm_API an SSI Client application with the following functionalties:
- Peer-DIDs: Create and Resolve Peer-DIDs
- DIDComm Messaging: Pack and Unpack authenticated+encrypted DIDComm Messages
- HTTP Requests: Pack the created DIDComm Messages in HTTP Requests as described below

is required. \
For a reference implementation see [SSI Simple Client](https://git.scc.kit.edu/uwmbv/ssi_simple_client)

### Packing DIDComm Messages in HTTP Requests and Responses:

Currently, the DID_Comm_API packs DIDComm Messages in the message bodies of HTTP Requests and Responses:
```json
{
  "didcomm_msg": "<encrypted and authenticated DIDComm Messsage>"
}
```

## Support

In case of questions about the project use the following contacts:\
Email: vasilpapanchev@gmail.com

## Project status

The project was created as a prototype used for evaluating purposes and will not be actively supported in the future.
