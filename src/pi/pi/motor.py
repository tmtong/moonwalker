import rclpy
from rclpy.node import Node
# import RPi.GPIO as GPIO
from geometry_msgs.msg import Twist
import json

class SimulatedPWN():
    def __init__(self, name):
        self.name = name
    def ChangeDutyCycle(self, speed):
        print('Pin ' + self.name + ' run at ' + str(speed))


class MotorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'direction',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.init_pins()
        # self.fake_pin()
    def fake_pin(self):
        self.leftin1 = SimulatedPWN('leftin1')
        self.leftin2 = SimulatedPWN('leftin2')
        self.rightin1 = SimulatedPWN('rightin1')
        self.rightin2 = SimulatedPWN('rightin2')
    def init_pins(self):
        self.leftin1pin = 24
        self.leftin2pin = 23
        leften = 25

        self.rightin1pin = 27
        self.rightin2pin = 22
        righten = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(leftin1pin,GPIO.OUT)
        GPIO.setup(leftin2pin,GPIO.OUT)
        GPIO.setup(leften,GPIO.OUT)
        GPIO.output(leftin1pin,GPIO.LOW)
        GPIO.output(leftin2pin,GPIO.LOW)
        self.leftpwm=GPIO.PWM(leften,1000)
        self.leftpwm.start(25)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rightin1pin,GPIO.OUT)
        GPIO.setup(rightin2pin,GPIO.OUT)
        GPIO.setup(righten,GPIO.OUT)
        GPIO.output(rightin1pin,GPIO.LOW)
        GPIO.output(rightin2pin,GPIO.LOW)
        self.rightpwm=GPIO.PWM(righten,1000)
        self.rightpwm.start(25)

        
            
    def listener_callback(self, msg):
        left_speed = 0
        right_speed = 0
        full_speed = 60
        turn_diff = 20
        # should be 9 possiblities
        if msg.linear.x == 1 and msg.angular.z == 1:
            left_speed = full_speed - turn_diff
            right_speed = full_speed
        if msg.linear.x == 1 and msg.angular.z == -1:
            left_speed = full_speed
            right_speed = full_speed - turn_diff
        if msg.linear.x == 0 and msg.angular.z == 1:
            left_speed = 0
            right_speed = turn_diff
        if msg.linear.x == 0 and msg.angular.z == -1:
            left_speed = turn_diff
            right_speed = 0
        if msg.linear.x == 0 and msg.angular.z == 0:
            left_speed = 0
            right_speed = 0
        if msg.linear.x == 1 and msg.angular.z == 0:
            left_speed = full_speed
            right_speed = full_speed
        if msg.linear.x == -1 and msg.angular.z == 1:
            left_speed = -full_speed + turn_diff
            right_speed = -full_speed
        if msg.linear.x == -1 and msg.angular.z == -1:
            left_speed = -full_speed
            right_speed = -full_speed + turn_diff
        if msg.linear.x == -1 and msg.angular.z == 0:
            left_speed = -full_speed
            right_speed = -full_speed
        
        if left_speed < 0:
            self.leftpwm.ChangeDutyCycle(abs(left_speed))
            GPIO.output(self.leftin1,GPIO.LOW)
            GPIO.output(self.leftin2,GPIO.HIGH)
        if left_speed == 0:
            self.leftpwm.ChangeDutyCycle(0)
            GPIO.output(self.leftin1,GPIO.LOW)
            GPIO.output(self.leftin2,GPIO.LOW)
        if left_speed > 0:
            self.leftpwm.ChangeDutyCycle(abs(left_speed))
            GPIO.output(self.leftin1,GPIO.HIGH)
            GPIO.output(self.leftin2.GPIO.LOW)
        if right_speed < 0:
            self.rightpwn.ChangeDutyCycle(abs(right_speed))
            GPIO.output(self.leftin1,GPIO.LOW)
            GPIO.output(self.leftin2,GPIO.HIGH)
        if right_speed == 0:
            self.rightpwm.ChangeDutyCycle(0)
            GPIO.output(self.rightin1,GPIO.LOW)
            GPIO.output(self.rightin2,GPIO.LOW)
        if right_speed > 0:
            self.rightpwm.ChangeDutyCycle(abs(right_speed))
            GPIO.output(self.rightin1,GPIO.HIGH)
            GPIO.output(self.rightin2.GPIO.LOW)

        self.get_logger().info('Received: "%s"' % str(msg.linear.x))


def main(args=None):
    rclpy.init(args=args)

    motor_subscriber = MotorSubscriber()

    rclpy.spin(motor_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    motor_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

