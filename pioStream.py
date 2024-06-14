import cv2
import socket
import pickle
import resource


def start_video_stream(udp_ip: str = "0.0.0.0", udp_port: int = 5005, packet_size: int = 65507):
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
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
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    print("CPU time consumption:", usage_after.ru_utime - usage_before.ru_utime)
    print("Maximum memory consumption (in kilobytes):", usage_after.ru_maxrss)


if __name__ == "__main__":
    start_video_stream()
