
class Movies:
    def __init__(self,m):
        self.m = m
    def add_movies(self):
        l = int(input("Enter how many movies you want to add: "))
        for i in range(l):
            n = input(f"Please enter the name of {i+1} movie:")
            b = input("Please enter the budget:")
            self.m.append((n,int(b)))
    def avg_budget(self):
        s = 0
        for i in self.m:
            s+=i[1]
        return s/len(self.m)
    def above_avg(self):
        try:
            self.a_avg = []
            for i in self.m:
                if i[1] > self.avg_budget():
                    diff = i[1]- self.avg_budget()
                    self.a_avg.append((i[0],int(diff)))
            print("The list of movies above the avg budget with their difference.")
            print(self.a_avg)
        except AttributeError:
            print("Error: Average budget is not calculated!\nFirst calculate the average budget.")
movies = [
("Eternal Sunshine of the Spotless Mind", 20000000),
("Memento", 9000000),
("Requiem for a Dream", 4500000),
("Pirates of the Caribbean: On Stranger Tides", 379000000),
("Avengers: Age of Ultron", 365000000),
("Avengers: Endgame", 356000000),
("Incredibles 2", 200000000)
]


collection1 = Movies(movies)
collection1.add_movies()
print(collection1.avg_budget())
print(collection1.above_avg())
