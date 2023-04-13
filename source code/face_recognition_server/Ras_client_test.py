import cv2
import numpy as np
import socket
import struct

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 연결
client_socket.connect((server_ip, server_port))

# 얼굴 검출 모델 로드
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 카메라 캡처 객체 생성
cap = cv2.VideoCapture(0)

while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()

    # 프레임 크기 변경
    frame = cv2.resize(frame, (640, 480))

    # 얼굴 검출
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 얼굴 영역 추출 후 이미지 변환
    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        img_encode = cv2.imencode('.jpg', face_roi)[1]
        img_data = np.array(img_encode)
        string_data = img_data.tostring()

        # 이미지 데이터 크기 전송
        size = len(string_data)
        client_socket.send(struct.pack('>L', size))

        # 이미지 데이터 전송
        client_socket.send(string_data)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 및 카메라 리소스 해제
client_socket.close()
cap.release()
cv2.destroyAllWindows()
