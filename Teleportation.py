#%matplotlib inline
# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.tools.visualization import *
import qiskit
import random
import math
import cmath
# Loading your IBM Q account(s)
#provider = IBMQ.load_account()

class GameController:
    
    players = []

    def getRand(self):
        re = random.uniform(0, 10)
        return re

    def setUpEntanglement(self):
        #print("Setting Up enganglement!")
        for x in range(1, 2*self.n-1, 2):
            self.circuit.h(x+1)
            self.circuit.cx(x + 1, x) 
        self.circuit.barrier()

    def __init__(self, n):
        self.n = n
        self.backend = self.getBackend()
        q = qiskit.QuantumRegister(2*n-1)
        # Create a Classical Register with 2 bits.
        self.c0 = qiskit.ClassicalRegister(1)
        self.c1 = qiskit.ClassicalRegister(1)
        # Create a Quantum Circuit
        self.circuit = qiskit.QuantumCircuit(q, self.c0, self.c1)

        self.setUpEntanglement()

        self.su = 0
        res = 1
        print("Our random numbers are:")
        for x in range(n-1):
            a = self.getRand()
            print("\t{}".format(a))
            res *= cmath.exp(math.pi * complex(0,a))
            self.players.append(Player([2*x,2*x+1],a,None,self.circuit, self.c0,self.c1))
            self.su += a

        a = math.ceil(self.su) - self.su
        print("\t{}".format(a))
        res *= cmath.exp(math.pi * complex(0,a))
        self.players.append(Player([2*(n-1),2*(n-1)+1],a,None,self.circuit, self.c0,self.c1))
        self.su += a
        self.firstPlayer = self.players[0]
        
        for x in range(n-1):
            self.players[x].next = self.players[x + 1]
        
        print("They sum to: {}".format(self.su))
        print("The final phase should therefore be: {}\n\n".format(cmath.exp(complex(0,math.pi*self.su))))

        self.firstPlayer.start()
       
    def getBackend(self):
        # print local backends
        #print('Available AER backends:')
        #for backend in Aer.backends():
        #    print('    - %s' % backend)

        # load account
        IBMQ.enable_account('52e86bacfb9a8485be7c14754131913dd1690a936a9ce11d72e5c92ef98071396b9c0252ad3844016f4fe73ece05cae52e8564b1d849b2707288397b3248f263')
        #IBMQ.load_account()

        # check providers in account
        #print('Available IBMQ providers:')
        #for provider in IBMQ.providers():
        #    print('    - %s' % provider)
       # select provider and print backends
        provider = IBMQ.get_provider(hub='ibm-q')
        #print('Available backends:')
        #for backend in provider.backends():
        #    print('    - %s' % backend)

        # select a backend for the tutorial
        backend = Aer.get_backend('qasm_simulator')
        return backend

class Player:
    def __init__(self, qubits, alpha, next, circuit, cla0, cla1):
        self.qubits = qubits
        self.alpha = alpha
        self.next = next
        self.circuit = circuit
        self.c0 = cla0
        self.c1 = cla1

    def input(self, z1, z2):
        self.circuit.rx(math.pi * self.alpha, self.qubits[0])
        
        self.circuit.barrier()

        if self.next == None:
            #self.circuit.h(self.qubits[0])
            self.circuit.measure(self.qubits[0], self.c0)
            self.circuit.measure(self.qubits[0], self.c1)
            print("Reached the end - cirquit is now set up")
        else:
            self.circuit.cx(self.qubits[0],self.qubits[1])
            self.circuit.h(self.qubits[0])
            self.circuit.barrier()
            self.circuit.measure(self.qubits[0], self.c0)
            self.circuit.measure(self.qubits[1], self.c1)
            
            self.circuit.barrier()
            
            #self.circuit.cz(self.qubits[0],self.qubits[1]+1)
            #self.circuit.cx(self.qubits[1],self.qubits[1]+1)
            
            self.circuit.z(self.qubits[1]+1).c_if(self.c0,1)
            self.circuit.x(self.qubits[1]+1).c_if(self.c1,1)
            
            self.next.input(self.c0,self.c1)

    def start(self):
        self.prepareInitialState()
        self.input(self.c0,self.c1)

    def prepareInitialState(self):
        #self.circuit.h(self.qubits[0])
        print("preparation of circuit...")


n = 5
shots = 100

print("setting up a Game with {} players".format(n))

gc = GameController(n)

print("\n\nNow executing the circuit! \n({} times)".format(shots))
job = qiskit.execute(gc.circuit, gc.backend, shots=shots) 
result=job.result()
c = result.get_counts(gc.circuit)
print("\n\nRESULTS:\n")

if (gc.su % 2 == 0):
    print("the sum ({}) is EVEN so we expect the result [ '00' : {}]".format(gc.su, shots))
else:
    print("the sum ({}) is ODD so we expect the result [ '11' : {}]".format(gc.su, shots))
    
print("The Result is:")
print(c)
