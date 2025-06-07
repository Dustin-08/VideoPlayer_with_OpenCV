"""
- 영상정보처리 Term Project
- 학번: 20234194
- 학부전공: IT융합학부 IT융합전공
- 개발 환경: MAC OS 16인치, Window OS 15.6인치
- 과제 설명
    1. OpenCV 라이브러리 활용(강의 시간에 배운 것들만)한 동영상 플레이어 구현
    2. 본인이 촬영한 1920×1080 해상도의 동영상 파일로 입력 동영상 설정
    3. 프로그램 실행시 동영상 플레이 화면 나오기 + 자동 재생 시작
    4. 동영상 플레이어 기능 구현되어야 하는 항목
        - 동영상은 본인이 촬영한 임의의 동영상을 로딩 (source과 같은 폴더에 위치)
        - ‘Spacebar’ 클릭 → 재생/일시정지 (토글 형태로 동작)
        - 숫자 ‘0’을 클릭 → 영상 첫번째 프레임으로 이동 후 재생
        - 방향키 ‘좌’ 클릭 → 5프레임 이전으로 이동 후 재생
        - 방향키 ‘우’ 클릭 → 5프레임 이후로 이동 후 재생
        - 방향키 ‘위’ 클릭 → 재생속도 2배 (최대 8배)
            - (예) 방향키 ‘위’ 한번 누르면 기존 재생 속도 대비 2배
        - 방향키 ‘아래’ 클릭 → 재생속도 1/2배 (최대 1/8배)
            - (예) 방향키 ‘아래’ 한번 누르면 기존 재생 속도 대비 1/2배
        - 문자키 ‘s’ 클릭 → 현재 프레임 이미지 저장 (프레임 번호로 저장)
        - ‘ESC’ 클릭 → 프로그램 종료
    5. 동영상 화면에 표시되어야 하는 항목
        - 현재 재생 속도 (예) x1, x2, x1/2 등
        - 현재 동영상 프레임 번호 (예) #27
"""
# OpenCV 라이브러리 import
import cv2
from fractions import Fraction # 재생 속도를 소수점이 아닌 분수 형태로 나타내기 위해 Fraction 라이브러리 import

# 동영상 파일 자동 열기(동일 경로에 영상 두기)
movie = cv2.VideoCapture('movie.mp4')

# 초기 변수 설정
playing = True # 재생중 여부
speed = 1.0 # 배속 기본 속도
frame_cnt = 0 # 프레임수 초기화
max_speed = 8.0 # 최대 배속
min_speed = 0.125 # 최저 배속
white = (255, 255, 255) # 텍스트 색상
title = "20234194_VideoPlayer_with_OpenCV_UOU_25-1_TermProject"

# 영상 열림 여부 확인 후 예외처리: if 영상이 안 열렸다면
if movie.isOpened() == False:
    print("경고: 동영상 파일이 없거나 형식이 맞지 않습니다.(Warning: The video file is missing or in the incorrect format.)")

