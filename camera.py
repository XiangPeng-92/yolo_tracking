import cv2

cap = cv2.VideoCapture(
    "rtsp://admin:admin@192.168.1.108/:554/cam/realmonitor?channel=1&subtype=1"
)

while True:
    ret, frame = cap.read()
    cv2.imshow("Capturing", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # click q to stop capturing
        break
cap.release()
cv2.destroyAllWindows()
