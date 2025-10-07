import r2r_dac as r2r
import triangle_generator as sg
import time

amplitude = 3.2          
signal_frequency = 10   
sampling_frequency = 1000  

if __name__ == "__main__":
    dac = None
    try:
        dac = r2r.R2R_DAC(
            gpio_bits=[16, 20, 21, 25, 26, 17, 27, 22],
            dynamic_range=3.3,
            verbose=False
        )

        start_time = time.time()

        while True:

            t = time.time() - start_time
            normalized_amp = sg.get_triangle_amplitude(signal_frequency, t)

            voltage = normalized_amp * amplitude

            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)

    finally:

        if dac is not None:
            dac.deinit()
        #GPIO.cleanup()
