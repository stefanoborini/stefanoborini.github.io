# Bacteria, a program to test natural selection on cybernetic bacteria
# License: MIT
# Author: Stefano Borini
# Website : http://forthescience.org
# Note: Don't take the design of this code as a measure of my design skills. it sucks.

import copy
import random
import sys

def floatrange(start, stop, n_intervals):
    diff = stop - start
    for i in xrange(n_intervals+1):
        yield start + (i*diff)/n_intervals

ALL_CODONS = ["IncA",  "IncX" , "LoadA", "LoadX", "LoadY", "AddYtoA", "MoveAtoY", "BranchXZero", "BranchXNotZero", "Return"]


def generateRandomCodon():
    opcode = random.choice(ALL_CODONS)
    if opcode in ["AddYtoA", "MoveAtoY", "Return"]:
        return (opcode, None)
    else:
        return (opcode, random.randint(-5,5))
    

class Bacterium(object):
    def __init__(self,gencode=None):
        """Initializes a Bacterium, defining a random genetic code for it"""
        self._x = 0
        self._y = 0
        self._a = 0
        self._genetic_code=[]

        # while executing the genetic code, keeps track of the current position in the code chain
        self._pc = 0 

        # so that we don't re-compute a value if we already computed the answer before.
        self._cache = {} 

        if gencode is None:
            # no genetic code has been provided. so we generate one
            opnum=random.randint(2,50)
            print "allocating bacterium with "+str(opnum)+" codons"
            for i in xrange(0,opnum):
                self._genetic_code.append(generateRandomCodon())
        else:
            # copy it in. 
            for i in xrange(0,len(gencode)):
                self._genetic_code.append(copy.deepcopy(gencode[i]))


        
    def feed(self,val):
        """Feeds the bacterium with mathematical food and returns a metabolism product after being processed
        by its genetic code."""
        # if we already computed the value, just return it
        if self._cache.has_key(val):
            return self._cache[val]

        # initialize the A register to the feed value, and all the other registers to zero.
        self._a = val
        self._x = 0
        self._y = 0
        self._pc = 0
        self._returned = False

        # to prevent infinite loops, we limit the number of executed codons. When the limit is reached, we return
        # what we have, no matter what.
        counter = 0  

        if len(self._genetic_code) == 0:
            self._returned = True
            self._cache[val] = self._a
            return self._a

        # here start the digestion
        while True:
            codon = self._genetic_code[self._pc]
            getattr(self, "_handle_"+codon[0])(codon[1])

            self._pc = self._pc + 1
            counter = counter + 1
            if counter > 50:
                # we executed more than 50 operations, we bail out with what we have to prevent infinite loops
                return self._a

            if self._pc < 0:
                # we jumped before the beginning of the genetic code (via a Branch). we set it to the start
                self._pc = 0
            elif self._pc >= len(self._genetic_code) or self._returned:
                # we jumped beyond the end of the genetic code, or the Return execution occurred (flagged by self.returned)
                self._cache[val] = self._a
                return self._a
        
    def mutate(self):
        """Randomly mutates the genetic code of the bacterium"""
       
        mutations=random.randint(1,5)

        for i in xrange(0,mutations):
            if len(self._genetic_code) == 0:
                continue
            mutation_type = random.choice(["substitution","deletion","insertion"])

            if mutation_type == "substitution": 
                v = random.randint(0,len(self._genetic_code)-1)
                self._genetic_code[v] = generateRandomCodon()
            elif mutation_type == "deletion":
                v = random.randint(0,len(self._genetic_code)-1)
                del self._genetic_code[v]
            elif mutation_type == "insertion":
                v = random.randint(0,len(self._genetic_code)-1)
                self._genetic_code.insert(v, generateRandomCodon())
                


    def geneticCode(self):
        return self._genetic_code

    # routines to handle the genetic code operations.
    def _handle_IncA(self,val):
        self._a = self._a + val
    def _handle_IncX(self,val):
        self._x = self._x + val
    def _handle_LoadA(self,val):
        self._a = val
    def _handle_LoadX(self,val):
        self._x = val
    def _handle_LoadY(self,val):
        self._y = val
    def _handle_AddYtoA(self,val):
        self._a = self._a + self._y
    def _handle_MoveAtoY(self,val):
        self._y = self._a
    def _handle_BranchXZero(self,val):
        if self._x == 0:
            self._pc = self._pc+val
    def _handle_BranchXNotZero(self,val):
        if self._x != 0:
            self._pc = self._pc+val
    def _handle_Return(self,val):
        self._returned = True


