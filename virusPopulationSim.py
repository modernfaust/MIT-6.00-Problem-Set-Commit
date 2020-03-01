#Problem Set 12
#Monte carlo virus population simulator with matplotlib graphs

import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import pylab


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        if random.random() <= self.clearProb:
            return True
        return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() <= self.maxBirthProb*(1-popDensity):
            return SimpleVirus(self.maxBirthProb,self.clearProb)
        raise NoChildException('This virus particle does not reproduce')
        #do we have to return a NoChildException?
        
class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.population_density = 0.
        
    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return len(self.viruses)
    
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        virus_list = self.viruses
        
        for virus in virus_list:
            if virus.doesClear():
                virus_list.remove(virus)
        self.viruses = virus_list
        self.population_density = len(self.viruses)/ self.maxPop
        
        
        for virus in virus_list:
            try: self.viruses.append(virus.reproduce(self.population_density))
            except:pass
        
        return self.getTotalPop()         
        
        
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    virus_list = []
    time = 300
    virus_pop = []
    for i in range (100):
        virus_list.append(SimpleVirus(0.1,0.05))
    test_patient = SimplePatient(virus_list,1000)
    for time in range (time):
        virus_pop.append(test_patient.update())
    x_axis = np.arange(time+1)
    plt.plot(x_axis,virus_pop)
    plt.axis([0,time+(time/4),0,max(virus_pop)+(max(virus_pop)/8)])
    plt.xlabel("Number of Timesteps")
    plt.ylabel("Total Virus Population")
    plt.title("Total Virus Population and Time")
#   
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        try:
            return self.resistances[drug]
        except:
            print("Drug does not exist in dictionary")
            
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        
        inherit_resistance = {}
        for drug in activeDrugs:
            if not self.getResistance(drug):
                raise NoChildException()
        if random.random() <= self.maxBirthProb*(1-popDensity):
            for resistance in self.resistances:
                if random.random() <= 1-self.mutProb:
                    inherit_resistance[resistance]=self.resistances[resistance]
                else:
                    inherit_resistance[resistance] = not self.resistances[resistance]
            return ResistantVirus(self.maxBirthProb,self.clearProb,inherit_resistance,self.mutProb)
        raise NoChildException('This virus particle does not reproduce')
        
        #if patient is not resistant to 1 drug, then the virus repopulates
                
            
class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.activeDrugs = []
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)
        
    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.activeDrugs
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        population = 0
        count = 0
        
        for virus in self.viruses:
            for drugs in drugResist:
                if virus.getResistance(drugs):
                    count+=1
            if count == len(drugResist):
                population+=1
        return population
        
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        virus_list = self.viruses
        new_viruses = []
        
        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                self.population_density = self.getTotalPop() / self.maxPop
                try: new_viruses.append(virus.reproduce(self.population_density,self.activeDrugs))
                except NoChildException:
                    pass
        self.viruses = self.viruses+new_viruses
        return self.getTotalPop()  
#        self.population_density = self.getTotalPop() / self.maxPop

