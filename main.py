import tkinter as tk
from tkinter import ttk
import numpy as np

# Definicja klasy aplikacji
class GameOfLifeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Game of Life")

        # Inicjalizacja zmiennych
        self.size = 50
        self.updateInterval = 200
        self.numFrames = 100

        self.ON = 255
        self.OFF = 0
        self.running = False

        # Tworzenie interfejsu użytkownika
        self.canvas = tk.Canvas(master, width=self.size * 10, height=self.size * 10)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.start_button = ttk.Button(master, text="Start", command=self.start_animation)
        self.start_button.grid(row=1, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_animation)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5)

        self.reset_button = ttk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.grid(row=1, column=2, padx=5, pady=5)

        # Inicjalizacja siatki
        self.setup_grid()
        self.draw_grid()

    # Ustawienie siatki na początkowe wartości
    def setup_grid(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)

    # Rysowanie siatki na podstawie aktualnego stanu
    def draw_grid(self):
        self.canvas.delete("all")
        cell_size = 10
        for i in range(self.size):
            for j in range(self.size):
                color = "white" if self.grid[i, j] == self.OFF else "black"
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)

    # Aktualizacja stanu siatki
    def update(self):
        # Tworzymy kopię aktualnej siatki
        newGrid = self.grid.copy()

        # Przechodzimy przez każdą komórkę w siatce
        for i in range(self.size):
            for j in range(self.size):
                # Obliczamy sumę stanów ośmiu sąsiednich komórek, po to, żeby zdecydować czy dana komórka
                # powinna pozostać żywa, czy umrzeć w następnej "generacji" gry
                total = int((self.grid[i, (j - 1) % self.size] + self.grid[i, (j + 1) % self.size] +
                             self.grid[(i - 1) % self.size, j] + self.grid[(i + 1) % self.size, j] +
                             self.grid[(i - 1) % self.size, (j - 1) % self.size] + self.grid[
                                 (i - 1) % self.size, (j + 1) % self.size] +
                             self.grid[(i + 1) % self.size, (j - 1) % self.size] + self.grid[
                                 (i + 1) % self.size, (j + 1) % self.size]) / 255)

                # Jeżeli komórka jest żywa
                if self.grid[i, j] == self.ON:
                    # Jeżeli ma mniej niż 2 lub więcej niż 3 żywych sąsiadów, umiera
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = self.OFF
                else:
                    # Jeżeli ma dokładnie 3 żywych sąsiadów, ożywa
                    if total == 3:
                        newGrid[i, j] = self.ON

        # Aktualizujemy siatkę do nowego stanu
        self.grid[:] = newGrid[:]

        # Usuwamy komórki, które są poza granicami siatki
        self.remove_out_of_bounds_cells()

        # Rysujemy siatkę na podstawie jej aktualnego stanu
        self.draw_grid()

    # Usuwanie komórek poza granicami siatki
    def remove_out_of_bounds_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == self.ON:
                    if i == 0 or i == self.size - 1 or j == 0 or j == self.size - 1:
                        self.grid[i, j] = self.OFF

    # Rozpoczęcie animacji
    def start_animation(self):
        self.running = True
        self.animate()

    # Zatrzymanie animacji
    def stop_animation(self):
        self.running = False

    # Resetowanie siatki do stanu początkowego
    def reset_grid(self):
        self.setup_grid()
        self.draw_grid()
        if self.running:
            self.stop_animation()
            self.start_animation()


    # Animacja siatki
    def animate(self):
        if self.running:
            self.update()
            self.master.after(self.updateInterval, self.animate)


    # Zmiana stanu komórki po kliknięciu
    def toggle_cell(self, event):
        x, y = event.x // 10, event.y // 10
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y, x] = self.ON if self.grid[y, x] == self.OFF else self.OFF
            self.draw_grid()

# Główna funkcja programu
def main():
    root = tk.Tk()
    app = GameOfLifeApp(root)
    app.canvas.bind("<Button-1>", app.toggle_cell)
    root.mainloop()

# Uruchomienie programu
if __name__ == "__main__":
    main()