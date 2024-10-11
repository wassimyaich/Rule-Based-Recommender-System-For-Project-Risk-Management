import os
import flask
from owlready2 import *
from owlready2.sparql.endpoint import *
import werkzeug.serving

onto = get_ontology("C:/Users/maily/OneDrive/Bureau/ontology.owl").load() 
endpoint = EndPoint(default_world)
app = endpoint.wsgi_app

werkzeug.serving.run_simple("localhost", 5000, app)