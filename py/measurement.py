#!/usr/bin/eval PYTHONPATH=/home/moklick/modules python

import pymongo
import json
import cgi
import logging

valid_directions = ['a','b','c','d']

class Measurement():
    
    def __init__(self):
	logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='/home/moklick/cdiff/py/cdiff.log',level=logging.INFO)

        # start connection
        con = pymongo.Connection('mongodb1.alwaysdata.com',27017)

        # create db called speakers
        db = con.moklick_color_deltas
        db.authenticate('moklick_mongo', 'MoDb123!')

        # create collection calles sites
        self.measurements = db.measurements

    def save(self,color_id, direction, value):
        res = {}
        color = self.measurements.find_one({'num' : color_id})
        
        if color is not None and direction in valid_directions:
            self.measurements.update({'num' : color_id}, { '$push' : {'direction.' + direction : value}})
            msg = 'Saved colorID: ' + str(color_id) + ' successfully.'
            res = {'message' : msg , 'objectID' : str(color['_id'])}             

	else:
	    res = {'message' : 'An error occured! Can not find colorID: ' + str(colorID)}  	

        return res

    def get_deltas(self, color_num):
        color = self.measurements.find_one({'num' : color_num})

        if color is not None:
            return color['direction']

    def get_all_deltas(self):
        deltas = {}

        for m in self.measurements.find().sort('num'):
            deltas[m['num']] = {'direction' : m['direction']}

        return deltas
    
def main():
    result = {}
    form = cgi.FieldStorage()
    
    color = form.getvalue("colorID")
    dirc = form.getvalue("direction")
    val = form.getvalue("value")
    action = form.getvalue("action") 
		
    measurement = Measurement()
    if action == 'save':
    	result = measurement.save(int(color),dirc,int(val))

    if action == 'getall':
	result = measurement.get_all_deltas()
    
    print 'Content-Type: application/json'
    print 
    print json.dumps(result)


if __name__ == "__main__":
    main() 
