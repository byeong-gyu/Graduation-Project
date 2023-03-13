import cv2
import numpy as np
import socket

# 서버 정보
server_ip = '서버 IP 주소'
server_port = 서버 포트 번호

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 연결 시도
client_socket.connect((server_ip, server_port))

# 카메라 캡쳐 객체 생성
cap = cv2.VideoCapture(0)

# 얼굴 검출 모델 불러오기
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 얼굴 검출을 위한 그레이스케일 이미지로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출 수행
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 검출된 얼굴 영역 전송
    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w] # 얼굴 부분만 이미지 추출
        # 이미지를 일정 크기로 조절하여 송신할 수 있도록 변환
        resized_face_img = cv2.resize(face_img, (150, 150), interpolation=cv2.INTER_AREA)
        # 이미지 데이터를 바이트 스트림으로 변환하여 송신
        client_socket.send(resized_face_img.tobytes())

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 닫기
client_socket.close()

# 카메라 리소스 해제
cap.release()