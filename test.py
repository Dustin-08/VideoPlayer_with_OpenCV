import cv2

# 동영상 파일 열기
cap = cv2.VideoCapture('movie.mp4')

# 초기 변수 설정
playing = True
speed = 1.0
frame_pos = 0
max_speed = 8.0
min_speed = 0.125

while cap.isOpened():
    if playing:
        ret, frame = cap.read()
        if not ret:
            break
        frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    else:
        # 일시정지 상태에서 프레임 유지
        frame = frame

    # 화면 정보 표시
    text = f"current speed: x{speed} frame_cnt: {frame_pos}"
    cv2.putText(frame, text, (frame.shape[1]-590, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow('Video Player', frame)

    key = cv2.waitKey(int(30 / speed)) & 0xFF

    # 키 입력 처리
    if key == 27:  # ESC
        break
    elif key == ord(' '):  # Spacebar
        playing = not playing
    elif key == ord('0'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    elif key == 81:  # ←
        pos = max(0, cap.get(cv2.CAP_PROP_POS_FRAMES) - 5)
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    elif key == 83:  # →
        pos = min(cap.get(cv2.CAP_PROP_FRAME_COUNT)-1, cap.get(cv2.CAP_PROP_POS_FRAMES) + 5)
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
    elif key == 82:  # ↑
        speed = min(max_speed, speed * 2)
    elif key == 84:  # ↓
        speed = max(min_speed, speed / 2)
    elif key == ord('s'):
        cv2.imwrite(f"frame_{frame_pos}.png", frame)

cap.release()
cv2.destroyAllWindows()