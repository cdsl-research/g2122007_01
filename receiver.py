import network
from esp import espnow
import ili9342c
import utime

execfile("ntptime.py")

color565 = ili9342c.color565
from machine import Pin, SPI
spi = SPI(miso=Pin(19), mosi=Pin(23, Pin.OUT), sck=Pin(18, Pin.OUT))
display = ili9342c.ILI934X(spi, cs=Pin(14), dc=Pin(27), rst=Pin(33), bl=Pin(32))
display.fill(color565(0x00, 0x00, 0x00))

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)
w0.active(True)
#w0.disconnect()   # For ESP8266
#utime.sleep(600)

for i in range(1):
  display.fill(color565(0x00, 0x00, 0x00))
  row = 0
  try:
    e = espnow.ESPNow()
    e.init()
    display.text('init', 0, row)
    row += 8
    print("init")
  
    peer = b'\xfc\xf5\xc4=;,'   # MAC address of peer's wifi interface
    e.add_peer(peer)
    display.text(str(peer), 0, row)
    row += 8
    print("add_peer: ", peer)
  except:
    print("init_error")

  try:
    while True:
      f = open("network.txt", "a")
      print("Receiving...")
      host, msg = e.irecv()     # Available on ESP32 and ESP8266
      if msg:             # msg == None if timeout in irecv()
        print(host, msg)
        display.text(str(msg), 0, row)
        if row < 240:
          row += 8
        else:
          row = 0
        display.text(str(e.stats()), 0, row)
        f.write(str(utime.localtime()))
        f.write(",")
        f.write(str(e.stats()))
        f.write(",")
        f.write(str(e.peers))
        f.write("\n")
        if row < 240:
          row += 8
        else:
          row = 0
        if msg == b'end':
          print("end")
          break
      f.close()
  except:
    print("receive_error")
  e.deinit()
  print("deinit")
  #utime.sleep(180)

