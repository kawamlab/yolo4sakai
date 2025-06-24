from signal import pause

from gpiozero import LED
from valve import AutoFactory


if __name__ == "__main__":
    af = AutoFactory()
    af.test_valve()
