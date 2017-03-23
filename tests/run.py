"""
SAND conformance server.

This implements a conformance server for ISO/IEC 23009-5 SAND.
It validates the incoming SAND messages as well as the protocols used by
a SAND client.

Copyright (c) 2016-, ISO/IEC JTC1/SC29/WG11
All rights reserved.

See AUTHORS for a full list of authors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the ISO/IEC nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys

from time import sleep

from subprocess import Popen, STDOUT

import re

import unittest

import requests

import logging

logging.basicConfig(filename="report.log", level=logging.DEBUG, filemode="w")

PORT_LOCAL_SAND_SERVER = 5000

OK_LINE = "\\[RESULT\\]\\[OK\\]"
KO_LINE = "\\[RESULT\\]\\[KO\\]"

class TestMetrics(unittest.TestCase):
    """
    Tests of the /metrics endpoints.

    This collects tests for metrics sent by the client with HTTP POST.
    """
    def setUp(self):
        try:
            # We assume the test sever runs locally on the default port
            requests.get(("http://localhost:%i" % PORT_LOCAL_SAND_SERVER))
        except:
            logging.info("No test server detected. We will create one.")
            server_log = open("server.log", "w")
            Popen(
                ["../sand_server.py", "run",
                 "--port", str(PORT_LOCAL_SAND_SERVER)],
                stdout=server_log,
                stderr=STDOUT)
            # We wait a bit for the server to start
            sleep(2)

    def test_invalid_get_request(self):
        """
        Send GET requests
        """
        try:
            response = requests.get(
                ("http://localhost:%i/metrics" % PORT_LOCAL_SAND_SERVER))
            logging.info("Server response")
            logging.info("===============")
            logging.info(response.text)
            logging.info("===============")
            self.assertTrue(response.status_code == 400)
            self.assertTrue(re.search(KO_LINE, response.text))
        except Exception as exception:
            logging.error("[TEST][KO] GET")
            raise type(exception)(exception.message)

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    return_value = not unittest.TextTestRunner(verbosity=2).run(test_suite).wasSuccessful()
    sys.exit(return_value)
