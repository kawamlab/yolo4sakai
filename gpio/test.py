from valve import AutoFactory


if __name__ == "__main__":
    af = AutoFactory()

    # Test blowout functionality
    # af.blowout(on_time=0.5, off_time=0.5, count=3, background=False)

    # Test valve functionality
    # af.test_valve()

    # Test interrupt sensor
    af.test_intr()
