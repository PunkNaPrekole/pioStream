import cv2
import socket
import pickle


def start_video_stream(udp_ip: str = "0.0.0.0", udp_port: int = 5005, packet_size: int = 65507):
    cap = cv2.VideoCapture(0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "start_video":
            break

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = pickle.dumps(buffer)
        for i in range(0, len(data), packet_size):
            chunk = data[i:i + packet_size]
            sock.sendto(chunk, addr)
        sock.sendto(b'END', addr)

    cap.release()
    sock.close()


if __name__ == "__main__":
    start_video_stream()
