import face_recognition
import sqlite3
import socket
import pickle
import threading
import numpy as numpy

lock = threading.Lock()

# 비교 모듈의 결과를 클라이언트에게 전송해주는 모듈
def broadcast_message(sender_socket, info_list):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            try:
                client_socket.send("실종자 발견".encode("utf-8"))
                # 리스트를 직렬화하여 클라이언트로 전송
                client_socket.sendall(pickle.dumps(info_list))
            except ConnectionError:
                print('클라이언트와의 연결이 끊어졌습니다.')


#실종자 등록 모듈
def register_missing_person(client_socket,img_data):
  
  with open("registration_image.jpg", "wb") as f:
        f.write(img_data)

  # 실종자 정보를 pickle 형식으로 받습니다.
  try:
    missing_person_info = pickle.loads(client_socket.recv(1024))
  except Exception as e:
    print("실종자 정보 읽기 오류:", e)
    client_socket.send("실종자 정보 읽기 오류가 발생했습니다.".encode("utf-8"))
    client_socket.close()
    return

  #클라이언트로부터 받은 이미지 읽어오기
  known_image = face_recognition.load_image_file("registration_image.jpg")
  # 실종자의 사진에서 얼굴 부분을 추출하고 얼굴 특징값을 반환 받는다.
  face_features = face_recognition.face_encodings(known_image)[0]

  # 얼굴 특징값을 문자열로 변환합니다.
  encoding_string = " ".join([str(x) for x in face_features])

  # 얼굴 특징값, 실종자 정보를 데이터베이스에 저장합니다.
  with sqlite3.connect("info.db") as conn:
    c = conn.cursor()
    c.execute("INSERT INTO information(encoding, name, sex, age, area, date, phone) VALUES(?, ?, ?, ?, ?, ?, ?)", (encoding_string, missing_person_info[0], missing_person_info[1], missing_person_info[2], missing_person_info[3], missing_person_info[4], missing_person_info[5]))

    conn.commit()

  # 클라이언트에 실종자 등록 완료 메시지를 송신합니다.
  client_socket.send("실종자 등록이 완료되었습니다.".encode("utf-8"))



#실종자 비교 모듈
def find_missing_person(client_socket,img_data):
  #실종자 비교 대상 사진 저장
  with open("comparison_image.jpg", "wb") as f:
    f.write(img_data)

  #클라이언트로부터 수신한 이미지 불러오기
  known_image = face_recognition.load_image_file("comparison_image.jpg")

  # 실종자의 사진에서 얼굴 부분을 추출하고 얼굴 특징값을 반환 받는다.
  face_features = face_recognition.face_encodings(known_image)[0]


  # 실종자 정보를 데이터베이스에서 조회한다.
  with sqlite3.connect("info.db") as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM information")

    while True:
      # 테이블의 값을 읽어오면 튜플형식으로 반환해준다.
      tuple_value = c.fetchone()
      # db에 저장된 인코딩값을 전부 읽었을 때 db는 None을 반환한다.
      # 그렇기 때문에 클라이언트로 일치하는 사람이 없다는 신호를 전송한다.
      if tuple_value == None:
        client_socket.send("None".encode("utf-8"))
        c.close()
        conn.close()
        client_socket.close()
        break
      # db로부터 받은 값은 튜플이기 때문에 인덱스가 tuple_value[1]인 곳에 문자열로 저장된 얼굴 인코딩 값이 있다.
      enco_value = tuple_value[1]


      # 문자열을 문자열 리스트로 변환(split() 메서드의 인자값을 안주면 공백을 기준으로 원소를 쪼개준다.)
      enco_list = enco_value.split()

      # 문자열 리스트를 실수형 리스트로 변환
      
      with lock:
        deco_face_value = []
        for i in range(len(enco_list)):
          try:
            value_b = float(enco_list[i])
            deco_face_value.append(value_b)
          except ValueError:
            continue

      # 클라이언트로부터 수신한 사진을 학습한 데이터와 db에 저장되있던 인코딩 값을 비교한다.(face_distances 안에는 0~1의 값이 들어간다.)
      face_distances = face_recognition.face_distance([deco_face_value], face_features)

      # 임계치는 0.35로 팀장(강병규)이 임의로 지정한것.
      # 만약 face_distances의 값이 0.35미만이면 동일인물로 판단한다.
      if face_distances < 0.35:
        # db에 저장된 일치하는 인물의 정보를 읽어와 클라이언트로 전송.
        matched_person = c.execute("SELECT name, sex, age, area, date, phone FROM information WHERE encoding=?", (enco_value,)).fetchone()
        matched_list = list(matched_person)

        #실종자 발견 메시지 전송
        broadcast_message(client_socket, matched_list)
        break
      

def main():

  # 서버 소켓 생성(패밀리: ipv4, 타입:tcp)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # 소켓을 특정 주소 및 포트에 바인딩
  host = "127.0.0.1"
  port = 12345
  s.bind((host, port))

  print('클라이언트 연결 대기중...')
  # 들어오는 연결 듣기
  s.listen(5)
  
  while True:
    # 클라이언트 연결 대기
    conn_s,addr = s.accept()
    print("Hello client! : ", addr)

    # 클라이언트의 요청을 처리합니다.
    request = conn_s.recv(1024).decode("utf-8")

    if request.strip() == "실종자 등록":
      # 실종자 등록 코드
      # 이미지 크기 받기
      image_size = int(conn_s.recv(1024).decode())
      # 이미지 데이터 수신
      img_data = conn_s.recv(image_size)

      threading.Thread(target=register_missing_person, args=(conn_s,img_data)).start()

      # # 스레드 시작
      # if conn_s not in client_sockets:  # 중복 확인
      #     threading.Thread(target=register_missing_person, args=(conn_s,img_data)).start()
      #     client_sockets.append(conn_s)
      # else:
      #     threading.Thread(target=register_missing_person, args=(conn_s,img_data)).start()

    elif request.strip() == "실종자 찾기":
      # 이미지 크기 받기
      image_size = int(conn_s.recv(1024).decode())
      # 이미지 데이터 수신
      img_data = conn_s.recv(image_size)
      
      # 스레드 시작
      # 실종자 찾기 코드
      if conn_s not in client_sockets:  # 중복 확인
          threading.Thread(target=find_missing_person, args=(conn_s,img_data)).start()
          client_sockets.append(conn_s)
      else:
          threading.Thread(target=find_missing_person, args=(conn_s,img_data)).start()
    
    else:
      client_sockets.append(conn_s)

  # 서버 소켓 닫기
  s.close()
client_sockets = []

if __name__ == "__main__":
  main()