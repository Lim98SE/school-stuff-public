import cv2

cap = cv2.VideoCapture("input.mp4")

index = 0

frame_div = 3

while (cap.isOpened()):
    ret, frame = cap.read()

    index += 1

    if (index % frame_div != 0):
        continue

    if ret == True:
        name = f"frames/{index // frame_div}.png"
        frame = cv2.resize(frame, (40, 20))
        frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite(name, frame)

        print(f"Frame {index // frame_div} saved")
    
    else:
        break

cap.release()
print("Done!!! :3 :3 :3")