'''
Created on Mar 10, 2013
@author: cgrubb
'''
import json
import sys
sys.path.append("..")
from tornado import web, ioloop

from parsers import address_parser as ap

class Listener(web.RequestHandler):
    
    def get(self, address):
        #address = self.get_argument("address",default = "")
        result = ap.streetAddress.parseString(address)
        output = {}
        street = {  "number": result.street.number.strip(),
                    "prefix_direction": result.street.prefix_direction,
                    "name": result.street.name,
                    "type": result.street.type,
                    "suffix_direction": result.street.suffix_direction
                }
        crossStreet = {}
        if result.crossStreet:
            crossStreet = {
                           "number": result.crossStreet.number.strip(),
                           "prefix_direction": result.crossStreet.prefix_direction,
                            "name": result.crossStreet.name,
                            "type": result.crossStreet.type,
                            "suffix_direction": result.crossStreet.suffix_direction
                           }
        output = {"street":
                    street,
                  "crossstreet":
                    crossStreet                                
                  }  
        
        enc = json.JSONEncoder()     
        self.set_header("Content-Type", "application/json")
        json_output = enc.encode(output)
        self.set_header("Content-Length", len(json_output))
        self.write(json_output)
        
if __name__ == "__main__":
    application = web.Application([(r"/(.*)", Listener),])
    application.listen(9999)
    ioloop.IOLoop.instance().start()
    