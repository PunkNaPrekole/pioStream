import cv2
import socket
import pickle
import threading


def receive_video(sock, packet_size, addr):
    data = b''
    while True:
        packet, _ = sock.recvfrom(packet_size)
        if packet == b'END':
            if data:
                frame = pickle.loads(data)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow('Pioneer stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    sock.sendto(b"stop_video", addr)
                    break
                data = b''
        else:
            data += packet

    cv2.destroyAllWindows()


def start_video_stream(udp_ip: str, udp_port: int = 5005, packet_size: int = 32768):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"start_video", (udp_ip, udp_port))

    video_thread = threading.Thread(target=receive_video, args=(sock, packet_size, (udp_ip, udp_port)))
    video_thread.start()
    video_thread.join()


if __name__ == "__main__":
    start_video_stream("10.1.100.43")