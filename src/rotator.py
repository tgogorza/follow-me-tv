import sys
import RPi.GPIO as GPIO
from time import sleep

#pwm=GPIO.PWM(8, 50)
#pwm.start(0)

class Rotator:
	def __init__(self, min_angle=35, max_angle=145, pin=8, freq=50):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = GPIO.PWM(pin, freq)
		self.pwm.start(0)
		self.pin = pin
		self.setAngle(90)

	def __del__(self):
		self.pwm.stop()
		GPIO.cleanup()

	def setAngle(self, angle):
		duty = angle / 18 + 2
		if 0.0 <= duty <= 100.0: 
			GPIO.output(self.pin, True)
			self.angle = angle
			self.pwm.ChangeDutyCycle(duty)
			sleep(0.5)
			GPIO.output(self.pin, False)
			self.pwm.ChangeDutyCycle(0)
		else:
			print("EXCEEDED DUTY CYCLE: {}. Must be between 0.0 and 100.0")

	def getAngle(self):
		return self.angle

# if __name__ == "__main__":
# 	pwm=GPIO.PWM(8, 50)
# 	pwm.start(0)
# 	ang = int(sys.argv[1])
# 	setAngle(ang, pwm)
# 	pwm.stop()
# 	GPIO.cleanup()