class Environment(object):
    """Keeps all the bacteria, feeds them, sets the rules for their survival"""

    def __init__(self):
        self._all_bacteria=[]
        self._conditions = []
        for i in xrange(1,2000):
            self._all_bacteria.append(Bacterium())

    def setConditions(self,conditions):
        self._conditions = conditions

    def _reaping(self, tolerance):
        """Kills the poor bacteria"""
        nextgen = []
        for bacterium in self._all_bacteria:
            score = 0.0
            for substrate, expected_product in self._conditions:
                score = score + (abs(float(bacterium.feed(substrate)) - float(expected_product))/abs(float(expected_product)))
            if (score/float(len(self._conditions)) <= float(tolerance)) \
                and random.random()*50 > float(len(bacterium.geneticCode())):
                nextgen.append(bacterium)

        self._all_bacteria=nextgen
    def _averageScore(self):
        scores = []
        for bacterium in self._all_bacteria:
            score = 0.0
            for substrate, expected_product in self._conditions:
                score = score + (abs(float(bacterium.feed(substrate)) - float(expected_product))/abs(float(expected_product)))
            scores.append(score/float(len(self._conditions)))
       
        return sum(scores)/len(scores)

    def _duplication(self):
        """Allows bacteria to duplicate and mutate"""
        new_bacteria=[]

        for c in self._all_bacteria:
            new_bacterium = Bacterium(copy.deepcopy(c.geneticCode()))
            new_bacterium.mutate()
            new_bacteria.append(new_bacterium)

        # we want to keep the pool of bacteria high, so we add more so to fill the pool
        available_slots = 4000-len(self._all_bacteria)
        for i in xrange(available_slots):
            new_bacterium = random.choice(new_bacteria)
            self._all_bacteria.append(new_bacterium)
        print len(self._all_bacteria)

    def epoch(self,start_tolerance, stop_tolerance, num_generations):
        """An epoch is a given number of generations. During an epoch the tolerance for the conditions gets progressively
        stricter"""
        generation = 1
        for tolerance in floatrange(start_tolerance, stop_tolerance, num_generations):
            self._duplication()
            print "Generation "+str(generation)+" Tolerance : "+str(tolerance)+" Average Score : "+str(self._averageScore())
            self._reaping(tolerance)
            if len(self._all_bacteria) == 0:
                print "Rock falls. Everybody dies."
                sys.exit(0)
            print "after reaping : "+str(len(self._all_bacteria))+" Average Score : "+str(self._averageScore())+" Average Length : "+str(sum(map(lambda x: len(x.geneticCode()), self._all_bacteria))/len(self._all_bacteria))

            generation = generation + 1
            self.storeBacteria(str(generation))
            
    def report(self):
        print "Final Report"
        print "------------"
        print "Average length : ", sum(map(lambda x: len(x.geneticCode()), self._all_bacteria))/len(self._all_bacteria)
        counting = []
        for codon_pos in xrange(0,50):
            counting.append({})
            for bacterium in self._all_bacteria:
                try:
                    codon = bacterium.geneticCode()[codon_pos]
                    counting[codon_pos][codon] = counting[codon_pos].get(codon,0) + 1
                except:
                    pass
            
        for codon_pos in xrange(0,50):
            print str(codon_pos)+" : "+str(sorted(counting[codon_pos].items(), cmp=lambda x,y : cmp(x[1],y[1]), reverse=True)[0:3])

        self.storeBacteria("end")
    def storeBacteria(self, label):
        f=file("gencode"+label+".txt","w")
        for c in self._all_bacteria:
            f.write(str(c.geneticCode())+"\n")

        f.close()
        
random.seed(10)

e=Environment()
e.setConditions([(0,7),(2,11),(4,15),(5,17)])
e.epoch(1.0,0.0, 20)
e.report()
