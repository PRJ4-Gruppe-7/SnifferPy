cd C:\Users\viksk\Documents\Elektronik\4. semester\PRJ4

pscp -r PySniffer pi@raspberrypi.local:temp/Python


sudo pgrep -f python3 | sudo xargs kill -9
