import smbus
import RPi.GPIO as GPIO

class MCP4725:
    def __init__(self, dynamic_range, address=0x60, verbose=True):
        # Примечание: стандартный адрес MCP4725 — 0x60 или 0x61 в зависимости от подтяжки A0
        self.bus = smbus.SMBus(1)
        self.address = address
        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()

    def set_number(self, number):
        if not isinstance(number, int):
            if self.verbose:
                print("На вход ЦАП можно подавать только целые числа")
            return

        if not (0 <= number <= 4095):
            if self.verbose:
                print("Число выходит за разрядность MCP4725 (12 бит). Устанавливаем 0.")
            number = 0

        # MCP4725 ожидает 12-битное значение: старшие 4 бита — нули, затем 12 бит данных
        # Формат: [C2 C1 C0 x x PD1 PD0 D11 D10 ... D0]
        # Для простой записи: C2=C1=C0=0, PD1=PD0=0 → команда = 0b01100000 = 0x60? 
        # Но на самом деле: при записи через fast mode (без команды) — просто два байта:
        # high_byte = (number >> 8) & 0x0F  # только 4 младших бита
        # low_byte  = number & 0xFF

        high_byte = (number >> 8) & 0x0F  # 4 бита данных (D11-D8)
        low_byte = number & 0xFF          # D7-D0

        # Отправляем два байта данных (fast write mode)
        self.bus.write_i2c_block_data(self.address, 0x00, [high_byte, low_byte])

        if self.verbose:
            print(f"Число: {number} (0x{number:03X}), отправлено: [0x{high_byte:02X}, 0x{low_byte:02X}]")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 – {self.dynamic_range:.3f} В)")
                print("Устанавливаем 0.0 В")
            voltage = 0.0

        # Преобразуем напряжение в 12-битное число
        number = int(voltage / self.dynamic_range * 4095)
        self.set_number(number)


if __name__ == "__main__":
    dac = None
    try:
        # Убедитесь, что адрес правильный! Обычно 0x60 или 0x61.
        # Проверьте: i2cdetect -y 1
        dac = MCP4725(dynamic_range=3.3, address=0x60, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз.\n")
    finally:
        if dac is not None:
            dac.deinit()
        GPIO.cleanup()  # хотя GPIO не используется, но на всякий случай
