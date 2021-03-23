import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# Activate Flask and Define Routes
app = Flask(__name__)

## Setup DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

## Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route('/')
def home():
    return (
        f"<h1>Surfs up! Precipitation and Station Analysis</h1>"
        f"____________________________________________________________________________<br/>"
        f"<h2>Available Routes<br/>"
        f"____________________________________________________________________________<br/>"
        f"<ul><li><a href='/api/v1.0/precipitation'>Precipitaion Data<br/></a></li></ul>"
        f"<ul><li><a href='/api/v1.0/stations'>Station Listing<br></a></li></ul>"
        f"<ul><li><a href='/api/v1.0/tobs'>12 months temperature observations (tobs) for most active station<br></a></li></ul>"
        f"<ul><li><a href='/api/v1.0/<start>'>Temperature Stats from start date<br/></a><li><ul>"
        f"<ul><li><a href='/api/v1.0/<start>/<end>'>Temperature Stats for a date range<br/></a><li><ul>"
    )

# Precipitation API route
@app.route('/api/v1.0/precipitation')
def precipitation():
     ## Query to return the date and precipitation
    session = Session(engine)
    prc_date_query = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    ## Convert query to dictionary
    prc_date_list = [{"Date":"Precipitation (inches)"}]

    for date, prcp in prc_date_query:
        prc_date_dict = {}
        prc_date_dict[date] = prcp
        prc_date_list.append(prc_date_dict)

    ## JSONIFY the dictionary
    return jsonify(prc_date_list)

    session.close()

## Station API Route
@app.route('/api/v1.0/stations')
def stations():

    ## Return the list of stations
    session = Session(engine)
    station_query = session.query(Station.station,Station.name).all()

    ## Convert to dictionary
    station_list = {"Station ID":"Station Name"}

    for station, name in station_query:
        station_list[station] = name

    ## JSONIFY!
    return jsonify (station_list)

    session.close()

## Tobs API Route
@app.route('/api/v1.0/tobs')
def tobs():

    ## Query to find the most recent date and the date for one year prior
    session = Session(engine)
    
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    prev_year_date = dt.datetime.strptime(most_recent_date[0],'%Y-%m-%d')-dt.timedelta(days=365)
    prev_year_date_formatted = prev_year_date.strftime('%Y-%m-%d')

    ## Query to get the 12 months of data
    temp_query = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= prev_year_date_formatted).\
                    order_by(Measurement.date).all()
    print(temp_query)
    ## Convert query to dictionary
    tobs_date_list = [{"Date":"Temperature (F)"}]

    for date, tobs in temp_query:
        tobs_date_dict = {}
        tobs_date_dict[date] = tobs
        tobs_date_list.append(tobs_date_dict)

    ## JSONIFY the dictionary
    return jsonify (tobs_date_list)

    session.close()

## Start Date Temp Data API Route
@app.route('/api/v1.0/<start>')
def top_start(start):

    ## Query to return the list of stations
    session = Session(engine)
    
    temp_start_query = session.query(Measurement.date,\
                                    func.min(Measurement.tobs),\
                                    func.max(Measurement.tobs),\
                                    func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()

    ## Convert query to dictionary
    temp_start_list = []
    
    for date, min, max, avg in temp_start_query:
        temp_start_dict = {}
        temp_start_dict["Date"] = date
        temp_start_dict["Min Temp"] = min
        temp_start_dict["Max Temp"] = max
        temp_start_dict["Avg Temp"] = avg
        temp_start_list.append(temp_start_dict)

    ## JSONIFY the dictionary
    return jsonify (temp_start_list)

    session.close()

## Station API Route
@app.route('/api/v1.0/<start>/<end>')
def temp_data_start(start,end):

    ## Query to return the list of stations
    session = Session(engine)
    
    temp_start_query = session.query(Measurement.date,\
                                    func.min(Measurement.tobs),\
                                    func.max(Measurement.tobs),\
                                    func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= start, Measurement.date <= end).\
                        group_by(Measurement.date).all()

    ## Convert query to dictionary
    temp_start_list = []
    
    for date, min, max, avg in temp_start_query:
        temp_start_dict = {}
        temp_start_dict["Date"] = date
        temp_start_dict["Min Temp"] = min
        temp_start_dict["Max Temp"] = max
        temp_start_dict["Avg Temp"] = avg
        temp_start_list.append(temp_start_dict)

    ## JSONIFY the dictionary
    return jsonify (temp_start_list)

    session.close()


if __name__ == '__main__':
    app.run(debug=True)