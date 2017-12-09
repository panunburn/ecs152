"""Binary Exponetial and Linear Backoff Algorithm"""

#The program automatically generates the results of both algorithm"""
# usage: python backoff-algorithm-analysis.py
#  Weiran Guo(912916431)
#  Siqi Pi(912421900)

import random
import simpy
import math

RANDOM_SEED = 29
SIM_TIME = 1000000
MU = 1
TS = 1 #time slot
N_HOST = 10 #number of hosts

""" Host class """
class Host:
    def __init__(self, env, arrival_rate):
        self.env = env
        self.arrival_rate = arrival_rate
        self.L = 0
        self.S = 0
        #self.arrives = 0
        self.N = 0 #times retransmitted
        self.server = simpy.Resource(env, capacity = 1)
        env.process(self.packets_arrival(env))
        
    def packets_arrival(self, env):
        while True:
            yield env.timeout(random.expovariate(self.arrival_rate))
            #self.arrives += 1
            if (self.L == 0): #no packet in the queue
                self.S = math.floor(env.now) + 1
                self.N = 0
            self.L += 1
        
    def process_packet(self, env):
        self.L -= 1
        if (self.L > 0):
            self.N = 0
            self.S = math.floor(env.now) + 1
    
    def exp_backoff(self, env):
        r = min(self.N, N_HOST)
        self.S = math.floor(env.now + random.randint(0,2**r)*TS) + 1
        self.N += 1
        
    def linear_backoff(self, env):
        K = min(self.N, 1024)
        self.S = math.floor(env.now + random.randint(0, K)*TS) + 1
        self.N += 1

""" Queue system  """		
class Ethernet:
    def __init__(self, env, arrival_rate, Type):
        self.env = env
        self.hosts = [Host(env, arrival_rate) for i in range(N_HOST)]
        self.success = 0
        self.collide = 0
        self.blank = 0
        self.Type = Type 
        self.arrival_rate = arrival_rate

    def sim(self, env):
        while True:
            hostLst = []
            for host in self.hosts:
                if (host.L > 0 and (host.S == math.floor(env.now))):#host is requesting now
                    hostLst.append(host)
            #print(len(hostLst))
            if (len(hostLst) == 1):#succeed
                hostLst[0].process_packet(env)
                self.success += 1
            elif (len(hostLst) > 1):#collide
                self.collide += 1
                for host in hostLst:
                    if (self.Type == 0):#exponetial
                        host.exp_backoff(env)
                    else:
                        host.linear_backoff(env)
            else:
                self.blank += 1
            yield self.env.timeout(TS)
                

def main():
	print("Ethernet system model:mu = {0}, Ts = {1}, N = {2}".format(MU, TS, N_HOST))

	random.seed(RANDOM_SEED)
	for Type in [0,1]:
		if (Type == 0):
			print ("For Exponetial Backoff Algorithm")
		else:
			print ("For Linear Backoff Algorithm")
		print ("{0:<9} {1:<9} {2:<9} {3:<9} {4:<9}".format(
			"Lambda", "Success", "Failed","Blank", "Throughput"))
		for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:
			env = simpy.Environment()
			ethernet = Ethernet(env, arrival_rate, Type)
			env.process(ethernet.sim(env))
			env.run(until=SIM_TIME)
			#for i in range(10):
				#print(ethernet.hosts[i].arrives)
			#print(total)
			print ("{0:<9.3f} {1:<9} {2:<9}{3:<9} {4:<9.5f}".format(
				arrival_rate,
				ethernet.success,
				ethernet.collide,
				ethernet.blank,
				ethernet.success/SIM_TIME))
	
if __name__ == '__main__': main()

