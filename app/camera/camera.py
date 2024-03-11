"""
    使用python实现：读取USB摄像头的画面
"""
# 导入CV2模块
import cv2

cap = cv2.VideoCapture(1)

def generate_frames():
  while True:
    success, frame = cap.read()
    if not success:
      break
    else:
      ret, buffer = cv2.imencode('.jpg', frame)
      frame = buffer.tobytes()
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

