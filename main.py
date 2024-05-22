from flask import Flask, session, render_template, redirect, url_for
from dotenv import load_dotenv
import os
from utils.db import db
from utils.kafka import consumer
import threading
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

from services import bp as main_bp
app.register_blueprint(main_bp)

def main():
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    debug = os.getenv('DEBUG')
    mydb = init_db()
    consumer_thread = threading.Thread(target=consumer.consume_video, args=(mydb, ))
    consumer_thread.start()
    app.run(host=host, port=port, debug=debug)

def init_db():
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_db = os.getenv('MYSQL_DB')
    mysql_port = os.getenv('MYSQL_PORT')

    mydb = db.DatabaseConnector(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db)
    mydb.set_table_name('videos')
    return mydb

if __name__ == '__main__':
    main()