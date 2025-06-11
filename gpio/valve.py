import atexit
import time
from signal import pause

from gpiozero import DigitalOutputDevice


class AutoFactory:
    def __init__(self):
        self.cam = DigitalOutputDevice("26")
        self.blower = DigitalOutputDevice("12")

        atexit.register(self.cleanup)

    def throughput(self):
        print("Starting throughput...")
        self.cam.on()

        # change here
        time.sleep(1)

        self.cam.off()

    def blowout(self, on_time=0.5, off_time=0.5, count=3, background=True):
        # brow three times
        print("Starting blowout...")
        self.blower.blink(
            on_time=on_time,
            off_time=off_time,
            n=count,
            background=background,
        )

    def cleanup(self):
        self.cam.off()
        self.blower.off()
        print("GPIO pins cleaned up.")

    def test_valve(self):
        print("starting valve test...")
        print(f"Valve 1: {self.cam.pin}, Valve 2: {self.blower.pin}")
        print("Turning on valves...")

        # self.blowout()
        pause()

        self.cam.on()
        self.blower.on()

        try:
            while True:
                time.sleep(0.5)
                self.cam.toggle()
                self.blower.toggle()
        except KeyboardInterrupt:
            print("Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    af = AutoFactory()
    af.test_valve()
