# SAND conformance server

[![build status](https://gitlab.com/MPEG_SAND/SAND_server/badges/master/build.svg)](https://gitlab.com/MPEG_SAND/SAND_server/commits/master)

This implements a conformance server for ISO/IEC 23009-5 Server And Network
asssited DASH (SAND).

It validates the incoming SAND messages as well as the protocols used by
a SAND client.

## Requirements

- [pip](https://pip.pypa.io/en/stable/)

## Installation

```pip install -r requirements.txt```

## Usage

```python sand_server.py```
