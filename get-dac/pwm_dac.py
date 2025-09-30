import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial=0)

        self.pwm = GPIO.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0) 

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 – {self.dynamic_range:.3f} В)")
                print("Устанавливаем 0.0 В")
            voltage = 0.0

        duty_cycle = (voltage / self.dynamic_range) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

        if self.verbose:
            print(f"Установлено напряжение: {voltage:.3f} В (скважность: {duty_cycle:.2f}%)")

if __name__ == "__main__":
    dac = None  
    try:
        dac = PWM_DAC(gpio_pin=12, pwm_frequency=1000, dynamic_range=3.290, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз.\n")
    finally:
        if dac is not None:
            dac.deinit()
