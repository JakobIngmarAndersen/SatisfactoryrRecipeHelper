class Task: 
    def __init__(self, gen, time, manpower):
        self.gen = gen
        self.timeReq = time
        self.manpower = manpower
        self.dependantOn = []
        self.enables = []
        self.transit = False
        self.slack = 0

    def __str__(self): 
        x = "Time for task: " + str(self.timeReq) + "\n" + "Manpower required: " + str(self.manpower)
        return x

    def startStop(self):
        if self.transit: 
            print("Completed: " + str(self.gen))
        else:
            print("Starting: " + str(self.gen))
            self.transit = True
        return self.manpower

    def deepDive(self):
        if self.enables:
            q = self.enables[0]
            for x in self.enables:
                if x.timeReq > q.timeReq:
                    q = x
            return q.deepDive()
        else: 
            return self
    
    def reSurface(self, value):
        if self.dependantOn:
            q = self.dependantOn[0]
            for x in self.dependantOn:
                if x.timeReq > q.timeReq:
                    q = x

            for x in self.dependantOn:
                if x != q:
                    x.slack = (q.timeReq - x.timeReq)
            value += q.timeReq
            return q.reSurface(value)
        else: 
            print("value out " + str(value))
            return value
        

            



class ScrumBoard:
    def __init__(self, tasks):
        self.time = 0
        self.toDo = tasks
        self.atWork = 0
        self.setEnables()
        self.slackulator(self.toDo)
        print("Initiating project \n\nTime: " + str(self.time))
        self.work(self.readyTasks(), self.time)
        
    def setEnables(self):
        for x in self.toDo:
            if x.dependantOn:
                for y in x.dependantOn:
                    y.enables.append(x)

    def slackulator(self, listy):
        botNode = self.toDo[0].deepDive()
        botNode.reSurface(botNode.timeReq)
        for x in self.toDo: 
            print(x.slack)


    def readyTasks(self):
        inProgress = []
        for y in self.toDo:
            if not y.dependantOn:
                inProgress.append(y)
        return inProgress

    def middleMan(self, listy):
        timer = self.opTime(listy)
        for x in listy:
            if not x.transit: 
                self.atWork += x.startStop()
            elif x.timeReq == 0:
                self.timeStamp()
                self.atWork -= x.startStop()
                for m in self.toDo: 
                    if x in m.dependantOn:
                        m.dependantOn.remove(x)
                self.toDo.remove(x)
                listy.remove(x)
            x.timeReq -= timer
        return timer

    def work(self, listy, time):
        while self.toDo: 
            self.time += self.middleMan(listy)
            self.work(self.readyTasks(), self.time)
            
    def timeStamp(self):
        print("Staff at work: " + str(self.atWork))
        print()
        print("Time: " + str(self.time))    

    def opTime(self, listy): 
        f = listy[0].timeReq
        for x in listy:
            if x.timeReq < f:
                f = x.timeReq
        return f

def makeExample():
    T1 = Task(1, 3, 4)
    T2 = Task(2, 5, 2)
    T3 = Task(3, 1, 2)
    T4 = Task(4, 2, 4)
    T5 = Task(5, 4, 3)
    T6 = Task(6, 8, 4)
    T7 = Task(7, 3, 2)
    T8 = Task(8, 1, 3)

    taskBook = [T1, T2, T3, T4, T5, T6, T7, T8]
    
    T8.dependantOn.append(T6)
    T7.dependantOn.append(T5)
    T7.dependantOn.append(T6)
    T6.dependantOn.append(T3)
    T6.dependantOn.append(T4)
    T5.dependantOn.append(T3)
    T4.dependantOn.append(T2)
    T3.dependantOn.append(T1)
    T3.dependantOn.append(T2)
    x = ScrumBoard(taskBook)

"""
    T2.enables.append(T3)
    T1.enables.append(T3)
    T2.enables.append(T4)
    T3.enables.append(T5)
    T4.enables.append(T6)
    T3.enables.append(T6)
    T6.enables.append(T7)
    T6.enables.append(T8)
    T5.enables.append(T7)
"""


    
    

makeExample()

