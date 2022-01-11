from simulation.qw import *

if __name__ == '__main__':
    # qw = GroverWalk2D()
    qw = EraseElectricHadamardWalk2DAlongX(erase_t_list=[10, 50, 100])
    qw.simulate(start_step_t=0)
