from datetime import datetime, timedelta

from flask import Flask, g, render_template
from sqlalchemy import create_engine

from config import Config

app = Flask(__name__)
app.config.from_object('config.Config')

engine = create_engine('postgres://codephil:codephil!@lavazares-db1.cnodp99ehkll.us-west-2.rds.amazonaws.com:5432/lavazaresdb')

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except RuntimeError as error:
    g.conn = None
    print(error)
    raise

@app.route("/")
def index():
  cursor = g.conn.execute("SELECT Count(*) as new_users_count from users where createdat > current_date - interval '7 days'").fetchone()
  new_users_count = cursor['new_users_count']

  cursor = g.conn.execute("SELECT Count(*) as total_users_count from users").fetchone()
  total_users_count = cursor['total_users_count']

  return render_template('index.html', 
    new_users_count=new_users_count, 
    today=datetime.today() - timedelta(days=7), 
    total_users_count=total_users_count)


if __name__ == '__main__':
  app.run()