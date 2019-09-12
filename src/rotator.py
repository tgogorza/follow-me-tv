import sys
import RPi.GPIO as GPIO
from time import sleep

#pwm=GPIO.PWM(8, 50)
#pwm.start(0)

class Rotator:
	def __init__(self, min_angle=35, max_angle=145, pin=8, freq=50):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		self.pwm=GPIO.PWM(pin, freq)
		self.pwm.start(0)
		self.pin = pin
		self.ang = 90
		SetAngle(ang, pwm)

	def __del__(self):
		self.pwm.stop()
		GPIO.cleanup()

	def SetAngle(angle):
		duty = angle / 18 + 2
		GPIO.output(self.pin, True)
		self.pwm.ChangeDutyCycle(duty)
		sleep(0.5)
		GPIO.output(self.pin, False)
		self.pwm.ChangeDutyCycle(0)

# if __name__ == "__main__":
# 	pwm=GPIO.PWM(8, 50)
# 	pwm.start(0)
# 	ang = int(sys.argv[1])
# 	SetAngle(ang, pwm)
# 	pwm.stop()
# 	GPIO.cleanup()
