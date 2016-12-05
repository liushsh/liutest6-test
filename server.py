import os
import json
import ibm_db
import logging
# from flask import Flask, jsonify

try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Parse VCAP_SERVICES Variable 
vcap_services = json.loads(os.environ['VCAP_SERVICES'])
service = vcap_services['dashDB'][0]
credentials = service["credentials"]
url = 'DATABASE=%s;uid=%s;pwd=%s;hostname=%s;port=%s;' % ( credentials["db"],credentials["username"],credentials["password"],credentials["host"],credentials["port"])

connection = ibm_db.connect(url, '', '')
statement = ibm_db.prepare(connection, 'SELECT DOGS, DASH111327 from SYSCAT.TABLES FETCH FIRST 10 ROWS ONLY')
ibm_db.execute(statement)
out = "<html><table border=\"1\"><tr><td>Table Name</td><td>Table Schema</td>" 
data = ibm_db.fetch_tuple(statement)
while (data):
    out = out + "<tr><td>"+data[0]+"</td><td>"+data[1]+"</td></tr>"
    data = ibm_db.fetch_tuple(statement)

ibm_db.free_stmt(statement)
ibm_db.close(connection)
out = out + "</table></html>"
return out


# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()