# 영상이 열렸다면 열려있는동안 동작하는 부분
while movie.isOpened():
    # 영상이 재생 중인지 일시정지 상태인지 판별 후 프레임 번호 가져오기
    if playing: 
        # 영상에서 프레임 읽기
        ret, frame = movie.read()
        if not ret: # ret = false면, 프레임이 제대로 읽히지 않았다는 것
            break
        frame_cnt = int(movie.get(cv2.CAP_PROP_POS_FRAMES)) # 캡처되는 프레임 번호를 frame_cnt에 입력
    else:
        # 일시정지 상태에서는 프레임 번호 유지
        frame_cnt = frame_cnt

    # 화면 정보(배속, 프레임수) 우상단에 표시
    # 참고: https://aiday.tistory.com/78 <- 4. Converting a float to fraction 참고해서 작성
    fraction = Fraction.from_float(speed) # 계산 용이를 위해 소수점으로 우선 계산 후, 화면에 표시할때만 분수로 변환해서 이를 화면에 표시
    text = f"current speed: x{fraction} frame_cnt: #{frame_cnt}"
    cv2.putText(frame, text, (1200, 50), cv2.FONT_HERSHEY_COMPLEX, 1, white, 2)
    cv2.namedWindow(title) # 윈도우 이름
    cv2.imshow(title, frame) # title 정보 표시

    #key = cv2.waitKeyEx(100) # 100ms 동안 키 이벤트 대기 <- 이거 사용하면 영상 딜레이 증가하는 이슈 존재합니다.
    FPS = movie.get(cv2.CAP_PROP_FPS) # 보통 FPS는 30이지만, 30이 아닌 영상을 위해
    # waitKeyEx가 아닌 waitKey만 사용하게 되면 화살표키(방향키)를 인식하지 못하는 이슈 존재합니다.
    key = cv2.waitKeyEx(int(1000 / FPS / speed)) # fps에 맞춰서 딜레이 주기
    #print("Key값은: ", key) # 키 입력 테스트를 위함

    # 키 입력 처리
    if key == 27: # esc 키 누르면 종료
        break
    elif key == ord(' '): # spacebar 키 입력시
        playing = not playing
    elif key == ord('0'): # 숫자 ‘0’을 클릭
        movie.set(cv2.CAP_PROP_POS_FRAMES, 0) # 프레임 수를 0으로 초기화
    elif key == 2424832: # Windows OS 기준 - 방향키 ‘좌’ 클릭
    #elif key == 63234: # MAC OS 기준 -  방향키 ‘좌’ 클릭
        frame_change = max(0, movie.get(cv2.CAP_PROP_POS_FRAMES) - 5) # 현재 가지고 온 프레임에서 -5, 후에 max(a, b)로 두 값중 더 큰 값 선택(프레임 번호가 음수 되는 것을 방지)
        movie.set(cv2.CAP_PROP_POS_FRAMES, frame_change) # max(a, b) 선택한 프레임 값으로 영상 프레임 설정
    elif key == 2555904: # Windows OS 기준 - 방향키 ‘우’ 클릭
    #elif key == 63235: # MAC OS 기준 -  방향키 ‘우’ 클릭
        frame_change = min(movie.get(cv2.CAP_PROP_FRAME_COUNT)-1, movie.get(cv2.CAP_PROP_POS_FRAMES) + 5) # 프레임 번호가 0부터 시작하기에 전체 프레임 개수에서 1 빼기, 후에 현재 가지고 온 프레임에서 +5, min(a, b)로 두 값중 더 작은 값 선택
        movie.set(cv2.CAP_PROP_POS_FRAMES, frame_change) # min(a, b) 선택한 프레임 값으로 영상 프레임 설정
    elif key == 2490368: # Windows OS 기준 - 방향키 ‘좌’ 클릭
    #elif key == 63232: # MAC OS 기준 -  방향키 ‘상’ 클릭
        speed = min(max_speed, speed * 2) # speed x2배를 한 후에, min(a, b)로 두 값중 더 작은 값 선택(초기에 설정한 최대 배속값만큼까지만 배속이 오르게 제한을 두기 위해)
    elif key == 2621440: # Windows OS 기준 - 방향키 ‘좌’ 클릭
    #elif key == 63233: # MAC OS 기준 -  방향키 ‘하’ 클릭
        speed = max(min_speed, speed / 2) # speed를 x1/2배를 한 후에, max(a, b)로 두 값중 더 큰 값 선택(초기에 설정한 최저 배속값만큼까지만 배속이 내려가게 제한을 두기 위해)
    elif key == ord('s'): # 문자키 ‘s’ 클릭
        cv2.imwrite(f"frame_#{frame_cnt}.png", frame) # 파일명을 프레임 번호로 저장

# 비디오 캡쳐 메모리 해제
movie.release()
# 창닫기
cv2.destroyAllWindows()