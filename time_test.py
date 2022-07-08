import ds3231_pb
from ds3231_port import DS3231
from machine import Pin, I2C

p21 = Pin(21,Pin.IN,Pin.PULL_UP)
p22 = Pin(22,Pin.IN,Pin.PULL_UP)
i2c = I2C(scl=Pin(22), sda=Pin(21))
ds3231 = DS3231(i2c)

f = open("time.txt", "a")
for i in range(100):
  f.write(str(ds3231.rtc_test()))
  f.write("\n")
f.close()

