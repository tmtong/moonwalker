import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from pynput import keyboard



class FakeMotorPublisher(Node):
    left_state = 1
    right_state = 1
    forward_state = 1
    backward_state = 1

    def __init__(self):
        super().__init__('motor_publisher')
        self.publisher_ = self.create_publisher(Twist, 'direction', 1)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        
        # Collect events until released
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def on_press(self, key):
        try:
            if keyboard.Key.left == key:
                self.left_state = -1
            if keyboard.Key.right == key:
                self.right_state = -1
            if keyboard.Key.up == key:
                self.forward_state = -1
            if keyboard.Key.down == key:
                self.backward_state = -1
        except AttributeError:
            pass

    def on_release(self, key):
        if keyboard.Key.left == key:
            self.left_state = 1
        if keyboard.Key.right == key:
            self.right_state = 1
        if keyboard.Key.up == key:
            self.forward_state = 1
        if keyboard.Key.down == key:
            self.backward_state = 1
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def timer_callback(self):
        forward_velocity = 1.0
        turn_angular_velocity = 1.0
        my_velocity = Twist()
        if self.forward_state == -1:
            my_velocity.linear.x = forward_velocity
        if self.backward_state == -1:
            my_velocity.linear.x = -forward_velocity
        if self.left_state == -1:
            my_velocity.angular.z = turn_angular_velocity
        if self.right_state == -1:
            my_velocity.angular.z = -turn_angular_velocity

        self.publisher_.publish(my_velocity)
        # self.get_logger().info('Publishing: "%s"' % my_velocity)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    motor_publisher = FakeMotorPublisher()

    rclpy.spin(motor_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Motor_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


