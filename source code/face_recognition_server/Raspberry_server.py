import cv2
import numpy as np
import socket
import struct

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# 클라이언트 연결 대기
server_socket.listen(1)
client_socket, addr = server_socket.accept()

# 이미지 수신 함수
def recv_image():
    # 이미지 데이터 크기 수신
    size_data = b''
    while len(size_data) < 4:
        size_data += client_socket.recv(4 - len(size_data))
    size = struct.unpack('>L', size_data)[0]

    # 이미지 데이터 수신
    frame_data = b''
    while len(frame_data) < size:
        frame_data += client_socket.recv(size - len(frame_data))

    # 수신한 데이터 배열 형태 변환
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = np.reshape(frame, (150, 150, 3))

    return frame

while True:
    # 이미지 수신
    frame = recv_image()

    # 이미지 출력
    cv2.imshow('Received Image', frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 리소스 해제
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
