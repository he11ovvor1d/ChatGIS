import psycopg2
import geojson
from psycopg2.extras import RealDictCursor
from geojson import loads,Feature, FeatureCollection, Point, LineString, Polygon
# from flask import Flask, request, jsonify
import cgi

form = cgi.FieldStorage()

param1 = form.getvalue("param1")

conn = psycopg2.connect(database="NJ", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()
cur.execute("SELECT ST_AsGeoJSON(geom) FROM 行政区 WHERE name = '鼓楼区'")
features = []
for row in cur.fetchall():
        feature = geojson.loads(row[0])
        features.append(feature)

feature_collection = FeatureCollection(features)

with open("./output.geojson", "w") as f:
        geojson.dump(feature_collection, f)

cur.close()
conn.close()

