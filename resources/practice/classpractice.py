class a:

    i = 12345

    def __init__(self):
        self.data = []

    def f(self):
        return 'hello world'

    def g(self):
        print i

class b:

    def __init__(self):
        self.i = 12345
        self.data = []

    def g(self):
        print self.i

class Complex:

    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

class Dog:

    kind = 'canine'

    def __init__(self, name):
        self.name = name

class Pizza(object):
    def __init__(self):
        self.toppings = []
    def __call__(self, topping):
        # when using '@instance_of_pizza' before a function def
        # the function gets passed onto 'topping'
        self.toppings.append(topping())
    def __repr__(self):
        return str(self.toppings)

pizza = Pizza()

@pizza
def cheese():
    return 'cheese'
@pizza
def sauce():
    return 'sauce'
















