# SAND conformance server

[![Build Status](https://travis-ci.org/edrthomas/SAND-HTTP-Conformance-Server.svg?branch=master)](https://travis-ci.org/edrthomas/SAND-HTTP-Conformance-Server)

This implements a conformance server for ISO/IEC 23009-5 Server And Network
asssited DASH (SAND).

It validates the incoming SAND messages as well as the protocols used by
a SAND client.

## Requirements

- [pip](https://pip.pypa.io/en/stable/)

## Installation

```pip install -r requirements.txt```

## Usage

```python sand_server.py run --port tcp_port```

By default, the server listens on port 5000.

## Help

```python sand_server.py run --help```

```
Usage: sand_server.py run [OPTIONS]

  Run the SAND server and listen to port 'port'.

Options:
  --port INTEGER  Listening port of the SAND conformance server.
  --help          Show this message and exit.
```

## Endpoints

### /headers

This endpoint validates that a DASH client sends a SAND message via the HTTP header as specified by ISO/IEC 23009-5 SAND.

### /metrics

This endpoint validates that a DASH client sends a metric message via the HTTP POST method as specified by ISO/IEC 23009-5 SAND.
