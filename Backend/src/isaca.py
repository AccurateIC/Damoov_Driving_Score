#!/usr/bin/env python

import rospy
import numpy as np
import sys
import os
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import OccupancyGrid, Odometry
from custom_sensor_msgs.msg import CentroidTrackArray
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Utilities.common_utilities import global_to_local_tf


class OccupancyGridPublisher:
    def __init__(self, grid_width=20, grid_height=20, grid_resolution=30, usv_grid_x=1, repulsion_range=2):
        rospy.init_node('occupancy_grid')

        # Save parameters as class attributes
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.GRID_RESOLUTION = grid_resolution
        self.USV_GRID_X = usv_grid_x
        self.USV_GRID_Y = (grid_height // 2)
        self.repulsion_range = repulsion_range

        # Publishers
        self.grid_pub = rospy.Publisher('/occupancy_grid', OccupancyGrid, queue_size=1)
        self.rviz_grid_pub = rospy.Publisher('/occupancy_grid_for_rviz', OccupancyGrid, queue_size=1)

        # Subscribers
        rospy.Subscriber('/radar/processed_centroids', CentroidTrackArray, self.processed_centroid_callback)
        rospy.Subscriber('/odometry/wamv_imu', Odometry, self.odometry_callback, queue_size=10)
        rospy.Subscriber('/radar/raw_radar_points', Float64MultiArray, self.raw_radar_points_callback)
        rospy.Subscriber('/radar/colliding_cpas', Float64MultiArray, self.colliding_cpas_callback)

        # Object tracking
        self.raw_radar_points = []                                      # Raw radar detections
        self.dynamic_objects = []                                       # Dynamic obstacles (CPA points)
        self.dynamic_objects_rviz = []                                  # Same but flipped Y for RViz
        self.static_points = []                                         # Static radar obstacles
        self.static_points_rviz = []                                    # Flipped Y for RViz
        self.cpa_points = []

        # Hard-coded obstacles (for testing only)
        self.hard_coded_obstacles = []
        self.hard_coded_obstacles_rviz = [(x, -y) for (x, y) in self.hard_coded_obstacles]

        # Timer for periodic publishing (10 Hz)
        self.timer = rospy.Timer(rospy.Duration(0.1), self.publish_grid)

        rospy.loginfo("Occupancy Grid Node Initialized")

    # ---------------- Utility Functions ----------------

    def convert_to_grid_system(self, point):
        gx = round(point[0] / self.GRID_RESOLUTION) + self.USV_GRID_X
        gy = round(point[1] / self.GRID_RESOLUTION) + self.USV_GRID_Y
        return gx, gy

    def build_and_publish_occupancy_grid(self, msg, timestamp, dynamic_targets, static_targets, hard_coded_obstacles):
        """Constructs and populates the occupancy grid with dynamic and static repulsion fields."""
        msg.header.stamp = timestamp
        msg.header.frame_id = "usv/base_link"
        msg.info.resolution = self.GRID_RESOLUTION
        msg.info.width = self.GRID_WIDTH
        msg.info.height = self.GRID_HEIGHT
        msg.info.origin.position.x = -(self.USV_GRID_X * self.GRID_RESOLUTION)
        msg.info.origin.position.y = -(self.GRID_HEIGHT * self.GRID_RESOLUTION // 2)
        msg.info.origin.orientation.w = 1.0

        grid = np.zeros((self.GRID_HEIGHT, self.GRID_WIDTH), dtype='int8')

        # Add dynamic, static, and hard-coded obstacles with repulsion
        for point in dynamic_targets + static_targets + hard_coded_obstacles:
            gx, gy = self.convert_to_grid_system(point)
            if 0 <= gx < self.GRID_WIDTH and 0 <= gy < self.GRID_HEIGHT:
                for nx in range(-self.repulsion_range, self.repulsion_range + 1):
                    for ny in range(-self.repulsion_range, self.repulsion_range + 1):
                        x, y = gx + nx, gy + ny
                        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
                            grid[y, x] = 100

        # Add gradient for free cells
        for dy in range(self.GRID_WIDTH):
            for dx in range(self.GRID_HEIGHT):
                if grid[dy, dx] == 0:
                    grid[dy, dx] = 0.1 * dy

        msg.data = grid.flatten().tolist()
        return msg

    # ---------------- Callbacks ----------------

    def odometry_callback(self, msg):
        self.header = msg.header
        self.timesamp = msg.header.stamp.to_sec()
        self.boat_x, self.boat_y = msg.pose.pose.position.x, msg.pose.pose.position.y
        self.boat_psi = msg.pose.pose.position.z  # Note: psi taken from z position (project-specific hack)

    def processed_centroid_callback(self, msg):
        self.static_points.clear()
        self.static_points_rviz.clear()
        if msg.tracks:
            for i, target in enumerate(msg.tracks):
                if target.velocity < 1:  # treat as static obstacle
                    obstacle_global = [target.x_global, target.y_global, 1]
                    obstacle_local_x, obstacle_local_y, _, _ = global_to_local_tf(
                        self.boat_x, self.boat_y, self.boat_psi, [obstacle_global], 0
                    )
                    self.static_points.append([obstacle_local_x[0], obstacle_local_y[0]])
                    self.static_points_rviz.append([obstacle_local_x[0], -obstacle_local_y[0]])
            print(f"static targets = {self.static_points}")

    def raw_radar_points_callback(self, msg):
        raw_radar_points_flat = msg.data
        self.raw_radar_points = np.array(raw_radar_points_flat).reshape((len(msg.data) // 2), 2).tolist()
        return self.raw_radar_points

    def colliding_cpas_callback(self, msg):
        colliding_cpas = msg.data
        colliding_cpas_np = np.array(colliding_cpas).reshape((len(msg.data) // 3), 3)
        colliding_cpas_np = colliding_cpas_np[:, 1:]  # take only x, y
        colliding_cpas_np_rviz = colliding_cpas_np * np.array([1, -1])
        self.dynamic_objects = colliding_cpas_np.tolist()
        self.dynamic_objects_rviz = colliding_cpas_np_rviz.tolist()
        print(f"colliding_cpas = {self.dynamic_objects}")

    # ---------------- Grid Publisher ----------------

    def publish_grid(self, event):
        """Build and publish the occupancy grid with repulsion."""
        grid_msg = OccupancyGrid()
        timestamp = rospy.Time.now()

        # For calculations
        populated_grid = self.build_and_publish_occupancy_grid(
            grid_msg, timestamp, self.dynamic_objects, self.static_points, self.hard_coded_obstacles
        )
        self.grid_pub.publish(populated_grid)

        # For RViz visualization (y-flipped)
        populated_grid_rviz = self.build_and_publish_occupancy_grid(
            grid_msg, timestamp, self.dynamic_objects_rviz, self.static_points_rviz, self.hard_coded_obstacles_rviz
        )
        self.rviz_grid_pub.publish(populated_grid_rviz)


if __name__ == '__main__':
    try:
        # You can configure the grid here while launching
        OccupancyGridPublisher(grid_width=30, grid_height=30, grid_resolution=20, usv_grid_x=2, repulsion_range=3)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
