from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('main', __name__)
CORS(bp, origins=["*"])


from services import get_videos
from services import get_video
from services import upload_video