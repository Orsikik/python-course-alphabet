from itertools import count
from functools import reduce


a = count(1, 1)
b = next(a)
c = next(a)
d = next(a)




reduce((lambda x, y: x if x.free_places() > y.free_places() else y), self.garages)






