from Tasks import *

class Perform_The_Tasks(object):
    def Perform_the_task_a(self):
        result = Tasks()
        result.task_a()

    def Perform_the_task_b(self):
        result = Tasks()
        result.task_b()

    def Perform_the_task_c(self):
        result = Tasks()
        result.task_c()
    
    def Perform_the_task_d(self):
        result = Tasks()
        result.task_d()

if __name__ == '__main__':
    Perform_The_Tasks().Perform_the_task_a()
    Perform_The_Tasks().Perform_the_task_b()
    Perform_The_Tasks().Perform_the_task_c()
    Perform_The_Tasks().Perform_the_task_d()