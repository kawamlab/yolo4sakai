#!/bin/bash

DEVICE=/dev/video0

v4l2-ctl -d $DEVICE \
  -c brightness=0 \
  -c contrast=32 \
  -c saturation=75 \
  -c hue=0 \
  -c white_balance_automatic=0 \
  -c white_balance_temperature=4600 \
  -c gamma=100 \
  -c gain=0 \
  -c power_line_frequency=1 \
  -c sharpness=3 \
  -c backlight_compensation=1 \
  -c auto_exposure=1 \
  -c exposure_time_absolute=5000 \
  -c exposure_dynamic_framerate=0
