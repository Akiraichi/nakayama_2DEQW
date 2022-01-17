from simulation.qw import *

if __name__ == '__main__':
    indexes = list(range(16, 256, 15))
    qw = ElectricGroverWalk2DAlongX()
    qw.simulate()
