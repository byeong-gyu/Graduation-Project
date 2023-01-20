#아래는 한글 인코딩을 위한 코드
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#사진 읽어오고 탐색,표현,비교까지 한번에 가능
import face_recognition
import sqlite3
import socket
import pickle

#서버 소켓 생성(패밀리: ipv4, 타입:tcp)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 특정 주소 및 포트에 바인딩
host = socket.gethostname()
port = 12345
s.bind((host, port))

# 들어오는 연결 듣기
s.listen(5)

while True:
    # 클라이언트 연결 대기
    conn_s,addr = s.accept()
    print("Hello client! : ", addr)
    # 이미지 크기 받기
    img_size = int(conn_s.recv(1024).decode())
    # 이미지 데이터 수신
    img_data = conn_s.recv(img_size)
    # 새 파일을 열고 받은 이미지 데이터 쓰기
    with open("received_image.jpg", "wb") as imageFile:
        imageFile.write(img_data)
    # 리스트 수신
    list_data = b''
    while True:
        data = conn_s.recv(4096)
        list_data += data
        if len(data) < 4096:
            break
    #예외처리
    try:
        # 클라이언트로부터 받은 실종자 정보 역직렬화
        info_list = pickle.loads(list_data)
    except pickle.UnpicklingError:
        print("클라이언트로부터 데이터를 수신하지 못했습니다.")

    #클라이언트로부터 받은 이미지 읽어오기
    known_image = face_recognition.load_image_file("received_image1.jpg")
    #이미지 인코딩(랜드마크), 리스트타입으로 각 원소는 얼굴의 특징점의 좌표값이다.
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    #info_list[0]에는 클라이언트가 관리자인지 사용자인지 구분하는 값이다.(0이면 관리자이다.)
    #관리자는 클라이언트로부터 수신한 이미지를 학습시킨 값과 실종자 정보를 db에 저장한다.
    if info_list[0] == '0':
        #db를 열고 변동사항은 자동 커밋된다.
        conn=sqlite3.connect("info.db",isolation_level=None)
        #커서 획득
        c=conn.cursor()
        #실종자 얼굴을 인코딩한 리스트의 각 원소를 문자열로 변환하여 문자열 리스트로 재생성
        str_list=[]
        for i, element in enumerate(known_face_encoding):
            string=str(element)
            str_list.append(string)

        #문자열 리스트를 하나의 문자열타입으로 합쳐준다. 각 원소는 공백을 사이로 두고 조인
        encoding_string=" ".join(str_list)

        #db에 있는 사용자 정보 테이블의 식별자 값중 제일 마지막 값을 읽어와 +1 해준다.
        #새로운 값을 넣기 위해서다.
        c.execute("SELECT pk FROM information ORDER BY pk DESC")
        num=c.fetchone()
        last_pk=num[0]
        add_pk=last_pk+1

        #실종자 정보 테이블에 클라이언트로부터 수신한 실종자정보와, 인코딩한 이미지 문자열을 추가한다.
        c.execute("INSERT INTO information(pk, encoding, name, sex, age, area, date) VALUES(?, ?, ?, ?, ?, ?, ?)",(add_pk, encoding_string, info_list[1], info_list[2], info_list[3], info_list[4], info_list[5]))

        #테이블에 실종자 정보를 저장했을 때 클라이언트로 확인 메시지를 전송한다.
        msg=['ok']
        conn_s.sendall(pickle.dumps(msg))

        c.close()
        conn.close()
        conn_s.close()

    #info_list[0]의 값이 1(사용자) 일때,
    #실종자로 의심되는 사람을 db에 저장된 인코딩값과 비교하기 위한 코드
    else:
        conn=sqlite3.connect("info.db",isolation_level=None)
        c=conn.cursor() 

        c.execute("SELECT encoding FROM information")
        
        while True:
            #테이블의 값을 읽어오면 튜플형식으로 반환해준다.
            tuple_value=c.fetchone()
            #db에 저장된 인코딩값을 전부 읽었을 때 db는 None을 반환한다.
            #그렇기 때문에 클라이언트로 일치하는 사람이 없다는 신호를 전송한다.
            if tuple_value == None:
                none_list=['none']
                conn_s.sendall(pickle.dumps(none_list))
                c.close()
                conn.close()
                conn_s.close()
                break
            #db로부터 받은 값은 튜플이기 때문에 인덱스가 tuple_value[0]인 곳에 문자열로 저장된 얼굴 인코딩 값이 있다.
            enco_value=tuple_value[0]
            
            #문자열을 문자열 리스트로 변환(split() 메서드의 인자값을 안주면 공백을 기준으로 원소를 쪼개준다.)
            enco_list=enco_value.split()
            
            #문자열 리스트를 실수형 리스트로 변환
            deco_face_value=[]
            for i, value in enumerate(enco_list):
                value_b=float(value)
                deco_face_value.append(value_b)

            #클라이언트로부터 수신한 사진을 학습한 데이터와 db에 저장되있던 인코딩 값을 비교한다.(face_distances 안에는 0~1의 값이 들어간다.)
            face_distances = face_recognition.face_distance([deco_face_value], known_face_encoding)

            #임계치는 0.35로 팀장(강병규)이 임의로 지정한것.
            #만약 face_distances의 값이 0.35미만이면 동일인물로 판단한다.
            if face_distances < 0.35:
                #db에 저장된 일치하는 인물의 정보를 읽어와 클라이언트로 전송.
                matched_person = c.execute("SELECT name,sex,age,area,date FROM information WHERE encoding=?", (enco_value,)).fetchone()
                matched_list=list(matched_person)
                #리스트를 직렬화하여 클라이언트로 전송
                conn_s.sendall(pickle.dumps(matched_list))
                c.close()
                conn.close()
                conn_s.close()
                break
        
    break
