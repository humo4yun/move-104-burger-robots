#!/usr/bin/env python3
import rospy, math, random, sys
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker
from tf.transformations import euler_from_quaternion

def get_font_pts(ox, digit):
    pts = []; g = 0.65; lean = 0.3
    if digit == "2":
        mask = [(x,y) for x in range(5) for y in [0,1,3,4,6,7]] + [(3,5),(4,5),(0,2),(1,2)]
    elif digit == "0":
        mask = [(x,y) for x in range(5) for y in [0,1,6,7]] + [(0,y) for y in range(2,6)] + [(1,y) for y in range(2,6)] + [(3,y) for y in range(2,6)] + [(4,y) for y in range(2,6)]
    elif digit == "5":
        mask = [(x,y) for x in range(5) for y in [0,1,3,4,6,7]] + [(0,5),(1,5),(3,2),(4,2)]
    
    unique_mask = sorted(list(set(mask)))
    for (x, y) in unique_mask:
        pts.append((ox + x*g + y*lean, y*g))
    return pts[:34] if digit != "0" else pts[:36]

T2, T0, T5 = get_font_pts(-15, "2"), get_font_pts(-2, "0"), get_font_pts(11, "5")
ALL_TARGETS = sorted(T2 + T0 + T5, key=lambda p: p[0])

class Robot:
    def __init__(self, id, target, delay):
        self.id, self.name, self.target, self.ready, self.done = id, f"tb3_{id}", target, False, False
        self.delay_offset = delay
        self.start_t, self.x, self.y, self.yaw = 0, 0.0, 0.0, 0.0
        self.pub = rospy.Publisher(f"/{self.name}/cmd_vel", Twist, queue_size=1)
        self.m_pub = rospy.Publisher('/swarm_markers', Marker, queue_size=100)
        rospy.Subscriber(f"/{self.name}/odom", Odometry, self.cb)
        self.marker = Marker()
        self.marker.header.frame_id, self.marker.ns, self.marker.id = "world", "trails", id
        self.marker.type, self.marker.scale.x, self.marker.color.a = Marker.LINE_STRIP, 0.06, 1.0
        if id <= 34: self.marker.color.r = 1.0 
        elif id <= 70: self.marker.color.g = 1.0
        else: self.marker.color.b = 1.0

    def cb(self, msg):
        self.x, self.y = msg.pose.pose.position.x, msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, self.yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        self.ready = True
        if not self.done and not rospy.is_shutdown():
            self.marker.points.append(Point(self.x, self.y, 0.01))
            self.marker.header.stamp = rospy.Time.now()
            try: self.m_pub.publish(self.marker)
            except: pass

    def step(self, mode="MOVE"):
        if self.done and mode == "MOVE": return True
        if rospy.get_time() < self.start_t: return False
        cmd = Twist()
        if mode == "DANCE":
            cmd.angular.z = 5.0 * math.sin(rospy.get_time() * 15); self.pub.publish(cmd); return True
        dist = math.hypot(self.target[0]-self.x, self.target[1]-self.y)
        if dist < 0.15:
            self.pub.publish(Twist()); self.done = True; return True
        angle = math.atan2(self.target[1]-self.y, self.target[0]-self.x) - self.yaw
        while angle > math.pi: angle -= 2*math.pi
        while angle < -math.pi: angle += 2*math.pi
        if abs(angle) > 0.4:
            cmd.angular.z = max(-2.0, min(4.5 * angle, 2.0)); cmd.linear.x = 0.0
        else:
            cmd.linear.x = min(0.4, 1.1 * dist); cmd.angular.z = 1.2 * angle
        self.pub.publish(cmd); return False

def main():
    rospy.init_node("final_205_italic")
    num = 104
    bots = [Robot(i+1, (0,0), i*0.06) for i in range(num)]
    while not rospy.is_shutdown() and not all(b.ready for b in bots): rospy.sleep(0.1)
    bots.sort(key=lambda b: b.x)
    for i in range(num): bots[i].target = ALL_TARGETS[i]
    input(">>> SAY 'FORMATION' OR PRESS ENTER <<<")
    t0 = rospy.get_time()
    for b in bots: b.start_t = t0 + b.delay_offset
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if all([b.step("MOVE") for b in bots]): break
        rate.sleep()
    rospy.loginfo("DONE! DANCING...")
    end_t = rospy.get_time() + 4.0
    while not rospy.is_shutdown() and rospy.get_time() < end_t:
        for b in bots: b.step("DANCE")
        rate.sleep()
    for b in bots: b.pub.publish(Twist())

if __name__ == "__main__": main()
