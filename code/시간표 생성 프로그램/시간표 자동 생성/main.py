import random
import copy

class Gene:
    def __init__(self, idx):
        self.slot_no = [idx * Chromosome.hours * Chromosome.days + i for i in range(Chromosome.hours * Chromosome.days)]

    def deep_clone(self):
        return copy.deepcopy(self)


class TimeTable:
    slot = [None] * (Chromosome.hours * Chromosome.days)


class Chromosome:
    crossover_rate = 0
    mutation_rate = 0
    hours = 0
    days = 0
    no_student_group = 0

    def __init__(self):
        self.gene = [Gene(i) for i in range(self.no_student_group)]
        self.fitness = self.get_fitness()

    def deep_clone(self):
        return copy.deepcopy(self)

    def get_fitness(self):
        point = 0
        for i in range(self.hours * self.days):
            teacher_list = []
            for j in range(self.no_student_group):
                slot = TimeTable.slot[self.gene[j].slot_no[i]] if TimeTable.slot[self.gene[j].slot_no[i]] is not None else None

                if slot is not None:
                    if slot.teacher_id in teacher_list:
                        point += 1
                    else:
                        teacher_list.append(slot.teacher_id)

        self.fitness = 1 - (point / ((self.no_student_group - 1.0) * self.hours * self.days))
        point = 0
        return self.fitness

    def print_time_table(self):
        for i in range(self.no_student_group):
            status = False
            l = 0
            while not status:
                if TimeTable.slot[self.gene[i].slot_no[l]] is not None:
                    print("Batch " + TimeTable.slot[self.gene[i].slot_no[l]].student_group.name + " Timetable-")
                    status = True
                l += 1

            for j in range(self.days):
                for k in range(self.hours):
                    if TimeTable.slot[self.gene[i].slot_no[k + j * self.hours]] is not None:
                        print(TimeTable.slot[self.gene[i].slot_no[k + j * self.hours]].subject, end=" ")
                    else:
                        print("*FREE*", end=" ")
                print("")

            print("\n\n\n")

    def print_chromosome(self):
        for i in range(self.no_student_group):
            for j in range(self.hours * self.days):
                print(self.gene[i].slot_no[j], end=" ")
            print("")

    def __lt__(self, other):
        return self.fitness > other.fitness


