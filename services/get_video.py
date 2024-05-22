from services import bp
from utils.kafka import consumer

@bp.route("/get-video/", methods=['GET'])
def id_error():
    return "ID was not provided !!"

@bp.route("/get-video/<id>", methods=['GET'])
def get_video(id):
    return "Video ID: " + id