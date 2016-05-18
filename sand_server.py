#!/usr/bin/python

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

from flask import Flask, request
from werkzeug.routing import Rule
from lxml import etree

app = Flask(__name__)
app.debug = False
app.url_map.add(Rule('/metrics', endpoint='metrics'))

@app.endpoint('metrics')
def metrics():
  success = True
  
  expected_request_method = "POST"
  expected_content_type = "application/sand+xml"

  # Test 1 - HTTP method test
  if request.method == expected_request_method:
    print "[TEST] HTTP method OK (" + expected_request_method + ")"
    success &= True
  else:
    print "[TEST] HTTP method NOK (" + request.method + " != " + expected_request_method + ")"
    success = False
  
  # Test 2 - Content-Type of SAND messages
  if request.headers['Content-Type'] == expected_content_type:
    print "[TEST] Content-Type OK (" + expected_content_type + ")"
    success &= True
  else:
    print "[TEST] Content-Type NOK (" + request.headers['Content-Type'] + " != " + expected_content_type + ")"
    success = False

  # Test 3 - Message validation
  try:
    
    with open("./schemas/sand_messages.xsd") as f: 
      sand_schema_doc = etree.parse(f)
      sand_schema = etree.XMLSchema(sand_schema_doc)

      try:
        sand_message = etree.fromstring(request.data)
        sand_schema.assertValid(sand_message)
        print "[TEST] SAND message validation OK."
        success &= True
      except etree.DocumentInvalid as e:
        print "[TEST] SAND message validation NOK."
        print e
        success = False
      except:
        print "[ERROR] XML SAND message parsing."
        success = False
  
  except etree.XMLSchemaParseError as e:
    print "[ERROR] XML schema parsing."
    print e
    success = False
  except:
    print "[ERROR] XML schema parsing."
    success = False
  

  if success:
    print "[RESULT] Success"
    return "Test succeeded !"
  else:
    print "[RESULT] Failure"
    return "Test failed !"

if __name__ == "__main__":
  print "========= SAND conformance server ============="
  print "-----------------------------------------------"
  app.run()