class SchedulerMain:
    populationsize = 1000
    maxgenerations = 100
    finalson = None

    def __init__(self):
        # printing input data (on console for testing)
        Utility.print_input_data()

        # generating slots
        TimeTable()

        # printing slots (testing purpose only)
        Utility.print_slots()

        # initializing first generation of chromosomes and putting in first array list
        self.initialize_population()

        # generating newer generation of chromosomes using crossovers and mutation
        self.create_new_generations()

    # Creating new Generations using crossovers and mutations
    def create_new_generations(self):
        nogenerations = 0

        # looping max no of generations times or until suitable chromosome found
        while nogenerations < self.maxgenerations:
            newlist = []
            newlistfitness = 0
            i = 0

            # first 1/10 chromosomes added as it is- Elitism
            for i in range(self.populationsize // 10):
                newlist.append(self.firstlist[i].deep_clone())
                newlistfitness += self.firstlist[i].get_fitness()

            # adding other members after performing crossover and mutation
            while i < self.populationsize:
                father = self.select_parent_roulette()
                mother = self.select_parent_roulette()

                # crossover
                if random.random() < inputdata.crossoverrate:
                    son = self.crossover(father, mother)
                else:
                    son = father

                # mutation
                self.custom_mutation(son)

                if son.fitness == 1:
                    print("Selected Chromosome is:-")
                    son.print_chromosome()
                    break

                newlist.append(son)
                newlistfitness += son.get_fitness()
                i += 1

            # if chromosome with fitness 1 found
            if i < self.populationsize:
                print("****************************************************************************************")
                print(
                    f"\n\nSuitable Timetable has been generated in the {i}th Chromosome of {nogenerations + 2} generation with fitness 1.")
                print("\nGenerated Timetable is:")
                son.print_time_table()
                self.finalson = son
                break

            # if chromosome with required fitness not found in this generation
            self.firstlist = newlist
            self.firstlist.sort()
            newlist.sort()
            print(
                f"**************************     Generation{nogenerations + 2}     ********************************************\n")
            self.print_generation(newlist)
            nogenerations += 1

    # selecting using Roulette Wheel Selection only from the best 10% chromosomes
    def select_parent_roulette(self):
        self.firstlistfitness /= 10
        random_double = random.random() * self.firstlistfitness
        current_sum = 0
        i = 0

        while current_sum <= random_double:
            current_sum += self.firstlist[i].get_fitness()
            i += 1

        return self.firstlist[i - 1].deep_clone()

    # custom mutation
    def custom_mutation(self, c):
        new_fitness = 0
        old_fitness = c.get_fitness()
        gene_no = random.randint(0, inputdata.nostudentgroup - 1)

        i = 0
        while new_fitness < old_fitness:
            c.gene[gene_no] = Gene(gene_no)
            new_fitness = c.get_fitness()

            i += 1
            if i >= 500000:
                break

    # Two point crossover
    def crossover(self, father, mother):
        random_int = random.randint(0, inputdata.nostudentgroup - 1)
        temp = father.gene[random_int].deep_clone()
        father.gene[random_int] = mother.gene[random_int].deep_clone()
        mother.gene[random_int] = temp
        if father.get_fitness() > mother.get_fitness():
            return father
        else:
            return mother

    # initializing first generation of population
    def initialize_population(self):
        # generating first generation of chromosomes and keeping them in an array list
        self.firstlist = []
        self.firstlistfitness = 0

        for _ in range(self.populationsize):
            c = Chromosome()
            self.firstlist.append(c)
            self.firstlistfitness += c.fitness

        self.firstlist.sort()
        print("----------Initial Generation-----------\n")
        self.print_generation(self.firstlist)

    # printing important details of a generation
    def print_generation(self, lst):
        print("Fetching details from this generation...\n")

        # to print only initial 4 chromosomes of sorted list
        for i in range(4):
            print(f"Chromosome no.{i}: {lst[i].get_fitness()}")
            lst[i].print_chromosome()
            print("")

        print(f"Chromosome no. {self.populationsize // 10 + 1}: {lst[self.populationsize // 10 + 1].get_fitness()}\n")
        print(f"Chromosome no. {self.populationsize // 5 + 1}: {lst[self.populationsize // 5 + 1].get_fitness()}\n")
        print(f"Most fit chromosome from this generation has fitness = {lst[0].get_fitness()}\n")


# select from best chromosomes only (alternate to roulette wheel selection)
def select_parent_best(lst):
    random_int = random.randint(0, 99)
    return lst[random_int].deep_clone()


# simple Mutation operation
def mutation(c):
    gene_no = random.randint(0, inputdata.nostudentgroup - 1)
    temp = c.gene[gene_no].slot_no[0]
    for i in range(inputdata.daysperweek * inputdata.hoursperday - 1):
        c.gene[gene_no].slot_no[i] = c.gene[gene_no].slot_no[i + 1]
    c.gene[gene_no].slot_no[inputdata.daysperweek * inputdata.hoursperday - 1] = temp


# swap mutation
def swap_mutation(c):
    gene_no = random.randint(0, inputdata.nostudentgroup - 1)
    slot_no1 = random.randint(0, inputdata.hoursperday * inputdata.daysperweek - 1)
    slot_no2 = random.randint(0, inputdata.hoursperday * inputdata.daysperweek - 1)

    temp = c.gene[gene_no].slot_no[slot_no1]
    c.gene[gene_no].slot_no[slot_no1] = c.gene[gene_no].slot_no[slot_no2]
    c.gene[gene_no].slot_no[slot_no2] = temp


def main():
    SchedulerMain()


if __name__ == "__main__":
    main()
