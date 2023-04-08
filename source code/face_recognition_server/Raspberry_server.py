import cv2
import numpy as np
import socket
import struct

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓 바인드
server_socket.bind((server_ip, server_port))

# 연결 대기
server_socket.listen()

# 클라이언트 연결 수락
client_socket, addr = server_socket.accept()

# 이미지 수신 및 출력
while True:
    # 이미지 데이터 크기 수신
    data = b""
    payload_size = struct.calcsize(">I")
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    # 이미지 데이터 수신
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">I", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    # 이미지 데이터 배열 변환
    frame_data = data[:msg_size]
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = frame.reshape(-1, 150, 150, 3)

    # 이미지 출력
    cv2.imshow('Face Detection', frame[0])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 및 카메라 리소스 해제
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()