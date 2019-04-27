import math
#import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
import csv

#only acceleration after launch is due to gravity, in vertical direction
g = 9.8 #m*s^-2

def calc_init_vel(vol=901, time=6.04, outer_dia=7.1, inner_dia=6.45):
    #volume mL, time sec, radii mm

    #v=Q/A; velocity = flow rate/area
    flow_rate = vol/(10**6 * time)

    outer_r = outer_dia/(2*10**3)
    #measured diameter in millimeters
    inner_r = inner_dia/(2*10**3)
    opening_area = math.pi*(outer_r**2-inner_r**2)

    vi = flow_rate/opening_area
    return vi

#def calc_init_vel(angle, hdisp, both):

class Projectile():
    #measured flow rate with timer and grad cylinder, measured radius of nozzle with calipers
    vi = calc_init_vel(901, 6.04, 7.1, 6.45)
    hi = 0.29 #m

    def __init__(self, theta, fire_height):
        theta = math.radians(theta)
        #print('angle is {}*pi'.format(theta/math.pi))
        self.vix, self.viy = Projectile.vi*math.cos(theta), Projectile.vi*math.sin(theta)
        self.hfire = fire_height

    def calc_hdisp(self):
        '''calculate and return horizontal displacement given init variables'''
        #solving for time t using: a/2*t^2 + viy*t + diy = 0, derived from d = vi*t + a(t^2)/2
        discriminant = self.viy**2 + 2*g*(Projectile.hi-self.hfire)
        #path of projectile is parabola, two x-intercepts exist, only want x-intercept farther than starting x position in positive x direction
        time = max((self.viy + discriminant**0.5)/g, (self.viy - discriminant**0.5)/g)

        #horiz. disp. = horizontal velocity * time, horizontal velocity doesn't change; no friction, air resistance, etc.
        return time*self.vix

def plt_graph(angles, hdisps, fmt=None, label=''):
    '''plot horizontal displacement over angle launched at'''
    #angles and hdisps should be iterables

    if fmt:
        #for experimental data: format will be scatter points
        plt.plot(angles, hdisps, fmt)

        #line of best fit
        b, m = polyfit(angles, hdisps, 1)
        fit_disps = [b + m*angle for angle in angles]
        plt.plot(angles, fit_disps, label=label)
    else:
        #if not experimental(uses default format of straight line)
        plt.plot(angles, hdisps, label=label)

    plt.xlabel('angle(degrees)')
    plt.ylabel('horizontal distance(m)')
    plt.legend()
    plt.title('Effect of Angle Launched on Distance Hit for a Water Jet')

def list_points(angles, hdisps):
    '''list out all horiz disps as a function of angles'''
    if len(angles) != len(hdisps):
        print('x-axis dataset ain\'t the same length as the y-axis one')
    else:
        print('(angle, horiz disp)')
        for ind in len(angles):
            print(angles[ind], hdisps[ind])

def load_dat(dataf_path):
    with open(dataf_path, 'r') as dataf:
        angles, hdists = [], []
        data = csv.DictReader(dataf)
        for row in data:
            #0 is neutral in this case
            angle = float(row["angle(deg)"]) - 90
            dist = float(row["horizontal distance(m)"])
            print('{} deg, {} m'.format(angle, dist))

            angles.append(angle)
            hdists.append(dist)
        return angles, hdists

if __name__ == "__main__":
    DATA_PATH = "projectile_experimental.csv"
    #load experimental data from spreadsheet
    experi_dat = load_dat(DATA_PATH)
    plt_graph([-ang for ang in experi_dat[0]], experi_dat[1], 'bo', 'experimental')

    Projectile.hi = float(input('Initial height lauched from in cm: '))/100.0

    angles = [angle for angle in range(-20, 25)]
    #robot can tilt + and - ~20 to 26 degrees
    print('tilt angle range assumed to be -20 to 25 degrees')

    #calculate horiz disp for projectiles at a lot of initial angles
    projs = [Projectile(angle, 0) for angle in angles[::-1]]
    hdisps = [proj.calc_hdisp() for proj in projs]

    #plot the graph
    plt_graph(angles[6:], hdisps[6:], label='prediction')

    plt.show()
