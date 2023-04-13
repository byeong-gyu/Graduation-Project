import cv2
import numpy as np
import socket
import struct

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 바인딩
server_socket.bind((server_ip, server_port))

# 서버 리스닝
server_socket.listen()

# 클라이언트 연결 수락
print('Waiting for client...')
client_socket, addr = server_socket.accept()
print('Client connected:', addr)

while True:
    # 이미지 데이터 수신
    size_data = b''
    while len(size_data) < 4:
        data = client_socket.recv(4 - len(size_data))
        if not data:
            break
        size_data += data
    if not data:
        break
    size = struct.unpack('>L', size_data)[0]

    img_data = b''
    while len(img_data) < size:
        data = client_socket.recv(size - len(img_data))
        if not data:
            break
        img_data += data
    if not data:
        break

    # 이미지 배열로 변환
    img = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # 이미지 출력
    cv2.imshow('Received Image', img)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 및 카메라 리소스 해제
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
