import math
from .spectrum import linear_interpolate, build_spectrum

def average_intersections(intersections, capacity, demand):
    if len(intersections) < 3:
        if intersections[0]['acc'] == 0:
            return intersections[1]
        elif intersections[1]['acc'] == 0:
            return intersections[0]
        else:
            return intersections[1]

    first_point = intersections[0]
    second_point = intersections[1]
    third_point = intersections[2]

    capacity_seg1 = chop_curve(capacity,
            first_point['disp'], second_point['disp'], 'disp', 'acc')
    capacity_seg2 = chop_curve(capacity,
            second_point['disp'], third_point['disp'], 'disp', 'acc')

    demand_seg1 = chop_curve(demand,
            first_point['disp'], second_point['disp'], 'disp', 'acc')
    demand_seg2 = chop_curve(demand,
            second_point['disp'], third_point['disp'], 'disp', 'acc')

    capacity_area1 = get_area_under_curve(capacity_seg1, 'disp', 'acc')
    capacity_area2 = get_area_under_curve(capacity_seg2, 'disp', 'acc')
    demand_area1 = get_area_under_curve(demand_seg1, 'disp', 'acc')
    demand_area2 = get_area_under_curve(demand_seg2, 'disp', 'acc')

    area_diff1 = abs(capacity_area1 - demand_area1)
    area_diff2 = abs(capacity_area2 - demand_area2)

    x_difference = third_point['disp'] - first_point['disp']

    if area_diff1 > area_diff2:
        adjust_percentage = area_diff2 / (area_diff1 + area_diff2)
        performance_point_disp = first_point['disp'] + (x_difference * adjust_percentage)
    else:
        adjust_percentage = area_diff1 / (area_diff1 + area_diff2)
        performance_point_disp = third_point['disp'] - (x_difference * adjust_percentage)

    performance_point = find_point_on_curve(performance_point_disp,
            capacity, 'disp', 'acc')

    return performance_point

def chop_curve(curve, start_val, stop_val, x='x', y='y'):
    idx = 0
    chopped_curve = []
    for point in curve:
        if point[x] == start_val:
            chopped_curve += [point]
        elif point[x] > start_val and point[x] < stop_val:
            if idx > 0 and len(chopped_curve) == 0:
                # interpolate to get the right value
                chopped_curve += [
                    {
                        'acc': linear_interpolate(start_val, curve[idx - 1], curve[idx], x, y),
                        'disp': start_val
                    },
                    point
                ]
            else:
                chopped_curve += [point]
        
        elif point[x] > stop_val:
            # interpolate final point
            chopped_curve += [
                {
                    'acc': linear_interpolate(stop_val, curve[idx - 1], curve[idx], x, y),
                    'disp': stop_val
                }
            ]
            return chopped_curve

        idx += 1
    return chopped_curve

def find_point_on_curve(x_val, curve, x = 'x', y = 'y'):
    point = {
        x: x_val,
        y: None
    }

    for idx in range(len(curve)):
        if curve[idx][x] > x_val:
            if idx > 0:
                point[y] = linear_interpolate(x_val, curve[idx-1], curve[idx], x, y)
            else:
                point[y] = linear_interpolate(x_val, curve[idx], curve[idx + 1], x, y)
        
            return point

    return None

def get_area_under_curve(curve, x='x', y='y'):
    '''
    Integrates a curve of discrete values
    '''
    x_vals = [curve[0][x] + x_int * .1 for x_int in range(0, int((curve[-1][x] - curve[0][x]) * 10))]
    x_vals += [curve[-1][x]]
    expanded_curve = build_spectrum(curve, x_vals, x=x, y=y)

    total_area = 0
    for idx in range(len(expanded_curve) - 1):
        p1 = expanded_curve[idx]
        p2 = expanded_curve[idx + 1]

        area = (p2[x] - p1[x]) * p2[y]
        total_area += area

    return total_area


def get_performance_point(capacity, demand):
    intersections = find_intersections(capacity, demand, 'disp', 'acc')

    # calculate periods for intersections
    for intersection in intersections:
        if intersection['acc'] != 0:
            period = math.sqrt(intersection['disp'] / intersection['acc'] /  9.779738)
            intersection['period'] = round(period*100) / 100
        else:
            intersection['period'] = 0

    if len(intersections) == 1:
        performance_point = intersections[0]
    elif len(intersections) > 1:
        performance_point = average_intersections(intersections, capacity, demand)
    else:
        performance_point = {
            'disp': 0,
            'acc': 0
        }

    return performance_point

    # determine performance point from multiple intersections
  
def find_intersections(line1, line2, x='x', y='y'):
    intersections = []
    line1_idx = 0
    line2_idx = 0
    while line1_idx < len(line1) - 1 and line2_idx < len(line2) - 1:
        seg1 = [line1[line1_idx], line1[line1_idx + 1]]
        seg2 = [line2[line2_idx], line2[line2_idx + 1]]
        
        intersection = get_intersection(seg1, seg2, x, y)
        if intersection is not False:
            # make sure this point isn't already in the array
            x_vals = [p[x] for p in intersections]
            if intersection[x] not in x_vals:
                intersections += [intersection]
        
        if seg1[1][x] == seg2[1][x]:
            line1_idx += 1
            line2_idx += 1
        elif seg1[1][x] < seg2[1][x]:
            line1_idx += 1
        else:
            line2_idx += 1

    return intersections

def get_intersection(seg1, seg2, x, y):
    '''
    seg1 and seg2 are 2d arrays 
    [ {x: x1_val,  y: y1_val}, {x: x2_val, y: y2_val} ]
    '''
    dx1 = seg1[1][x] - seg1[0][x]
    dx2 = seg2[1][x] - seg2[0][x]
    dy1 = seg1[1][y] - seg1[0][y]
    dy2 = seg2[1][y] - seg2[0][y]

    # check for parallel segs
    if (dx2 * dy1 - dy2 * dx1) == 0:
        # The segments are parallel.
        return False
    
    s = ((dx1 * (seg2[0][y] - seg1[0][y]) + dy1 * (seg1[0][x] - seg2[0][x])) /
                (dx2 * dy1 - dy2 * dx1))
    t = ((dx2 * (seg1[0][y] - seg2[0][y]) + dy2 * (seg2[0][x] - seg1[0][x])) /
                (dy2 * dx1 - dx2 * dy1))
    
    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        x_val = abs(round((seg1[0][x] + t * dx1) * 1000) / 1000)
        y_val = abs(round((seg1[0][y] + t * dy1) * 1000) / 1000)
        return {x: x_val, y: y_val}
    else:
      return False
