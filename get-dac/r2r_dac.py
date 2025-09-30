import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        if not (0 <= number <= 255):
            if self.verbose:
                print("Число выходит за пределы диапазона (0–255). Устанавливаем 0.")
            number = 0

        bin_repr = [int(bit) for bit in bin(number)[2:].zfill(8)]
        
        for i in range(len(self.gpio_bits)):
            GPIO.output(self.gpio_bits[i], bin_repr[i])

        if self.verbose:
            print(f"Число на вход в ЦАП: {number}")
            print(f"Биты: {bin_repr}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 – {self.dynamic_range:.3f} В)")
                print("Устанавливаем 0.0 В")
            voltage = 0.0

        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)


if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы не ввели число. Попробуйте еще раз.\n")
    finally:
        dac.deinit()
