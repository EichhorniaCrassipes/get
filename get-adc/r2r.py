import RPi.GPIO as GPIO
from time import sleep

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self) -> None:
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_adc(self, number: int) -> None:
        if self.verbose:
            print("Устанавливаю число... ")
        if not (0 <= number <= 255):
            if self.verbose:
                print("Число выходит за диапазон 0...255. Устанавливаю 0. ")
            number = 0

        bin_from_dec = [int(element) for element in bin(number)[2:].zfill(8)]
        if self.verbose:
            print("Вход в АЦП: ")
            print("bits: ", bin_from_dec)
        
        for i in range(len(self.bits_gpio)):
            GPIO.output(self.bits_gpio[i], bin_from_dec[i])

    def sequential_counting_adc(self) -> int:
        num = 0
        self.number_to_adc(num)
        while num < 256 and not GPIO.input(self.comp_gpio):
            num+=1
            self.number_to_adc(num)
            sleep(self.compare_time)
        return num

    def get_sc_voltage(self) -> float:
        return self.dynamic_range * self.sequential_counting_adc()/255

    def successive_approximation_adc(self) -> int:
        left, right = 0, 256
        while left < right-1:
            middle = (left + right) // 2
            self.number_to_adc(middle)
            sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                right = middle
            else:
                left = middle
        return left

    def get_sar_voltage(self) -> float:
        return self.dynamic_range * self.successive_approximation_adc()/255


if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.29)
        while True:
            try:
                print(f"Напряжение: {adc.get_sar_voltage():.3f} В")
                sleep(.25)
            except ValueError:
                print("Вы не ввели число. Попробуйте снова!")
        except KeyboardInterrupt:
            print("Выключение...")
        except Exception as e:
            print(f"Ошибка")