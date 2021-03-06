echo enter number in /dev/video for one cam
read num1
echo other cam
read num2

v4l2-ctl -d /dev/video$num1 \
--set-ctrl=brightness=120 \
--set-ctrl=contrast=32 \
--set-ctrl=saturation=58 \
--set-ctrl=white_balance_temperature_auto=0 \
--set-ctrl=white_balance_temperature=6000\
--set-ctrl=gain=64 \
--set-ctrl=power_line_frequency=2 \
--set-ctrl=sharpness=22 \
--set-ctrl=backlight_compensation=1 \
--set-ctrl=exposure_auto_priority=0 \
--set-ctrl=exposure_auto=1 \
--set-ctrl=exposure_absolute=200 \
--set-ctrl=focus_auto=0 \
--set-ctrl=focus_absolute=0 \
--set-ctrl=zoom_absolute=1

v4l2-ctl -d /dev/video$num2 \
--set-ctrl=brightness=120 \
--set-ctrl=contrast=32 \
--set-ctrl=saturation=58 \
--set-ctrl=white_balance_temperature_auto=0 \
--set-ctrl=white_balance_temperature=6000\
--set-ctrl=gain=64 \
--set-ctrl=power_line_frequency=2 \
--set-ctrl=sharpness=22 \
--set-ctrl=backlight_compensation=1 \
--set-ctrl=exposure_auto_priority=0 \
--set-ctrl=exposure_auto=1 \
--set-ctrl=exposure_absolute=200 \
--set-ctrl=focus_auto=0 \
--set-ctrl=focus_absolute=0 \
--set-ctrl=zoom_absolute=1
