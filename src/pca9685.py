import RPi.GPIO as GPIO
import smbus2

# Set values to be written to registers
_address = 0x40

REG_MODE1 = 0x00
REG_MODE2 = 0x01
REG_LED0_ON_L = 0x06
REG_LED0_OFF_L = 0x08

REG_ALL_LED_ON_L = 0xfa
REG_ALL_LED_OFF_L = 0xfc

REG_PRESCALE = 0xfe

MODE1_SLEEP = 1 << 4
MODE1_EXTCLK = 1 << 6
MODE1_AI = 1 << 5 # enable auto-increment control register

class RawAccess:
    def __init__(self, owner):
        self.owner = owner
    def __repr__(self):
        return repr(self.owner.channels_get_raw_all())
    def __getitem__(self, key):
        return self.owner.channel_get_raw(key)
    def __setitem__(self, key, value):
        self.owner.channel_set_raw(key, value)
    def __len__(self):
        return 16
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        if self.n < 16:
            return self[self.n]
            self.n += 1
        else:
            raise StopIteration

class PwmAccess(RawAccess):
    def __repr__(self):
        return repr(self.owner.channels_get_pwm_all())
    def __getitem__(self, key):
        return self.owner.channel_get_pwm(key)
    def __setitem__(self, key, value):
        self.owner.channel_set_pwm(key, value)

class DutyAccess(RawAccess):
    def __repr__(self):
        return repr(["%.2f" % d for d in self.owner.channels_get_duty_all()])
    def __getitem__(self, key):
        return self.owner.channel_get_duty(key)
    def __setitem__(self, key, value):
        self.owner.channel_set_duty(key, value)

