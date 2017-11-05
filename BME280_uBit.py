from microbit import i2c, sleep

# calibration parameters stored in the sensor (adjust to your sensor's values!)
dig_T1 = 28212
dig_T2 = 26305
dig_T3 = 50

dig_P1 = 38411
dig_P2 = -10738
dig_P3 = 3024
dig_P4 = 8977
dig_P5 = -128
dig_P6 = -7
dig_P7 = 12300
dig_P8 = -12000
dig_P9 = 5000

dig_H1 = 0
dig_H2 = 368
dig_H3 = 0
dig_H4 = 303
dig_H5 = 50
dig_H6 = 30

# sensor memory map registers
REG_ID = 0xD0
SENSOR_ID = 0x60
REG_CTRL_HUM = 0XF2
REG_CTRL_MEAS = 0XF4
REG_DATA = 0XF7
REG_CONFIG = 0xF5


class BME280_Sensor(object):
    def __init__(self, HEX_ADDRESS):
        self._address = HEX_ADDRESS
        try:
            i2c.read(self._address, 1)
        except OSError as error:
            raise SystemExit(error)
        else:
            i2c.write(self._address, bytearray([REG_ID]))
            ID = i2c.read(self._address, 1)
            if ord(ID) == SENSOR_ID:
                print("found BME280 sensor: [%s]" % hex(self._address))
                print("sensor device ID is: [%s]" % hex(ord(ID)))
            else:
                print("another device at address [%s]!" % hex(self._address))
                raise SystemExit()

    def sensor_forced_mode_1x(self):
        i2c.write(self._address, bytearray([REG_CTRL_HUM, 0x01]))
        i2c.write(self._address, bytearray([REG_CTRL_MEAS, 0x25]))
        sleep(1000)
        return

    def read_data_register(self):
        i2c.write(self._address, bytearray([REG_DATA]))
        return i2c.read(self._address, 8)

    def temperature_raw(self, data_bytes):
        """returns raw (uncompensated) temperature value from the sensor"""
        adc_T = ((data_bytes[3] << 16) | (
                 data_bytes[4] << 8) | data_bytes[5]) >> 4
        return adc_T

    def pressure_raw(self, data_bytes):
        """returns raw (uncompensated) pressure value from the sensor"""
        adc_P = ((data_bytes[0] << 16) | (
                 data_bytes[1] << 8) | data_bytes[2]) >> 4
        return adc_P

    def humidity_raw(self, data_bytes):
        """returns raw (uncompensated) humidity value from the sensor"""
        adc_H = (data_bytes[6] << 8) | data_bytes[7]
        return adc_H

    def temp_fine(self, raw_T):
        """calculates fine resolution temperature value"""
        UT = float(raw_T)
        var1 = (UT / 16384.0 - float(dig_T1) / 1024.0) * float(dig_T2)
        var2 = ((UT / 131072.0 - float(dig_T1) / 8192.0) * (
                 UT / 131072.0 - float(dig_T1) / 8192.0)) * float(dig_T3)
        return int(var1 + var2)

    def temperature_corrected(self, t_fine):
        """returns the compensated temperature in degrees celsius"""
        T = float(t_fine) / 5120.0
        return T

    def pressure_corrected(self, raw_P, t_fine, altitude=179.0):
        """calculates the compensated pressure in hPa
        and the pressure at sealevel at a given altitude in m"""
        var1 = float(t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(dig_P6) / 32768.0
        var2 = var2 + var1 * float(dig_P5) * 2.0
        var2 = (var2 / 4.0) + (float(dig_P4) * 65536.0)
        var1 = (float(dig_P3) * var1 * var1 / 524288.0
                + float(dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(dig_P1)
        if var1 == 0:
            return 0
        P = 1048576.0 - raw_P
        P = ((P - (var2 / 4096.0)) * 6250.0) / var1
        var1 = float(dig_P9) * P * P / 2147483648.0
        var2 = P * float(dig_P8) / 32768.0
        P = P + (var1 + var2 + float(dig_P7)) / 16.0
        P = P / 100

        Psea = P / pow(1.0 - altitude/44330.0, 5.255)
        return P, Psea

    def humidity_corrected(self, raw_H, t_fine):
        """calculates the compensated humidity in rel. %"""
        H = float(t_fine) - 76800.0
        H = (raw_H - (float(dig_H4) * 64.0 + float(dig_H5) / 16384.0 * H)) * (
             float(dig_H2) / 65536.0 * (
              1.0 + float(dig_H6) / 67108864.0 * H * (
               1.0 + float(dig_H3) / 67108864.0 * H)))
        H = H * (1.0 - float(dig_H1) * H / 524288.0)
        if H > 100:
            H = 100
        elif H < 0:
            H = 0
        return H


if __name__ == '__main__':

    BME280 = BME280_Sensor(HEX_ADDRESS=0x76)  # hex address can be adjusted to 0x77 using the SDO pin
    print()

    while True:
        BME280.sensor_forced_mode_1x()
        data_bytes = BME280.read_data_register()
        raw_T = BME280.temperature_raw(data_bytes)
        raw_P = BME280.pressure_raw(data_bytes)
        raw_H = BME280.humidity_raw(data_bytes)

        t_fine = BME280.temp_fine(raw_T)

        T = BME280.temperature_corrected(t_fine)
        P = BME280.pressure_corrected(raw_P, t_fine)
        H = BME280.humidity_corrected(raw_H, t_fine)

        print("***************************")
        print(' Temperature  =   {0:0.1f} deg'.format(T))
        print(' Pressure     =  {0:0.1f} hPa'.format(P[0]))
        print(' P (sea)      = {0:0.1f} hPa'.format(P[1]))
        print(' Humidity     =   {0:0.1f} %rH'.format(H))
        print("***************************")
        print()
        input("Press Enter to measure again...")
