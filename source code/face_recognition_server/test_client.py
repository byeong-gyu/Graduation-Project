import socket
import pickle

# 서버의 IP 주소와 포트 번호
server_ip = "127.0.0.1"
server_port = 12345

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:

  # 사용자에게 실종자 등록 여부를 묻습니다.
  request = input("실종자 등록(1), 실종자 찾기(2): ")

  # 실종자 등록을 선택한 경우
  if request == "1":
    # 실종자 정보를 입력받습니다.
    missing_person_info_list = []
    missing_person_info_list.append(input("실종자 이름을 입력하세요: "))
    missing_person_info_list.append(input("성별을 입력하세요: "))
    missing_person_info_list.append(input("나이를 입력하세요: "))
    missing_person_info_list.append(input("지역을 입력하세요: "))
    missing_person_info_list.append(input("실종 날짜를 입력하세요: "))
    missing_person_info_list.append(input("전화번호를 입력하세요: "))

    # 실종자 사진을 입력받습니다.
    with open("admin2.jpg", "rb") as f:
      image_data = f.read()

    # 실종자 정보를 서버로 전송합니다.
    request_type = "실종자 등록"
    client_socket.sendall((request_type + "\n").encode("utf-8"))
      
    # 이미지 크기 전송
    client_socket.sendall(str(len(image_data)).encode())

    # 이미지를 서버로 전송
    client_socket.sendall(image_data)

    # 실종자 정보 전송 
    client_socket.sendall(pickle.dumps(missing_person_info_list))

    # 서버의 응답 수신
    response = client_socket.recv(1024).decode("utf-8")

    if response == "실종자 등록이 완료되었습니다.":
      print("실종자 등록이 완료되었습니다.")
    else:
      print("실종자 등록에 실패했습니다.")

  else:
    while True:
      # 서버의 응답 수신
      response = client_socket.recv(1024).decode("utf-8")
      if response == "실종자 발견":
        missing_person_info = pickle.loads(client_socket.recv(1024))
        print(missing_person_info)
      else:
        print("잘못된 출력입니다. 시스템을 정비하세요.")
        break

      a = input('계속 대기하시겠습니까?(y/n): ')
      if a == "n":
        client_socket.close()
        break
      




# 서버 연결 종료
client_socket.close()