### Requirements
- Mininet-WiFi
- VLC

### Reproducibility Steps

```
sudo python allWirelessNetworksAroundUs.py
mininet-wifi> xterm sta1 h1
```

sta1 terminal:
```
cvlc -vvv v4l2:///dev/video0 --input-slave=alsa://hw:1,0 --mtu 1000 --sout'#transcode{vcodec=mp4v,vb=800,scale=1,acodec=mpga,ab=128,channels=1}: duplicate{dst=display,dst=rtp{sdp=rtsp://10.0.0.10:8080/helmet.sdp}'
```

h1 terminal:
```
cvlc rtsp://10.0.0.10:8080/helmet.sdp
```

Fontes, R. R., Rothenberg, C. E. Towards an Emulator for Software-Defined Wireless Networks. In: SwitchOn 2015, São Paulo – SP – Brazil.
