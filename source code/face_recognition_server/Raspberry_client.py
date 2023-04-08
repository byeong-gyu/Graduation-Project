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

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(0)

# 얼굴 검출 모델 불러오기
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 이미지 전처리 함수
def preprocess(frame):
    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 검출된 얼굴이 없으면 None 리턴
    if len(faces) == 0:
        return None

    # 검출된 얼굴 중 가장 큰 영역의 좌표 가져오기
    (x, y, w, h) = sorted(faces, reverse=True, key=lambda x: x[2] * x[3])[0]

    # 얼굴 부분 이미지 추출
    face_image = frame[y:y+h, x:x+w]

    # 이미지 리사이즈 및 정규화
    face_image = cv2.resize(face_image, (150, 150))
    face_image = face_image / 255.0

    # 이미지 배열 형태 변환
    face_image = face_image.reshape((1, 150, 150, 3))

    return face_image

# 이미지 전송 함수
def send_image(frame):
    # 이미지 데이터 크기 구하기
    frame_data = frame.tobytes()
    size = len(frame_data)

    # 이미지 데이터 크기 전송
    client_socket.sendall(struct.pack('>L', size))

    # 이미지 데이터 전송
    client_socket.sendall(frame_data)

while True:
    # 비디오 프레임 읽기
    ret, frame = cap.read()

    # 이미지 전처리
    face_image = preprocess(frame)

    # 얼굴이 검출된 경우 이미지 전송
    if face_image is not None:
        send_image(face_image)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 및 카메라 리소스 해제
client_socket.close()
cap.release()
cv2.destroyAllWindows()
