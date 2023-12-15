import pickle

class Chromosome:
    crossover_rate = 0  # Replace with actual values
    mutation_rate = 0  # Replace with actual values
    hours = 0  # Replace with actual values
    days = 0  # Replace with actual values
    no_student_group = 0  # Replace with actual values

    def __init__(self):
        self.gene = [Gene(i) for i in range(self.no_student_group)]
        self.fitness = self.get_fitness()

    def deep_clone(self):
        return pickle.loads(pickle.dumps(self, -1))

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


class Gene:
    def __init__(self, idx):
        self.slot_no = [idx * Chromosome.hours * Chromosome.days + i for i in range(Chromosome.hours * Chromosome.days)]


class TimeTable:
    slot = [None] * (Chromosome.hours * Chromosome.days)  # Assuming TimeTable is a class with a static slot attribute
