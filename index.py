"""
- 영상정보처리 Term Project
- 학번: 20234194
- 학부전공: IT융합학부 IT융합전공
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
        - 현재 재생 속도 (예) x1, x2 x1/2 등
        - 현재 동영상 프레임 번호 (예) #27
"""
import cv2

# 동영상 파일 자동 열기(동일 경로에 영상 두기)
movie = cv2.VideoCapture('movie.mp4')

# 초기 변수 설정
playing = True
speed = 1.0
frame_cnt = 0
max_speed = 8.0
min_speed = 0.125 # 1/8
white = (255, 255, 255)
title = "20234194_VideoPlayer_with_OpenCV"

if movie.isOpened() == False:
    print("동영상 파일이 없거나 형식이 맞지 않습니다.(The video file is missing or in the incorrect format.)")

while movie.isOpened():
    if playing:
        # 영상에서 프레임 읽기
        ret, frame = movie.read()
        if not ret: # ret = false면, 프레임이 제대로 읽히지 않았다는 것
            break
        frame_cnt = int(movie.get(cv2.CAP_PROP_POS_FRAMES)) # 캡처되는 프레임 번호를 frame_cnt에 입력
    else:
        # 일시정지 상태에서 프레임 유지
        frame_cnt = frame_cnt

    # 화면 정보(배속, 프레임수) 우상단에 표시
    text = f"current speed: x{speed} frame_cnt: {frame_cnt}"
    cv2.putText(frame, text, (frame.shape[1]-700, 50), cv2.FONT_HERSHEY_COMPLEX, 1, white, 2)
    cv2.namedWindow(title) # 윈도우 이름
    cv2.imshow(title, frame) # title 정보 표시

    #key = cv2.waitKeyEx(100) # 100ms 동안 키 이벤트 대기 <- 이거 하면 딜레이 증가해버림
    key = cv2.waitKey(int(30/speed)) & 0xFF # 100ms 동안 키 이벤트 대기

    # 키 입력 처리
    if key == 27: # esc 키 누르면 종료
        break
    elif key == ord(' '): # spacebar 키 입력시
        playing = not playing
    elif key == ord('0'): # 숫자 ‘0’을 클릭
        movie.set(cv2.CAP_PROP_POS_FRAMES, 0) # 프레임 수를 0으로 초기화
    elif key == 81: # 방향키 ‘좌’ 클릭
        frame_change = max(0, movie.get(cv2.CAP_PROP_POS_FRAMES) - 5) # 현재 가지고 온 프레임에서 -5
        movie.set(cv2.CAP_PROP_POS_FRAMES, frame_change)
    elif key == 83: # 방향키 ‘우’ 클릭
        frame_change = min(movie.get(cv2.CAP_PROP_FRAME_COUNT)-1, movie.get(cv2.CAP_PROP_POS_FRAMES) + 5) # 현재 가지고 온 프레임에서 +5
        movie.set(cv2.CAP_PROP_POS_FRAMES, frame_change)
    elif key == 82: # 방향키 ‘위’ 클릭
        print()
    elif key == 84: # 방향키 ‘아래’ 클릭
        print()
    elif key == ord('s'): # 문자키 ‘s’ 클릭
        cv2.imwrite(f"frame_{frame_cnt}.png", frame)

# 비디오 캡쳐 메모리 해제
movie.release()
# 창닫기
cv2.destroyAllWindows()