import socket

# 서버 정보
server_ip = '127.0.0.1'
server_port = 5000

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 바인딩
server_socket.bind((server_ip, server_port))

# 클라이언트 연결 대기
server_socket.listen()

# 클라이언트 연결 수락
client_socket, addr = server_socket.accept()

while True:
    # 송신된 이미지 데이터 수신
    data = b''
    while True:
        packet = client_socket.recv(1024)
        if not packet:
            break
        data += packet

    # 수신된 데이터를 이미지로 변환
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    # 수신된 이미지 출력
    cv2.imshow('received image', img)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 소켓 닫기
client_socket.close()
server_socket.close()