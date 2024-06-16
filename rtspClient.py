import cv2


def pio_stream_receive(ip_address):
    rtsp_url = f'rtsp://{ip_address}:8554/pioneer_stream'
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("The video stream could not be opened")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to get a frame")
            break
        cv2.imshow('pioneer stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    pio_stream_receive("192.168.0.102")
