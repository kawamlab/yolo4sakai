from signal import pause

from gpiozero import LED

valve1 = LED("GPIO26")
valve2 = LED("GPIO12")

if __name__ == "__main__":
    valve1.blink(1, 1)
    valve2.blink(1, 1)
    # valve2.blink(1, 1, 5, background=True)

    try:
        pause()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        valve1.off()
        valve2.off()
        print("Cleaned up GPIO pins.")
