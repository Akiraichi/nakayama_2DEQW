from simulation.qw import *

if __name__ == '__main__':
    indexes = list(range(16,156,15))
    qw = EraseElectricHadamardWalk2DAlongX(erase_t_list=indexes)
    # qw = GroverWalk2D()
    # qw = ElectricGroverWalk2DAlongX()
    # qw = ElectricHadamardWalk2DAlongXY()
    qw.simulate(t_of_load=0)
