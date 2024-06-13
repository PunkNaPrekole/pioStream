import cv2
import socket
import pickle


def start_video_stream(udp_ip: str, udp_port: int = 5005, packet_size: int = 65507):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"start_video", (udp_ip, udp_port))
    data = b''
    while True:
        packet, addr = sock.recvfrom(packet_size)
        if packet == b'END':
            frame = pickle.loads(data)
            cv2.imshow('Received', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = b''
        else:
            data += packet

    cv2.destroyAllWindows()
