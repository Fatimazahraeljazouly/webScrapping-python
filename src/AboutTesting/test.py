class rectangle:
    def __init__(self,x,y):
        self._x = x
        self._y = y
    def surface(self):
        return self._x*self._y
class paveDroit(rectangle):
    def __init__(self,x,y,z):
        super().__init__(x,y)
        self.__z = z
    def surface(self):
        return 2*(self._x*self._y+self._x*self.__z+self._y*self.__z)
photo1 = rectangle(3,4)
print(photo1.surface())
photo2 = paveDroit(3,4,10)
print(photo2.surface())
photo2=photo1
print(photo2.surface())
photo2= rectangle(3,4)
print(photo2.surface())


class A:
    def __init__(self):
        print("Début init A")
        super().__init__()
        print(super().__str__())
        print("Fin init A")
    def __str__(self):
        return "Classe A"
class B:
    def __init__(self):
        print("Début init B")
        super().__init__()
        print(super().__str__())
        print("Fin init B")
    def __str__(self):
        return "Classe B"
class C(A, B):
    def __init__(self):
        print("Début init C")
        super().__init__()
        print("Fin init C")
class D(B, A):
    def __init__(self):
        print("Début init D")
        super().__init__()
        print("Fin init D"),
c=C()
d=D()