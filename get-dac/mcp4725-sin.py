import mcp4725_driver as mcp
import signal_generator as sg

amplitude = 3.2          
signal_frequency = 10   
sampling_frequency = 1000  

if __name__ == "__main__":
    dac = None
    try:
        mcp_obj = mcp.MCP4725(
            gpio_pin=PWM_PIN,
            pwm_frequency=PWM_FREQUENCY,
            dynamic_range=3.3,
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
