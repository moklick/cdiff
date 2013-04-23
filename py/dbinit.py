#!/usr/bin/env python

import pymongo

con = pymongo.Connection('mongodb1.alwaysdata.com',27017)
# create db called speakers
db = con.moklick_color_deltas
db.authenticate('moklick_mongo', 'MoDb123!')
# create collection called measurement
measurements = db.measurements
# remove all
#measurements.remove({})

for i in range(0,25):
	m = measurements.insert({'num' : i, 'direction' : {'a' : [], 'b': [], 'c' : [], 'd' : []}})
	print measurements.find_one(m)
