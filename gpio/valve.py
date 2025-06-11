import atexit
import time

from gpiozero import OutputDevice


class AutoFactory:
    def __init__(self):
        self.cam = OutputDevice("26")
        self.blower = OutputDevice("12")

        atexit.register(self.cleanup)

    def throughput(self):
        print("Starting throughput...")
        self.cam.on()

        # change here
        time.sleep(1)

        self.cam.off()

    def blowout(self):
        # brow three times
        print("Starting blowout...")
        for _ in range(3):
            self.blower.on()
            time.sleep(0.5)
            self.blower.off()
            time.sleep(0.5)

    def cleanup(self):
        self.cam.off()
        self.blower.off()
        print("GPIO pins cleaned up.")

    def test_valve(self):
        print("starting valve test...")
        print(f"Valve 1: {self.cam.pin}, Valve 2: {self.blower.pin}")
        print("Turning on valves...")

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