class PCA9685:
    def __init__(self, bus=4):
        self.extclk = 25e6 # BlueRobotics uses 24.567e6, we have dif clock
        self._bus = smbus2.SMBus(bus)
        self.initialize()
        # Configure output enable pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)

    def initialize(self):

        self.write(REG_MODE1, [MODE1_SLEEP | MODE1_AI])
        self.get_prescaler()

    #########################
    # Prescaler Configuration
    #########################
    def get_prescaler(self):
        prescaler = self._bus.read_i2c_block_data(_address, REG_PRESCALE, 1)[0]
        # cache this value to be used in pwm to duty conversions
        self.period_us = 1e6/self.prescaler_to_frequency(prescaler)
        return prescaler

    def set_prescaler(self, prescaler):
        # pca must be in sleep mode
        self.write(REG_MODE1, [MODE1_EXTCLK | MODE1_SLEEP | MODE1_AI])

        # prescaler minimum limited to 3 by hardware
        if prescaler < 3 or prescaler > 0xff:
            #print("new prescaler out of range: %s" % prescaler)
            return False
        prescaler = prescaler & 0xff

        # after entering sleep mode, the output counters are disabled (the
        # outputs go to zero) until one of the output counter registers
        # is written. (this is not documented, and can apparently be done
        # before or after exiting sleep mode)
        self.raw[0] = self.raw[0]

        # write the prescaler
        self.write(REG_PRESCALE, [prescaler & 0xff])

        # bring out of sleep mode
        self.write(REG_MODE1, [MODE1_EXTCLK | MODE1_AI])

        # verify the prescaler
        current = self.get_prescaler()
        if current != prescaler:
            #print("error writing new prescaler. wrote: %2x read %2x" % (prescaler, current))
            return False

        return True

    def set_pwm_frequency(self, target_frequency_hz):
        # frequency = extclk/(4096*(prescaler + 1))
        # extclk/(f * 4096) - 1 = prescaler
        new_prescaler = self.frequency_to_prescaler(target_frequency_hz)
        if not self.set_prescaler(new_prescaler):
            old_prescaler = self.get_prescaler()
            old_frequency = self.prescaler_to_frequency(old_prescaler)
            return old_frequency
        new_frequency = self.prescaler_to_frequency(new_prescaler)
        return new_frequency

    ###################
    # Output Functions
    ###################

    # set OE pin LOW
    def output_enable(self):
        GPIO.output(26, GPIO.LOW)
        return

    # set OE pin HIGH
    def output_disable(self):
        GPIO.output(26, GPIO.HIGH)
        return

    # get the state of the output enable pin
    # todo
    def output_enabled(self):
        return True

    # clear all pwm output registers
    def output_clear(self):
        self.channels_set_raw_all(0)

    ##########################
    # List interface
    ##########################
    @property
    def raw(self):
        return RawAccess(self)

    @raw.setter
    def raw(self, values):
        self.channels_set_raw(values)

    @property
    def duty(self):
        return DutyAccess(self)
    
    @duty.setter
    def duty(self, values):
        self.channels_set_duty(values)
    
    @property
    def pwm(self):
        return PwmAccess(self)

    @pwm.setter
    def pwm(self, values):
        self.channels_set_pwm(values)

    #####################
    # Channel access
    #####################
    def channel_get_raw(self, channel):
        data = self._bus.read_i2c_block_data(_address, self.offreg(channel), 2)
        return self.data_to_raw(data)

    def channel_get_duty(self, channel):
        return self.raw_to_duty(self.channel_get_raw(channel))

    def channel_get_pwm(self, channel):
        return self.raw_to_pwm(self.channel_get_raw(channel))

    def channels_get_raw_all(self):
        return [self.channel_get_raw(channel) for channel in range(16)]

    def channels_get_duty_all(self):
        return [self.raw_to_duty(raw) for raw in self.channels_get_raw_all()]

    def channels_get_pwm_all(self):
        return [self.raw_to_pwm(duty) for duty in self.channels_get_raw_all()]

    # write a single channel output value
    def channel_set_raw(self, channel, raw):
        data = self.raw_to_data(raw)
        offreg = self.offreg(channel)
        self.write(offreg, data)
        read = self.read(offreg, len(data))
        if read != data:
            raise Exception(f'pca9685 register write failed\noffreg:{offreg}\nwrote:{data}\nread:{read}')

    def channel_set_duty(self, channel, duty):
        raw = self.duty_to_raw(duty)
        self.channel_set_raw(channel, raw)

    def channel_set_pwm(self, channel, pwm_us):
        raw = self.pwm_to_raw(pwm_us)
        self.channel_set_raw(channel, raw)

    # write multiple individual channel output values with minimal bus transactions
    def channels_set_raw(self, duties):
        data = []
        # 16 channels max
        for duty in duties[:16]:
            data.extend([0,0])
            data.extend(self.raw_to_data(duty))
        self.write(REG_LED0_ON_L, data)
        read = self.read(REG_LED0_ON_L, len(data))
        if read != data:
            raise Exception(f'pca9685 register write failed\nwrote:{data}\nread:{read}')

    def channels_set_duty(self, duties):
        raws = [self.duty_to_raw(duty) for duty in duties]
        self.channels_set_raw(raws)
        
    def channels_set_pwm(self, pwms_us):
        raws = [self.pwm_to_raw(pwm_us) for pwm_us in pwms_us]
        self.channels_set_raw(raws)

    # write all channels to the same output value with minimal bus transactions
    def channels_set_raw_all(self, raw):
        data = self.raw_to_data(raw)
        self.write(REG_ALL_LED_OFF_L, data)

    def channels_set_duty_all(self, duty):
        self.channels_set_raw_all(self.duty_to_raw(duty))

    def channels_set_pwm_all(self, pwm_us):
        self.channels_set_raw_all(self.pwm_to_raw(pwm_us))

    #############
    # Bus Transactions
    #############
    def read(self, register_address, nbytes):
        data = self._bus.read_i2c_block_data(_address, register_address, nbytes)
        #print("i2c read  0x%.2x: %s" % (register_address, [hex(d) for d in data]))
        return data

    def write(self, register_address, data):
        #print("i2c write 0x%.2x: %s" % (register_address, [hex(d) for d in data]))
        data2 = data.copy()
        data2.insert(0, register_address)
        msg = smbus2.i2c_msg.write(_address, data2)
        self._bus.i2c_rdwr(msg)

    ##############
    # Conversion facilities
    ##############

    def offreg(self, channel):
        return REG_LED0_OFF_L + (channel*4)

    # f(prescaler + 1) = extclk/(4096)
    def prescaler_to_frequency(self, prescaler):
        return self.extclk/(4096*(prescaler + 1)) # todo check the math?

    # may not be exact
    # datasheet section 7.2.5:
    # prescaler = round(extclk/(4096*f)) - 1
    def frequency_to_prescaler(self, frequency_hz):
        return round(self.extclk/(4096*frequency_hz)) - 1 # todo check the math?

    def raw_to_pwm(self, raw):
        return round(raw*self.period_us/0xfff)

    # convert pwm microsecond duty to LEDn_OFF register value
    def pwm_to_raw(self, pwm_us):
        return round(0xfff*pwm_us/self.period_us)

    def raw_to_duty(self, raw):
        return raw/4095.0

    #todo double check this math
    def duty_to_raw(self, duty):
        return round(duty*4095)

    def raw_to_data(self, raw):
        data = [0]*2
        data[0] = raw & 0xff
        data[1] = (raw >> 8) & 0x0f
        return data

    def data_to_raw(self, data):
        return (data[1] << 8) | data[0]