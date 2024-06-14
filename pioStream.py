import cv2
import socket
import pickle
import threading


def video_streaming(sock, addr, cap, packet_size, stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = pickle.dumps(buffer)
        for i in range(0, len(data), packet_size):
            chunk = data[i:i + packet_size]
            sock.sendto(chunk, addr)
        sock.sendto(b'END', addr)


def start_video_stream(udp_ip: str = "0.0.0.0", udp_port: int = 5005, packet_size: int = 65507):
    cap = cv2.VideoCapture(0)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    stream_thread = None
    stop_event = threading.Event()

    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode()
        if command == "start_video":
            if stream_thread is None or not stream_thread.is_alive():
                stop_event.clear()
                stream_thread = threading.Thread(target=video_streaming, args=(sock, addr, cap, packet_size, stop_event))
                stream_thread.start()
        elif command == "stop_video":
            stop_event.set()
            if stream_thread is not None:
                stream_thread.join()
            cap.release()
            cap = cv2.VideoCapture(0)


if __name__ == "__main__":
    start_video_stream()
