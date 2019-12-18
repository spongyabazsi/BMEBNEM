import math
from pomegranate import *
import random as rando

def generate():
    gendata = []
    for i in range(1,100):
        newnode = []
        for j in range (0,5):
            rand = rando.random()
            if rand > 0.5:
                newnode.append('H')
            else:
                newnode.append('I')

        gendata.append(newnode)
    return gendata
def EMpredictor(network, data):
    incompletedata = []

    for k in range(1,10):
        node = []
        for i in range(1,6):
            rand = rando.random()
            if rand > 0.5:
                node.append('H')
            else:
                node.append('I')
            if i == 5:
                which = rando.randrange(5)
                node[which] = None
                print(node)
                incompletedata.append(node)
    for x in range(0, 9):
        hid = network.predict(incompletedata)
        print(hid[x:x+1])
    print("egyesevel")
    for x in range(0, 9):
        hid = network.predict(incompletedata[x:x + 1])
        print(hid[0])
        data.append(hid[0])
        network.fit(data)




if __name__ == '__main__':
    breakin = DiscreteDistribution({'I': 1. / 1000, 'H': 1-1. / 1000})
    earthquake = DiscreteDistribution({'I': 2. / 1000, 'H': 1-2. / 1000})
    alarm = ConditionalProbabilityTable(
        [['I', 'I', 'I', 0.95],
         ['I', 'H', 'I', 0.94],
         ['H', 'I', 'I', 0.29],
         ['H', 'H', 'I', 0.001],
         ['I', 'I', 'H', 0.05],
         ['I', 'H', 'H', 0.06],
         ['H', 'I', 'H', 0.71],
         ['H', 'H', 'H', 0.999]
         ], [breakin, earthquake])
    maria = ConditionalProbabilityTable(
        [['I','I',0.7],
         ['I','H',0.3],
         ['H','I',0.01],
         ['H','H',0.99]], [alarm])
    joseph = ConditionalProbabilityTable(
        [['I','I',0.9],
         ['I','H',0.1],
         ['H','I',0.05],
         ['H','H',0.95]], [alarm])
    s1 = State(breakin, name="Breakin")
    s2 = State(earthquake, name="Earthquake")
    s3 = State(alarm, name="Alarm")
    s4 = State(maria, "Maria")
    s5 = State(joseph, "Joseph")
    network = BayesianNetwork("test")
    network.add_states(s1, s2, s3, s4, s5)
    network.add_transition(s1, s3)
    network.add_transition(s2, s3)
    network.add_transition(s3,s4)
    network.add_transition(s3,s5)
    network.bake()
    print ("\t".join([state.name for state in network.states]))
    observations = {'Earthquake': 'I','Maria': 'I', 'Alarm': 'H', 'Breakin': 'H' }
    beliefs = map(str, network.predict_proba(observations))

    data = generate()
    network.fit(data)
    print(alarm)
    EMpredictor(network,data)
    print(alarm)
