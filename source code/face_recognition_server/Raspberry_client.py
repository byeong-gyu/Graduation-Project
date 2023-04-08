import cv2
import numpy as np
import socket
import struct

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_ip, server_port))

# 카메라 연결
cap = cv2.VideoCapture(0)

# 이미지 송신
while True:
    # 이미지 캡처 및 배열 변환
    ret, frame = cap.read()
    frame = cv2.resize(frame, (150, 150))
    frame_data = frame.tobytes()

    # 이미지 데이터 크기 전송
    data_size = struct.pack(">I", len(frame_data))
    client_socket.sendall(data_size)

    # 이미지 데이터 전송
    client_socket.sendall(frame_data)

    # ESC 키 입력 시 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 소켓 및 카메라 리소스 해제
client_socket.close()
cap.release()
cv2.destroyAllWindows()
