import math
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
import csv

#only acceleration after launch is due to gravity, in vertical direction
g = -9.8 #m*s^-2

class Projectile():
    def __init__(self, vi, theta, hi):
        theta = math.radians(theta)
        #print('angle is {}*pi'.format(theta/math.pi))
        self.vix, self.viy = vi*math.cos(theta), vi*math.sin(theta)
        #self.vi = vi
        self.diy = hi

    def calc_hdisp(self):
        '''calculate and return horizontal displacement given init variables'''
        #solving for time t using: a/2*t^2 + viy*t + diy = 0, derived from d = vi*t + a(t^2)/2
        discriminant = self.viy**2 - 4 * g/2 * self.diy
        denom = g # =(2g)/2
        time = ((discriminant**0.5-self.viy)/denom, (-(discriminant**0.5)-self.viy)/denom)
        #path of projectile is parabola, two x-intercepts exist, only want x-intercept farther than starting x position in positive x direction
        #print('time can be {}, picking {}'.format(time, max(time)))
        time = max(time)

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
    plt_graph(load_dat(DATA_PATH)[0], load_dat(DATA_PATH)[1], 'bo', 'experimental')

    #flow_rate = float(input('Flow rate in mL/s: '))
    #nozzle_radius = float(input('Radius of opening in nozzle(m): '))
    #nozzle_area = math.pi * nozzle_radius**2

    init_vel = 3.16475986 #m/s
    #calculated from v=Q/A -> velocity = flow rate/area, measured flow rate with timer and grad cylinder, measured radius of nozzle with calipers
    init_height = float(input('Initial height lauched from in cm: '))/100.0

    angles = [angle for angle in range(-20, 25)]
    #robot can tilt + and - 30 degrees, -30 degrees = 330 degrees
    print('tilt angle range is -30 to 30 degrees')

    #calculate horiz disp for projectiles at a lot of initial angles
    projs = [Projectile(init_vel, angle, init_height) for angle in angles]
    hdisps = [proj.calc_hdisp() for proj in projs]

    #plot the graph
    plt_graph(angles, hdisps, label='prediction')

    plt.show()
