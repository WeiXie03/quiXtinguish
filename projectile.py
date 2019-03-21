import math
import matplotlib.pyplot as plt

#only acceleration after launch is due to gravity, in vertical direction
g = -9.8 #m*s^-2

class Projectile():
    def __init__(self, vi, theta, hi):
        theta = math.radians(theta)
        print('angle is {}*pi'.format(theta/math.pi))
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

def plt_graph(angles, hdisps):
    '''plot horizontal displacement over angle launched at'''
    #times and hdisps should be iterables
    plt.plot(angles, hdisps)
    plt.xlabel('angle(degrees)')
    plt.ylabel('horizontal distance(m)')
    plt.title('Effect of Angle Launched on Distance Hit for a Water Jet')
    plt.show()

def list_points(angles, hdisps):
    '''list out all horiz disps as a function of angles'''
    if len(angles) == len(hdisps):
        print('x-axis dataset ain\'t the same length as the y-axis one')
    else:
        print('(angle, horiz disp)')
        for ind in len(angles):
            print(angles[ind], hdisps[ind])

if __name__ == "__main__":
    #flow_rate = float(input('Flow rate in mL/s: '))
    #nozzle_radius = float(input('Radius of opening in nozzle(m): '))
    #nozzle_area = math.pi * nozzle_radius**2

    init_vel = 3.41588510611 #m/s
    #calculated from v=Q/A -> velocity = flow rate/area, measured flow rate with timer and grad cylinder, measured radius of nozzle with calipers
    init_height = float(input('Initial height lauched from in m: '))

    angles = [angle for angle in range(30)]
    #robot can tilt + and - 30 degrees, -30 degrees = 330 degrees
    print('tilt angle range is -30 to 30 degrees')

    projs = [Projectile(init_vel, angle, init_height) for angle in angles]
    hdisps = [proj.calc_hdisp() for proj in projs]

    #plot the graph
    plt_graph(angles, hdisps)
