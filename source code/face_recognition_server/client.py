import socket
import pickle
import threading
import struct

def handle_receive(client_socket):
    while True:
        try:
            response = client_socket.recv(1024).decode("utf-8")
            if response == "실종자 등록이 완료되었습니다.":
                print("실종자 등록이 완료되었습니다.")
            elif response == "실종자 발견":
                missing_person_info = pickle.loads(client_socket.recv(1024))
                print('\n실종자를 발견 했습니다!')
                print(missing_person_info)
                print("\n실종자 이름을 입력하세요: ")
            else:
                print("실종자 등록에 실패했습니다.")
        except ConnectionError:
            print('서버와의 연결이 끊어졌습니다.')
            break

def handle_send(client_socket):
    while True:
        try:
            print('실종자를 등록합니다.\n')
            # 실종자 정보를 입력받습니다.
            missing_person_info_list = []
            missing_person_info_list.append(input("실종자 이름을 입력하세요: "))
            missing_person_info_list.append(input("성별을 입력하세요: "))
            missing_person_info_list.append(input("나이를 입력하세요: "))
            missing_person_info_list.append(input("지역을 입력하세요: "))
            missing_person_info_list.append(input("실종 날짜를 입력하세요: "))
            missing_person_info_list.append(input("전화번호를 입력하세요: "))

            # 실종자 사진을 입력받습니다.
            with open("arin2.jpg", "rb") as f:
                image_data = f.read()

            # 요청을 서버로 전송합니다.
            request_type = "실종자 등록"
            client_socket.sendall((request_type + "\n").encode("utf-8"))
        
            # 이미지 크기 전송
            image_size_bytes = struct.pack("!I", len(image_data))
            client_socket.sendall(image_size_bytes)

            # 이미지를 서버로 전송
            client_socket.sendall(image_data)

            # 실종자 정보 전송 
            client_socket.sendall(pickle.dumps(missing_person_info_list))

        except ConnectionError:
            print('서버와의 연결이 끊어졌습니다.')
            break

        if input('계속하시겠습니까?(y/n): ') == "n":
            client_socket.close()
            break
        


# 서버의 IP 주소와 포트 번호
server_ip = "192.168.123.111"
server_port = 12345
# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=handle_receive, args=(client_socket,)).start()
threading.Thread(target=handle_send, args=(client_socket,)).start()

