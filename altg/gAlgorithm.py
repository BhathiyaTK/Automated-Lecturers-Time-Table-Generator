import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'altg.settings')
django.setup()

import prettytable as prettytable
import random as rnd

from altg_app.models import *

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

passed_val1 = '%s' % (sys.argv[1])
passed_val2 = '%s' % (sys.argv[2])
class Data:
    HALLS = AllLectureHalls.objects.all().values_list('hall_name', 'hall_capacity')
    MEETING_TIMES = [["MT1", "Monday 08:00 - 10.00"],
                     ["MT2", "Monday 10:00 - 12:00"],
                     ["MT3", "Monday 01:00 - 03:00"],
                     ["MT4", "Monday 03:00 - 05:00"],
                     ["MT5", "Tuesday 08:00 - 10.00"],
                     ["MT6", "Tuesday 10:00 - 12.00"],
                     ["MT7", "Tuesday 01:00 - 03:00"],
                     ["MT8", "Tuesday 03:00 - 05.00"],
                     ["MT9", "Wednesday 08:00 - 10.00"],
                     ["MT10", "Wednesday 10:00 - 12:00"],
                     ["MT11", "Wednesday 01:00 - 03:00"],
                     ["MT12", "Wednesday 03:00 - 05:00"],
                     ["MT13", "Thursday 08:00 - 10.00"],
                     ["MT14", "Thursday 10:00 - 12:00"],
                     ["MT15", "Thursday 01:00 - 03:00"],
                     ["MT16", "Thursday 03:00 - 05:00"],
                     ["MT17", "Friday 08:00 - 10.00"],
                     ["MT18", "Friday 10:00 - 12:00"],
                     ["MT19", "Friday 01:00 - 03:00"],
                     ["MT20", "Friday 03:00 - 05:00"]]
    INSTRUCTORS = User.objects.filter(lecturer_name=passed_val1).values_list('lecturer_code', 'lecturer_name')
    COURSES = AllSubjects.objects.filter(related_lecturer=passed_val1, semester=passed_val2).values_list('subject_code', 'subject_name', 'related_lecturer', 'std_count')
    def __init__(self):
        self._halls = []
        self._meetingTimes = []
        self._instructors = []
        self._courses = []
        for i in range(0, len(self.HALLS)):
            self._halls.append(Hall(self.HALLS[i][0], self.HALLS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        for i in range(0, len(self.COURSES)):
            self._courses.append(Course(
                self.COURSES[i][0], self.COURSES[i][1], self.COURSES[i][2], self.COURSES[i][3]))
        dept1 = Department("CIS", self._courses)
        self._depts = [dept1]
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())
    def get_halls(self): return self._halls
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses
    
class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self):
        return self._numbOfConflicts
    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness
    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0,len(data.get_meetingTimes()))])
                newClass.set_hall(data.get_halls()[rnd.randrange(0, len(data.get_halls()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if(classes[i].get_hall().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if(j >= i):
                    if(classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                       if(classes[i].get_hall() == classes[j].get_hall()):
                           self._numbOfConflicts += 1
                       if(classes[i].get_instructor() == classes[j].get_instructor()):
                           self._numbOfConflicts += 1
        return 1/((1.0*self._numbOfConflicts + 1))
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ","
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue
    
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialize())
    def get_schedules(self):
        return self._schedules
    
class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(rnd.random() > 0.5):
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()):
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key = lambda x: x.get_fitness(), reverse = True)
        return tournament_pop
    
class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def __str__(self): return self._name

class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name

class Hall:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity
    
class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time

class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses
    
class Class:
    def __init__(self, id, hall, course):
        self._id = id
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._hall = None
    def get_id(self): return self._id
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_hall(self): return self._hall
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_hall(self, hall): self._hall = hall
    def __str__(self):
        return str(self._course.get_number()) + "," + str(self._hall.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())

class DisplayMgr:
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = []
        for i in range(0, len(classes)):
            table.append([str(i+1), classes[i].get_course().get_name() + " ("+
                           classes[i].get_course().get_number() + ", "+
                           str(classes[i].get_course().get_maxNumbOfStudents()) + ")",
                           classes[i].get_hall().get_number(),
                           classes[i].get_meetingTime().get_time()])
        print(table)

data = Data()
displayMgr = DisplayMgr()
generationNumber = 0
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key = lambda x: x.get_fitness(), reverse = True)
geneticAlgorithm = GeneticAlgorithm()
while(population.get_schedules()[0].get_fitness() != 1.0):
    generationNumber += 1
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key = lambda x: x.get_fitness(), reverse = True)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
