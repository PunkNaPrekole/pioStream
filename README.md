1) Перенесите rtspServer.py и pio-rtsp-server.service через ftp с помощью scp \
  scp path/to/rtcpServer.py pi@<drone_ip>:/home/pi/ \
  scp path/to/pio-rtsp-server.service pi@<drone_ip>:/home/pi/
3) Перенесите pioStream.service в директорию /etc/systemd/system \
   sudo mv /path/to/pioStream.service /etc/systemd/system/pio-rtsp-server.service
4) Сделайте скрипт rtspServer.py исполняемым \
   chmod +x /home/pi/rtspServer.py
5) Перезагрузите systemd для применения изменений \
  sudo systemctl daemon-reload
6) Включите сервис для автозапуска при загрузке системы \
   sudo systemctl enable pio-rtsp-server.service
7) Перезаргрузите дрон \
  sudo reboot
