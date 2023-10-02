'''
WIP-program for generating recipe lists for end product orders in the open-world factory building game "Satisfactory" (2022)
'''

def main():
    #filtest()
    items = loaditems("satisfactorygiga.txt")
    processitems(items)
    expo = {}
    
    x = hub([[20, items[5]]], items)
    print("x:", x)

    for y in x:
        neworder = Order(0, y)
        neworder.clean(items)
        print(neworder.resultbook)
    print(x)
    print(expo)
    


def loaditems(filename):
    file = open(filename)
    itemlist = []
    for line in file:
        x = line.strip().split(" ")
        focus = str(x[0])
        machine = str(x[1])
        output = float(x[2])
        rest = x[3:] #recipe and byproduct

        ingredients = []
        byproduct = []
        
        counter = 0
        if len(rest) % 2 == 0:
            while counter < len(rest):
                ingredients.append([float(rest[counter]), str(rest[(counter + 1)])])
                counter += 2
        else: 
            while counter < len(rest):
                if rest[counter] == "yes":
                    counter += 1
                    byproduct.append([float(rest[counter]), str(rest[(counter + 1)])])
                    counter += 2
                else:
                    ingredients.append([float(rest[counter]), str(rest[(counter + 1)])])
                    counter += 2
        exportrecipe = Recipe(machine, output, ingredients, byproduct)
        bino = False
        binocount = 0
        for q in itemlist:
            if q.name == focus:
                bino = True
            else: 
                binocount += 1

        if bino:
            itemlist[binocount].addrecipe(exportrecipe)
        else: 
            newitem = Item(focus)
            newitem.addrecipe(exportrecipe)
            itemlist.append(newitem)

    return itemlist
    

def processitems(itemlist):
    for x in itemlist:
        for y in x.recipe:
            for z in y.ingredients:
                for a in itemlist:
                    if z[1] == a.name:
                        z[1] = a


def hub(orderlist, itemlist):
    print("orderlist")
    print(orderlist)
    nextstep = []
    for x in orderlist:
        print("hub doin", x)
        if x[1] in itemlist:
            nextstep.append((order(x[0], x[1])))
        else:
            nextstep.append([x[0], x[1]])
    return nextstep[0]


def order(amount, item):
    print("ordering")
    print(amount, item)
    exp = []
    if len(item.recipe) == 1:
        print("1 rec")
        freq = (amount / item.recipe[0].output)
        for y in item.recipe[0].ingredients:
            exp.append([(freq * y[0]), y[1]])
        return exp
    else:
        print("more rec")
        for x in item.recipe:
            alts = []
            freq = (amount / x.output)
            for y in x.ingredients:
                alts.append([(freq * y[0]), y[1]])
            exp.append(alts)
        return exp


class Order: 
    def __init__(self, id, items):
        print("neworder", id, items)
        self.id = id
        self.branches = items
        self.children = []
        self.resultbook = {}
    
    def clean(self, items):
        lok = []
        print("order in", self.branches)
        for x in self.branches:
            if x[1] not in items: 
                if x[1] in self.resultbook.keys():
                    self.resultbook[x[1]] += x[0]
                else: 
                    self.resultbook[x[1]] = x[0]
                lok.append(x)
        for a in lok: 
            self.branches.remove(a)
        print("order out", self.branches)

class Item: 
    def __init__(self, name):
        self.name = name
        self.recipe = []

    def addrecipe(self, recipe):
        self.recipe.append(recipe)

    def __repr__(self):
        return self.name


class Recipe: 
    def __init__(self, machine, output, ingredients, byproduct):
        self.machine = machine
        self.output = output
        self.ingredients = ingredients
        self.byproduct = byproduct

    def __repr__(self):
        ingrstring = ""
        for x in self.ingredients:
            ingrstring += str(x[0])
            ingrstring += " "
            ingrstring += str(x[1])
            ingrstring += " "
        superstring = ("Maskin: " + self.machine + " Output: " + str(self.output) + " " + "Ingredienser: " + ingrstring)

        return superstring.strip()
        
        
main()

'''
def filtest():
    file = open("satisfactorygiga.txt")
    unik = []
    for line in file:
        x = line.strip().split(" ")
        for y in x:
            if y not in unik:
                unik.append(y)
    unik = sorted(unik)
    for x in unik:
        print(x)



print("ordering", amount, item)
    alternatives = []
    for x in item.recipe:
        freq = (amount / x.output)
        temp = []
        if len(x.ingredients) == 1:
            if x.ingredients[0][1] in itemlist:
                print("1")
                alternatives.append(order((x.ingredients[0][0] * freq), x.ingredients[0][1], itemlist, expo))
            else:
                print("2")
                styly = [(x.ingredients[0][0] * freq), x.ingredients[0][1]]
                alternatives.append(styly)
                expo.append(styly)
        else: 
            for y in x.ingredients:
                if y[1] in itemlist:
                    print("3")
                    temp.append(order((y[0] * freq), y[1], itemlist, expo))
                else: 
                    print("4")
                    temp.append([(y[0] * freq), y[1]])
            alternatives.append(temp)
    
    print("alternatives")
    if len(alternatives) == 1:
        print(alternatives[0])
        return alternatives[0]
    else:
        print(alternatives)
        return alternatives


'''