from services import bp

@bp.route("/get-videos", methods=['GET'])
def get_videos():
    return "Videos List"