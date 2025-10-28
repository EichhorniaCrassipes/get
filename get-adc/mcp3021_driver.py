import smbus
from time import sleep

class MCP3021:
    def __init__(self, dynamic_range: float, address=0x4D, verbose: bool = False) -> None:
        self.bus = smbus.SMBus(1)
        self.address = address

        self.verbose = verbose
        self.dynrange = dynamic_range

    def __del__(self) -> None:
        self.bus.close()
    
    def get_number(self) -> int:
        data = self.bus.read_word_data(self.address, 0)
        lower_byte = data >> 8
        upper_byte = data & 0xFF
        number = (upper_byte << 6) | (lower_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data} | верхний/нижний: {upper_byte:x}/{lower_byte:x}, число: {number}")
        return number

    def get_voltage(self) -> float:
        return self.dynrange * self.get_number() / 1024


if __name__ == "__main__":
    adc = MCP3021(5.20, verbose=True)
    try:
        while True:
            try:
                print(f"Напряжение: {adc.get_voltage():.3f} В")
                sleep(.25)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз.\n")
    except KeyboardInterrupt:
        print("Выключение...")
    except Exception as e:
        print(f"Неизвестная ошибка: \"[{e.__class__.__name__}]: {e.args if len(e.args) > 0 else '<no args>'}\"")
