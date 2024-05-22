
from services import bp
from flask import Flask, session, render_template, redirect, url_for, request
import uuid
import threading
from utils.compressing import compressing
from main import init_db
from utils.db import db
from utils.kafka import producer
import json

@bp.route("/upload-video/", methods=['POST', 'GET', 'OPTIONS'])
def upload_video():
    mydb = init_db()
    if request.method == "POST":
        my_data = {}
        try:
            my_data = json.loads(request.data)
            if "video_link" not in my_data:
                return "video_link is missing"
        except Exception as ex:
            return "something wrong happened while extracting video_link" , ex 
        video_link = my_data["video_link"]
        input_path = "./utils/compressing/input.mp4"
        output_path = "./utils/compressing/op" + video_link + ".mp4"
        random_uuid = mydb.insert_data(input_path)
        compress_thread = threading.Thread(target=producer.produce_video, args=(random_uuid, input_path, "Processing", output_path))
        compress_thread.start()
        return redirect("/status/" + random_uuid, 302)
        # return "Your video uuid is: " + str(random_uuid)
    return render_template("services/update_video.html")

@bp.route('/status/<video_uuid>', methods=['GET'])
def thread_status(video_uuid):
    mydb = init_db()
    data = mydb.get_by_uuid(video_uuid)
    if len(data) == 0:
        msg = "Couldn't retrieve Data"
        status=None
    if len(data) > 1:
        msg = "Multiple data retrieved"
        status=None
    if len(data[0]) < 5:
        msg = "Data scheme is corrupted"
        status=None
    if data[0][4] == "Done":
        msg = str(video_uuid)
        status='Done'
    else:
        msg = str(video_uuid)
        status='Running ...'
    return render_template("services/video_status.html", msg=msg, status=status)
