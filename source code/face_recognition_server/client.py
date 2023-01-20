#아래 4줄은 한글 깨지는거 땜에 해둔것.
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#소켓통신을 위한 라이브러리
import socket
import pickle


# 소켓 객체 생성(패밀리 : ipv4, 타입 : tcp)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 호스트와 포트 지정
host = socket.gethostname()
port = 12345

# 서버에 연결 요청
s.connect((host, port))

# 바이너리로 파일 열기(학습용 or 탐색용 사진을 서버로 전송하기 위한 코드)
with open("a.jpg", "rb") as imageFile:
    img_data = imageFile.read()

# 클라이언트로 부터 입력받은 실종자의 정보 리스트
my_list = ["식별값(관리자:0, 사용자:1)","이름", "성별", "나이", "실종장소", "실종날짜"]

# 리스트를 서버로 송신하기 위해 직렬화 시킨다.
list_data = pickle.dumps(my_list)

# 이미지를 서버로 전송하기 위해 이미지의 크기값(문자열타입)을 바이트타입으로 변형하여 전송  
s.sendall(str(len(img_data)).encode())

# 이미지를 서버로 전송
s.sendall(img_data)

# 실종자 정보 리스트를 서버로 송신 
s.sendall(list_data)

#바이너리 타입의 변수 선언(서버에서 수신되는 값은 바이너리값이기 때문)
#서버에서 1)학습완료 메시지, 2)일치하는값 못찾음 메시지, 3)일치하는값 찾음 메시지 수신
byte_data = b''
while True:
    data = s.recv(4096) #서버로부터 4096 바이트 만큼 데이터 수신
    byte_data += data
    if len(data) < 4096:
        break

#예외처리(서버로부터 수신한 리스트를 역직렬화 시키는 코드)
try:
    # 역직렬화
    info_list = pickle.loads(byte_data)
except pickle.UnpicklingError:
    print("서버로부터 전송된 데이터가 없습니다.")

#1) 'none': db에 없음, 'ok': 학습완료, 그 외: 동일인물 정보 출력
if info_list[0] == 'none':
    print("일치하는 사람이 없습니다.")   
elif info_list[0] == 'ok':
    print("학습이 완료 되었습니다!")
else :
    # 데이터 역직렬화 
    print("사람을 찾았습니다!")
    print(info_list)

s.close()
