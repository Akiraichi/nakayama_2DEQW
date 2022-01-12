from simulation.qw import *

if __name__ == '__main__':
    qw = EraseElectricGroverWalk2DAlongX(erase_t_list=list(range(101,201)))
    qw.simulate(start_step_t=0)
