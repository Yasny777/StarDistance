import tkinter as tk
from Star import *
from StarCatalog import *
from tkinter import filedialog

class StarGUI:
    def __init__(self, catalog):
        self.catalog = catalog

#------------------------------------------------------Window-------------------------------------------------------
        self.root = tk.Tk()
        self.root.title("Systemy gwiezdne")
        # self.root.geometry("500x300")

#------------------------------------------------------Labels-------------------------------------------------------
        self.name_label = tk.Label(self.root, text="Nazwa Planety:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)


        self.distance_label = tk.Label(self.root, text="Dystans od Ziemi:")
        self.distance_label.grid(row=1, column=0)
        self.distance_entry = tk.Entry(self.root)
        self.distance_entry.grid(row=1, column=1)

#------------------------------------------------------BUTTONS------------------------------------------------------
        self.add_button = tk.Button(self.root, text="Dodaj Gwiazde", command=self.add_star)
        self.add_button.grid(row=2, column=0, sticky="nswe")

        self.search_button = tk.Button(self.root, text="Szukaj Gwiazdy", command=self.search_star)
        self.search_button.grid(row=2, column=1, sticky="nswe")

        self.remove_button = tk.Button(self.root, text="Usun Gwiazde", command=self.remove_star)
        self.remove_button.grid(row=2, column=2, sticky="nswe")

        self.disp_button = tk.Button(self.root, text="Wyswietl Gwiazdy", command=self.display_stars)
        self.disp_button.grid(row=2, column=3, sticky="nswe")

        self.file_button = tk.Button(self.root, text="Wczytaj z Pliku", command=self.browse_files) # command tu
        self.file_button.grid(row=2,column=4, sticky="nswe")

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, column=0, columnspan=3)

        self.listbox = tk.Listbox(self.root, width=60)
        self.listbox.grid(row=4, column=0, columnspan=4)


        self.root.mainloop()

# sciezke zmienic w razie czego
    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir = "/Pulpit/",
                                              title = "Wybierz plik",
                                              filetypes = (("Pliki tekstowe", "*.txt"),("wszystkie pliki","*.*")))
        starList = []
        try:
            if(filename.endswith(".txt")):
                file = open(filename, "r")

                for line in file.readlines():
                    starList.append(line)

                for star in starList:
                    object = star.strip("\n").split(",")
                    name = object[0]
                    distance = object[1]
                    self.add_star_from_file(name, distance)

                file.close()
            else:
                self.result_label.config(text="To nie jest plik txt")
        except UnboundLocalError:
            self.result_label.config(text="To nie jest plik txt")



    def add_star_from_file(self, name, distance):
        try:
            name_length = len(name)
            distance_length = len(distance)
            distance = float(distance)

            for star in self.catalog.stars:
                if(name == star.name):
                    return

            if (name_length == 0 or distance_length == 0):
                return

            elif(distance == 0 or name=="Ziemia" or name=="ziemia"):
                return

            elif (distance < 0):
                return

            else:
                self.catalog.add_star(Star(name, distance))
                self.catalog.sort_by_distance()
        except ValueError:
            self.result_label.config(text="Nie wszystkie dane w pliku byly poprawne (sprawdz plik)")

    def add_star(self):
        try:
            name = self.name_entry.get()
            distance = float(self.distance_entry.get())

            for star in self.catalog.stars:
                if(name == star.name):
                    self.result_label.config(text="Taka planeta juz istnieje w katalogu")
                    return

            if (len(self.name_entry.get()) == 0 or len(self.distance_entry.get()) == 0):
                self.result_label.config(text="Zle dane wejsciowe")
                return
            elif(distance == 0 or name=="Ziemia" or name=="ziemia"):
                self.result_label.config(text="To jest Ziemia XD")
                return
            elif (distance > 0):
                self.catalog.add_star(Star(name, distance))
                self.catalog.sort_by_distance()
                self.result_label.config(text="Gwiazda dodana")
            else:
                self.result_label.config(text="Odleglosc ujemna")
        except ValueError:
            self.result_label.config(text="Zle dane wejsciowe")

    #do poprawy
    def search_star(self):
        name = self.name_entry.get()
        # if(len(name) == 0):
        #     self.result_label.config(text="Nazwa jest pusta")
        #     return
        star = self.catalog.search(name)
        if star == None:
            self.result_label.config(text="Gwiazda nieznaleziona, nie ma takiej gwiazdy w katalogu")
        else:
            self.result_label.config(text=f"Nazwa: {star.name}, Dystans: {star.distance_from_earth}")

    def remove_star(self):
        name = self.name_entry.get()
        remove_star = self.catalog.remove(name)
        if remove_star == None:
            self.result_label.config(text="Nie ma takiej gwiazdy do usuniecia lub nazwa jest pusta")
        else:
            self.catalog.sort_by_distance()
            self.result_label.config(text="Gwiazda usunieta pomyslnie")

    def display_stars(self):
        self.listbox.delete(0, tk.END) # clear the previous items in the listbox
        for star in self.catalog.stars:
            self.listbox.insert(tk.END, f"Nazwa: {star.name}, Dystans: {star.distance_from_earth}")



