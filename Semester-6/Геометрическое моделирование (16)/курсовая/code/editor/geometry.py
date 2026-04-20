import math

from .config import EPS


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def normalize_angle(deg):
    return deg % 360


def point_angle(center, point):
    # Tk Canvas uses a mathematical angle measured from the positive X axis.
    return normalize_angle(math.degrees(math.atan2(center[1] - point[1], point[0] - center[0])))


def angle_to_point(center, radius, deg):
    rad = math.radians(deg)
    return (center[0] + radius * math.cos(rad), center[1] - radius * math.sin(rad))


def ccw_sweep(start, end):
    return (end - start) % 360


def clockwise_sweep(start, end):
    return -((start - end) % 360)


def angle_on_ccw_arc(start, extent, test):
    return ccw_sweep(start, test) <= max(0, extent) + 0.001


def circle_from_three_points(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < EPS:
        return None

    ux = (
        (ax * ax + ay * ay) * (by - cy)
        + (bx * bx + by * by) * (cy - ay)
        + (cx * cx + cy * cy) * (ay - by)
    ) / d
    uy = (
        (ax * ax + ay * ay) * (cx - bx)
        + (bx * bx + by * by) * (ax - cx)
        + (cx * cx + cy * cy) * (bx - ax)
    ) / d
    center = (ux, uy)
    return center, distance(center, a)


def arc_from_three_points(a, b, c):
    circle = circle_from_three_points(a, b, c)
    if not circle:
        return None
    center, radius = circle
    start = point_angle(center, a)
    mid = point_angle(center, b)
    end = point_angle(center, c)
    extent_ccw = ccw_sweep(start, end)
    if angle_on_ccw_arc(start, extent_ccw, mid):
        extent = extent_ccw
    else:
        extent = clockwise_sweep(start, end)
    return center, radius, start, extent


def arc_points_from_three(a, b, c, steps=48):
    arc = arc_from_three_points(a, b, c)
    if not arc:
        return [a, c]
    center, radius, start, extent = arc
    count = max(8, int(abs(extent) / 8), steps)
    pts = []
    for i in range(count + 1):
        t = i / count
        pts.append(angle_to_point(center, radius, start + extent * t))
    return pts


def flatten(points):
    result = []
    for x, y in points:
        result.extend([x, y])
    return result


def rect_from_points(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def bbox_inside(inner, outer):
    return inner[0] >= outer[0] and inner[1] >= outer[1] and inner[2] <= outer[2] and inner[3] <= outer[3]


def bbox_intersects(a, b):
    return a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]

