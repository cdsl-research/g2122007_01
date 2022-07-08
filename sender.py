import network
from esp import espnow
import utime

execfile("ntptime.py")

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # Or network.AP_IF
w0.active(True)
#w0.disconnect()   # For ESP8266
#utime.sleep(600)

for i in range(1):
  utime.sleep(10)
  e = espnow.ESPNow()
  e.init()
  print("init")
  peer = b'\xb8\xf0\t\xc5\xc2\xb8' # MAC address of peer's wifi interface

  e.add_peer(peer)
  print("add_peer: ", peer)

  e.send("Starting...")       # Send to all peers
  print("Starting...")
  for i in range(300):
    f = open("network.txt", "a")
    e.send(peer, str(i), True)
    f.write(str(utime.localtime()))
    f.write(",")
    f.write(str(e.stats()))
    f.write("\n")
    utime.sleep(0.1)
    f.close()
  e.send(b'end')
  print("0"*20)
  print("end")
  e.deinit()
  
  #utime.sleep(180)
