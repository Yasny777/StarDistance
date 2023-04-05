from Star import *

class StarCatalog:
    def __init__(self):
        self.stars = []

    def add_star(self, star):
            self.stars.append(star)


    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                name, distance = line.strip().split(',')
                self.add_star(Star(name, float(distance)))

    def search(self, name):
        if(len(name) == 0):
            return None
        else:
            for star in self.stars:
                if star.name == name:
                    return star
        return None

    def remove(self, name):
        star = self.search(name)
        if star == None:
            return None
        else:
            self.stars.remove(star)

    def sort_by_distance(self):
        self.stars.sort(key=lambda x: x.distance_from_earth)
