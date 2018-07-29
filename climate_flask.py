from flask import Flask
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
app = Flask(__name__)

db_path = "sqlite:///Resources/hawaii.sqlite"

@app.route('/')
def home_route():
    return "This is the homepage"

@app.route('/api/v1.0/precipitation')
def get_temp():
    (session, Measurement, Station) = init_ORM(db_path)
    date_string = session.query(func.max(Measurement.date)).one()[0]
    most_recent_date = datetime.strptime(date_string,"%Y-%m-%d")
    one_year_earlier = most_recent_date - relativedelta(years=1)
    q1 = session.query(Measurement.date, func.avg(Measurement.tobs))\
        .filter(Measurement.date > one_year_earlier)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)
    d = dict(q1.all())
    return jsonify(d)

@app.route('/api/v1.0/stations')
def get_stations():
    (session, Measurement, Station) = init_ORM(db_path)
    q2 = session.query(Station.station)
    return jsonify(q2.all())

@app.route('/api/v1.0/tobs')
def get_tobs():
    (session, Measurement, Station) = init_ORM(db_path)
    q3 = session.query(Measurement.tobs)
    return jsonify(q3.all())

@app.route('/api/v1.0/<start_date>')
def get_since(start_date):
    (session, Measurement, Station) = init_ORM(db_path)
    q4 = session.query(func.min(Measurement.tobs),
                        func.avg(Measurement.tobs),
                        func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)
    return jsonify(q4.all())

@app.route('/api/v1.0/<start_date>/<end_date>')
def get_range(start_date, end_date):
    (session, Measurement, Station) = init_ORM(db_path)
    q5 = session.query(func.min(Measurement.tobs),
                        func.avg(Measurement.tobs),
                        func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)
    return jsonify(q5.all())

def init_ORM(db_path):
    engine = create_engine(db_path)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    return (session, Measurement, Station)

if (__name__ == "__main__"): 
    app.run(port = 5545, debug=True)
