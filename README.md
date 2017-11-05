# ubit-BME280

Basic functions to use the BME280 breakout board with the
Bosch Sensortec ME280 Temperature, Humidity and Pressure Sensor
with the I2C interface on the micro:bit.

see: https://www.bosch-sensortec.com/bst/products/all_products/bme280 for the Sensor datasheet
and: https://www.microbit.co.uk/home for the micro:bit.

**how to connect the breakout board to the micro:bit:**

SCL --> pin19

SDA --> pin20

VDD --> 3V

GND --> 0


**Note: sensor calibration parameters stored in registers 0x88-0xA1 and 0xE01-0xE07 
 are declared due to memory restrictions on the micro:bit.
 Use get_calibration_data.py to read the needed values**

Class currently implements only "forced mode" (meaning that a single measurement
is performed, when finished, the sensor returns to sleep mode and the measurement
results can be read from the data registers) and the recommended settings
for "Weather monitoring" (1x oversampling for temperature,
humidity and pressure, filter OFF). This can be easily adjusted by setting
the corresponding CTRL_HUM = 0XF2, CTRL_MEAS = 0XF4, and CONFIG = 0xF5 registers.   
