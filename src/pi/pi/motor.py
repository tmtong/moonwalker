import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from geometry_msgs.msg import Twist
import json
import argparse
import time
class MotorSubscriber(Node):

    def __init__(self):
        print('constructor')
        self.init_pins()
        # self.fake_pin()
    def connect(self):
        print('connect')
        super().__init__('motor_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'direction',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
    def fake_pin(self):
        self.leftin1 = SimulatedPWN('leftin1')
        self.leftin2 = SimulatedPWN('leftin2')
        self.rightin1 = SimulatedPWN('rightin1')
        self.rightin2 = SimulatedPWN('rightin2')
    def init_pins(self):
        print('init_pins')
        self.leftin1pin = 24
        self.leftin2pin = 23
        self.leften = 25

        self.rightin1pin = 27
        self.rightin2pin = 22
        self.righten = 17
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftin1pin,GPIO.OUT)
        GPIO.setup(self.leftin2pin,GPIO.OUT)
        GPIO.setup(self.leften,GPIO.OUT)
        GPIO.output(self.leftin1pin,GPIO.LOW)
        GPIO.output(self.leftin2pin,GPIO.LOW)
        self.leftpwm=GPIO.PWM(self.leften,1000)
        self.leftpwm.start(25)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rightin1pin,GPIO.OUT)
        GPIO.setup(self.rightin2pin,GPIO.OUT)
        GPIO.setup(self.righten,GPIO.OUT)
        GPIO.output(self.rightin1pin,GPIO.LOW)
        GPIO.output(self.rightin2pin,GPIO.LOW)
        self.rightpwm=GPIO.PWM(self.righten,1000)
        self.rightpwm.start(25)

    def infinite_loop(self):
        while True:
            time.sleep(1)
    def change_left_motor(self, left_speed):
        print('left speed ' + str(left_speed))
        left_speed = float(left_speed)
        if left_speed < 0:
            self.leftpwm.ChangeDutyCycle(abs(left_speed))
            GPIO.output(self.leftin1pin,GPIO.LOW)
            GPIO.output(self.leftin2pin,GPIO.HIGH)
        if left_speed == 0:
            self.leftpwm.ChangeDutyCycle(0)
            GPIO.output(self.leftin1pin,GPIO.LOW)
            GPIO.output(self.leftin2pin,GPIO.LOW)
        if left_speed > 0:
            self.leftpwm.ChangeDutyCycle(abs(left_speed))
            GPIO.output(self.leftin1pin,GPIO.HIGH)
            GPIO.output(self.leftin2pin,GPIO.LOW)
    def change_right_motor(self, right_speed):
        print('right speed ' + str(right_speed))
        right_speed = float(right_speed)
        if right_speed < 0:
            self.rightpwn.ChangeDutyCycle(abs(right_speed))
            GPIO.output(self.leftin1pin,GPIO.LOW)
            GPIO.output(self.leftin2pin,GPIO.HIGH)
        if right_speed == 0:
            self.rightpwm.ChangeDutyCycle(0)
            GPIO.output(self.rightin1pin,GPIO.LOW)
            GPIO.output(self.rightin2pin,GPIO.LOW)
        if right_speed > 0:
            self.rightpwm.ChangeDutyCycle(abs(right_speed))
            GPIO.output(self.rightin1pin,GPIO.HIGH)
            GPIO.output(self.rightin2pin,GPIO.LOW)
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
        
        change_left_wheel(left_speed)
        change_right_wheel(right_speed)
        
       

        self.get_logger().info('Received: "%s"' % str(msg.linear.x))
def ros_loop():
    rclpy.init(args=args)

    motor_subscriber = MotorSubscriber()
    motor_subscriber.connect()
    rclpy.spin(motor_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    motor_subscriber.destroy_node()
    rclpy.shutdown()

def main(args=None):

    parser = argparse.ArgumentParser(description='L298N Driver')
    parser.add_argument('--left', action='store', default=False,
                    dest='left_test',
                    help='Test left')
    parser.add_argument('--right', action='store', default=False,
                    dest='right_test',
                    help='Test right')
    parser.add_argument('--ros', action='store_true', default=False,
                    dest='ros',
                    help='Controlled by ROS Stack')
    results = parser.parse_args()
    print(results)
    if results.left_test != None and results.left_test != False:
        motor_subscriber = MotorSubscriber()
        motor_subscriber.change_left_motor(results.left_test)
        motor_subscriber.infinite_loop()
    elif results.right_test != None and results.right_test != False:
        motor_subscriber = MotorSubscriber()
        motor_subscriber.change_right_motor(results.right_test)
        motor_subscriber.infinite_loop()
    elif results.ros != None and results.ros != False:
        ros_loop()
    


if __name__ == '__main__':
    main()

