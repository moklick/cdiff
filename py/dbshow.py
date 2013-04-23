#!/usr/bin/env python

import pymongo

con = pymongo.Connection('mongodb1.alwaysdata.com',27017)
# create db called speakers
db = con.moklick_color_deltas
db.authenticate('moklick_mongo', 'MoDb123!')
# create collection called measurement
measurements = db.measurements

for i in range(0,25):
	m = measurements.find_one({'num' : i})
	print m
