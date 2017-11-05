from microbit import *
from struct import unpack

BME280_address = 0x76  # can be changed to 0x77 using the SDO pin

while True:
    try:
        i2c.read(BME280_address, 1)
    except OSError as error:
        raise SystemExit(error)
    else:
        i2c.write(BME280_address, bytearray([0XD0]))
        ID = i2c.read(BME280_address, 1)
        print("BM280 HUMIDITY, PRESSURE & TEMPERATURE SENSOR: [%s]" % hex(BME280_address))
        print("ID is: ", ord(ID))  # get ID of the sensor, should be 0x60

        # read temperature calibration data
        # 0x88 / 0x89 dig_T1 [7:0] / [15:8] unsigned short
        i2c.write(BME280_address, bytearray([0X88]))
        dig_T1 = unpack("<H", i2c.read(BME280_address, 2))
        print("T1:",dig_T1[0])
        
        # 0x8A / 0x8B dig_T2 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X8A]))
        dig_T2 = unpack("<h", i2c.read(BME280_address, 2))
        print("T2:", dig_T2[0])
        
        # 0x8C / 0x8D dig_T3 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X8C]))
        dig_T3 = unpack("<h", i2c.read(BME280_address, 2))
        print("T3:", dig_T3[0])

        # read pressure calibration data
        # 0x8E / 0x8F dig_P1 [7:0] / [15:8] unsigned short
        i2c.write(BME280_address, bytearray([0X8E]))
        dig_P1 = unpack("<H", i2c.read(BME280_address, 2))
        print("P1:", dig_P1[0])
        
        # 0x90 / 0x91 dig_P2 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X90]))
        dig_P2 = unpack("<h", i2c.read(BME280_address, 2))
        print("P2:", dig_P2[0])
        
        # 0x92 / 0x93 dig_P3 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X92]))
        dig_P3 = unpack("<h", i2c.read(BME280_address, 2))
        print("P3:", dig_P3[0])
        
        # 0x94 / 0x95 dig_P4 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X94]))
        dig_P4 = unpack("<h", i2c.read(BME280_address, 2))
        print("P4:", dig_P4[0])
        
        # 0x96 / 0x97 dig_P5 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X96]))
        dig_P5 = unpack("<h", i2c.read(BME280_address, 2))
        print("P5:", dig_P5[0])
        
        # 0x98 / 0x99 dig_P6 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X98]))
        dig_P6 = unpack("<h", i2c.read(BME280_address, 2))
        print("P6:", dig_P6[0])
        
        # 0x9A / 0x9B dig_P7 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X9A]))
        dig_P7 = unpack("<h", i2c.read(BME280_address, 2))
        print("P7:", dig_P7[0])
        
        # 0x9C / 0x9D dig_P8 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X9C]))
        dig_P8 = unpack("<h", i2c.read(BME280_address, 2))
        print("P8:", dig_P8[0])
        
        # 0x9E / 0x9F dig_P9 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0X9E]))
        dig_P9 = unpack("<h", i2c.read(BME280_address, 2))
        print("P9:", dig_P9[0])

        # read humidity calibration data
        # 0xA1 dig_H1 [7:0] unsigned char
        i2c.write(BME280_address, bytearray([0XA1]))
        dig_H1 = unpack("B", i2c.read(BME280_address, 1))
        print("H1:", dig_H1[0])
        
        # 0xE1 / 0xE2 dig_H2 [7:0] / [15:8] signed short
        i2c.write(BME280_address, bytearray([0XE1]))
        dig_H2 = unpack("<h", i2c.read(BME280_address, 2))
        print("H2:", dig_H2[0])
        
        # 0xE3 dig_H3 [7:0] unsigned char
        i2c.write(BME280_address, bytearray([0XE3]))
        dig_H3 = unpack("B", i2c.read(BME280_address, 1))
        print("H3:", dig_H3[0])
        
        # 0xE4 / 0xE5[3:0] dig_H4 [11:4] / [3:0] signed short
        i2c.write(BME280_address, bytearray([0XE4]))
        dig_H4 = unpack("b", i2c.read(BME280_address, 1)) # signed
        dig_H4 = (dig_H4[0] << 4)
        i2c.write(BME280_address, bytearray([0XE5]))
        dig_H4b = unpack("B", i2c.read(BME280_address, 1))
        dig_H4 = dig_H4 | (dig_H4b[0] & 0x0F)
        print("H4:", dig_H4)
              
        # 0xE5[7:4] / 0xE6 dig_H5 [3:0] / [11:4] signed short
        i2c.write(BME280_address, bytearray([0XE6]))
        dig_H5 = unpack("b", i2c.read(BME280_address, 1))
        dig_H5 = (dig_H5[0] << 4)
        i2c.write(BME280_address, bytearray([0XE5]))
        dig_H5b = unpack("B", i2c.read(BME280_address, 1))
        dig_H5 = dig_H5 | (dig_H5b[0] >> 4 & 0x0F)
        print("H5:", dig_H5)
        
        # 0xE7 dig_H6 signed char
        i2c.write(BME280_address, bytearray([0XE7]))
        dig_H6 = unpack("b", i2c.read(BME280_address, 1))
        print("H6:", dig_H6[0])

        print("finished reading calibration data")
        input("Press Enter to read registers again...")