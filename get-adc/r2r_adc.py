import RPi.GPIO as GPIO
from time import sleep


class R2R_ADC:
    def __init__(self, dynamic_range: float, compare_time: float = 1e-3, verbose: bool = False) -> None:
        self.dynrange = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose

        self.gpio_bits = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def __del__(self) -> None:
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def number_to_dac(self, number: int) -> None:
        if self.verbose:
            print("Установка числа...")
        if not (0 <= number <= 255):
            if self.verbose:
                print("> число выходит за допустимый предел 0...255, устанавливаем 0")
            number = 0
        bin_from_dec = [int(element) for element in bin(number)[2:].zfill(8)]
        if self.verbose:
            print("> вход в ЦАП:", number)
            print("> биты:", bin_from_dec)

        for i in range(len(self.gpio_bits)):
            GPIO.output(self.gpio_bits[i], bin_from_dec[i])
    
    def sequential_counting_adc(self) -> int:
        num = 0
        self.number_to_dac(num)
        while num < 256 and not GPIO.input(self.comp_gpio):
            num += 1
            self.number_to_dac(num)
            sleep(self.compare_time)
        return num
    
    def get_sc_voltage(self) -> float:
        return self.dynrange * self.sequential_counting_adc() / 255
    
    def successive_approximation_adc(self) -> int:
        left, right = 0, 256
        while left < right - 1:
            middle = (left + right) // 2
            self.number_to_dac(middle)
            sleep(self.compare_time)
            if GPIO.input(self.comp_gpio):
                right = middle
            else:
                left = middle
        return left

    def get_sar_voltage(self) -> float:
        return self.dynrange * self.successive_approximation_adc() / 255


if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.29)
        while True:
            try:
                print(f"Напряжение: {adc.get_sar_voltage():.3f} В")
                sleep(.25)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз.\n")
    except KeyboardInterrupt:
        print("Выключение...")
    except Exception as e:
        print(f"Ошибка: \"[{e.__class__.__name__}]: {e.args if len(e.args) > 0 else '<no args>'}\"")