#        for virus in virus_list:
#            self.population_density = self.getTotalPop() / self.maxPop
#            try: self.viruses.append(virus.reproduce(self.population_density,self.activeDrugs))
#            except:pass
#        
#        return self.getTotalPop()  
#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    virus_list = []
    resistances = {'guttagonol':False}
    time = 300
    virus_pop = []
    for i in range(100):
        virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
    test_patient = Patient(virus_list,1000)
    for k in range (time//2):
        virus_pop.append(test_patient.update())
    test_patient.addPrescription('guttagonol')
    for k in range (time//2):
        virus_pop.append(test_patient.update())
    x_axis = np.arange(time)
    plt.plot(x_axis,virus_pop)
    plt.axis([0,time+(time/4),0,max(virus_pop)+(max(virus_pop)/8)])
    plt.xlabel("Number of Timesteps")
    plt.ylabel("Total Resistant Virus Population")
    plt.title("Total Guttagonol Resistant Virus Population and Time")
#
# PROBLEM 5
#
        
def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    resistances = {'guttagonol':False}
    #time = 300
    virus_pop_1 = []
    virus_pop_2 = []
    virus_pop_3 = []
    virus_pop_4 = []
    num_patients = 100
    total_viruses = 0
#    for i in range(100):
#        virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
    
    for p in range (num_patients):
        virus_list = []
        for i in range(100):
            virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
########RUN FOR DELAY OF 300
        test_patient_1 = Patient(virus_list,1000)
        for k in range (450):
            total_viruses = test_patient_1.update()
            if k == 300:
                test_patient_1.addPrescription('guttagonol')
        virus_pop_1.append(total_viruses)
        total_viruses = 0
        
#########RUN FOR DELAY OF 150
#        test_patient_2 = Patient(virus_list,1000)
#        for k in range (300):
#            total_viruses=(test_patient_2.update())
#            if k == 150:
#                test_patient_2.addPrescription('guttagonol')
#        virus_pop_2.append(total_viruses)
#        print("Patient:",p,"has", total_viruses)
#        total_viruses = 0
#        
##########RUN FOR DELAY OF 75
#        test_patient_3 = Patient(virus_list,1000)
#        for k in range (225):
#            virus_pop_3.append(test_patient_3.update())
#            if k == 75:
#                test_patient_3.addPrescription('guttagonol')
#        virus_pop_3.append(total_viruses)
#        total_viruses = 0
#        
#        
#########RUN FOR DELAY OF 0
#        test_patient_4 = Patient(virus_list,1000)
#        for k in range (150):
#            virus_pop_4.append(test_patient_4.update())
#            if k == 0:
#                test_patient_4.addPrescription('guttagonol')
#        virus_pop_4.append(total_viruses)
#        total_viruses = 0
        
    plt.figure()
    plt.hist(virus_pop_1)
    plt.xlabel('Final Total Virus Populations')
    plt.ylabel('Number of Patients')
    plt.title("100 Patients: Total Guttagonol Resistant Virus Population delay 300")
#    plt.hist(virus_pop_2,label = 'Delay: 150')
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Guttagonol Resistant Virus Population delay 150")
#    plt.hist(virus_pop_3,label = 'Delay: 75')
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Guttagonol Resistant Virus Population delay 75")
##    plt.hist(virus_pop_4, label = 'Delay: 0')
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Guttagonol Resistant Virus Population delay 0")
    plt.show()

#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    resistances = {'guttagonol':False,'grimpex':False}
    virus_pop_1 = []
    virus_pop_2 = []
    virus_pop_3 = []
    virus_pop_4 = []
    time_1 = 150+300+150
    time_2 = 150+150+150
    time_3 = 150+75+150
    time_4 = 150+0+150
    num_patients = 100
    num_viruses = 100
    total_viruses = 0
#    for i in range(100):
#        virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
    
    for p in range (num_patients):
        virus_list = []
        for i in range(num_viruses):
            virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
########RUN FOR DELAY OF 300
#        test_patient_1 = Patient(virus_list,1000)
#        for k in range (time_1):
#            if k == 150:
#                test_patient_1.addPrescription('guttagonol')
#            if k == 450:
#                test_patient_1.addPrescription('grimpex')
#            total_viruses = test_patient_1.update()
#        virus_pop_1.append(total_viruses)
#        total_viruses = 0
        
########RUN FOR DELAY OF 150
        test_patient_2 = Patient(virus_list,1000)
        for k in range (time_2):
            if k == 150:
                test_patient_2.addPrescription('guttagonol')
            if k == 300:
                test_patient_2.addPrescription('grimpex')            
            total_viruses=(test_patient_2.update())
        virus_pop_2.append(total_viruses)
        print("Patient:",p,"has", total_viruses)
        total_viruses = 0
#        
###########RUN FOR DELAY OF 75
#        test_patient_3 = Patient(virus_list,1000)
#        for k in range (time_3):
#            if k == 150:
#                test_patient_3.addPrescription('guttagonol')
#            if k == 225:
#                test_patient_3.addPrescription('grimpex')  
#            virus_pop_3.append(test_patient_3.update())
#        virus_pop_3.append(total_viruses)
#        total_viruses = 0
#        
#        
#########RUN FOR DELAY OF 0
#        test_patient_4 = Patient(virus_list,1000)
#        for k in range(time_4)
#            if k == 150:
#                test_patient_4.addPrescription('guttagonol')
#                test_patient_4.addPrescription('grimpex')  
#            if k == 0:
#                test_patient_4.addPrescription('guttagonol')
#        virus_pop_4.append(total_viruses)
#        total_viruses = 0
        
    plt.figure()
########RUN FOR DELAY OF 300    
#    plt.hist(virus_pop_1)
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Resistant Virus Population delay 300")
    
########RUN FOR DELAY OF 150    
    plt.hist(virus_pop_2,label = 'Delay: 150')
    plt.xlabel('Final Total Virus Populations')
    plt.ylabel('Number of Patients')
    plt.title("100 Patients: Total Resistant Virus Population delay 150")
    
###########RUN FOR DELAY OF 75    
#    plt.hist(virus_pop_3,label = 'Delay: 75')
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Resistant Virus Population delay 75")
    
#########RUN FOR DELAY OF 0    
##    plt.hist(virus_pop_4, label = 'Delay: 0')
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Resistant Virus Population delay 0")
    plt.show()

#
# PROBLEM 7
#
     
def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    resistances = {'guttagonol':False,'grimpex':False}
    virus_pop_1 = []
    virus_pop_2 = []
    time_1 = 150+300+150
    time_2 = 150+150
    num_patients = 100
    num_viruses = 100
    total_viruses = 0
#    for i in range(100):
#        virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
    
    for p in range (num_patients):
        virus_list = []
        for i in range(num_viruses):
            virus_list.append(ResistantVirus(0.1,0.05,resistances,0.005))
        
        
#########RUN FOR 150-> GUTTAGONOL, THEN 300-> GRIMPEX
#        test_patient_1 = Patient(virus_list,1000)
#        for k in range (time_1):
#            if k == 150:
#                test_patient_1.addPrescription('guttagonol')
#            if k == 300:
#                test_patient_1.addPrescription('grimpex')            
#            total_viruses=(test_patient_1.update())
#        virus_pop_1.append(total_viruses)
#        print("Patient:",p,"has", total_viruses)
#        total_viruses = 0
#        
##########RUN 150-> GUTTAGONOL + GRIMPEX
        test_patient_2 = Patient(virus_list,1000)
        for k in range (time_2):
            if k == 150:
                test_patient_2.addPrescription('guttagonol')
            if k == 225:
                test_patient_2.addPrescription('grimpex')  
            total_viruses = (test_patient_2.update())
        virus_pop_2.append(total_viruses)
        print("Patient:",p,"has", total_viruses)
        total_viruses = 0
        
        

    plt.figure()
##########RUN FOR 150-> GUTTAGONOL, THEN 300-> GRIMPEX
#    plt.hist(virus_pop_1)
#    plt.xlabel('Final Total Virus Populations')
#    plt.ylabel('Number of Patients')
#    plt.title("100 Patients: Total Resistant Virus Population, sep. admin drugs")
    
##########RUN 150-> GUTTAGONOL + GRIMPEX   
    plt.hist(virus_pop_2,label = 'Delay: 150')
    plt.xlabel('Final Total Virus Populations')
    plt.ylabel('Number of Patients')
    plt.title("100 Patients: Total Resistant Virus Population, simult. admin drugs")
problem7()
