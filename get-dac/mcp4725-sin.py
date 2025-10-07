import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 3.2       
signal_frequency = 10   
sampling_frequency = 1000


I2C_ADDRESS = 0x61

if __name__ == "__main__":
    dac = None
    try:

        dac = mcp.MCP4725(
            dynamic_range=3.3,
            address=I2C_ADDRESS,
            verbose=False
        )

        start_time = time.time()

        while True:
            t = time.time() - start_time
            normalized_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
 
            voltage = normalized_amp * amplitude

            dac.set_voltage(voltage)

            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        if dac is not None:
            dac.deinit()
