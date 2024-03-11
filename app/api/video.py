import logging

import cv2
from flask import (Blueprint, Response)

from app.camera.camera import generate_frames
from app.models import base

logger = logging.getLogger(__name__)

api = Blueprint('video', __name__, url_prefix='/api/video')
db = base.db



@api.route('/camera')
def video_feed():
  return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
