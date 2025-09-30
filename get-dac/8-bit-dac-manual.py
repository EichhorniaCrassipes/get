import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac_bits = [22, 27, 17, 26, 25, 21, 20, 16]

GPIO.setup(dac_bits, GPIO.OUT)

GPIO.output(dac_bits, 0)

dynamic_range = 3.17

def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number):
    if not (0 <= number <= 255):
        return 0
    bin_from_dec = [int(element) for element in bin(number)[2:].zfill(8)]
    for i in range(len(dac_bits)):
        GPIO.output(dac_bits[i], bin_from_dec[i])


try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
            print(f"Число на вход в ЦАП: {number}")
            print(f"биты: {[int(element) for element in bin(number)[2:].zfill(8)]}")
            
        
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")
        
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()
