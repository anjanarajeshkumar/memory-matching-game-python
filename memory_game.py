import tkinter as tk
from tkinter import messagebox
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matching Game")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Game State Variables
        self.moves = 0
        self.matches = 0
        self.start_time = time.time()
        self.timer_running = True

        self.first_card_idx = None
        self.second_card_idx = None
        self.can_click = True

        self.buttons = []
        # We need 8 pairs for a 4x4 grid. Using standard letters for simplicity.
        self.card_values = list("AABBCCDDEEFFGGHH")
        random.shuffle(self.card_values)

        # Initialize GUI
        self.create_ui()
        self.update_timer()

    def create_ui(self):
        """Creates the graphical interface including the stats header and the card grid."""
        # Top Frame for Move and Time Tracking
        stats_frame = tk.Frame(self.root, pady=10)
        stats_frame.pack()

        self.moves_label = tk.Label(stats_frame, text="Moves: 0", font=("Helvetica", 14, "bold"))
        self.moves_label.grid(row=0, column=0, padx=20)

        self.time_label = tk.Label(stats_frame, text="Time: 0s", font=("Helvetica", 14, "bold"))
        self.time_label.grid(row=0, column=1, padx=20)

        # Grid Frame for the 4x4 Card Layout
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        # Create 16 buttons (cards) and place them in a 4x4 grid
        for i in range(16):
            btn = tk.Button(self.grid_frame, text=" ", font=("Helvetica", 24, "bold"), 
                            width=4, height=2, bg="lightgrey", relief="raised",
                            command=lambda i=i: self.on_card_click(i))
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons.append(btn)

    def update_timer(self):
        """Updates the timer every second while the game is running."""
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}s")
            # Call this function again after 1000ms (1 second)
            self.root.after(1000, self.update_timer)

    def on_card_click(self, idx):
        """Handles the logic when a player clicks a card."""
        # Prevent clicking if evaluating a pair or if the card is already flipped
        if not self.can_click or self.buttons[idx]["text"] != " ":
            return

        # Reveal the card
        self.buttons[idx].config(text=self.card_values[idx], bg="white")

        if self.first_card_idx is None:
            # This is the first card flipped
            self.first_card_idx = idx
        else:
            # This is the second card flipped
            self.second_card_idx = idx
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            
            # Temporarily disable clicks while evaluating the match
            self.can_click = False 
            self.root.after(800, self.check_match)

    def check_match(self):
        """Checks if the two revealed cards match."""
        first_val = self.card_values[self.first_card_idx]
        second_val = self.card_values[self.second_card_idx]

        if first_val == second_val:
            # Match found! Disable the buttons and change color
            self.buttons[self.first_card_idx].config(state="disabled", disabledforeground="green", bg="lightgreen")
            self.buttons[self.second_card_idx].config(state="disabled", disabledforeground="green", bg="lightgreen")
            self.matches += 1

            # Check for win condition
            if self.matches == 8:
                self.timer_running = False
                elapsed_time = int(time.time() - self.start_time)
                messagebox.showinfo("Congratulations!", f"Game Over!\nYou won in {self.moves} moves and {elapsed_time} seconds.")
        else:
            # Mismatch! Hide the cards again
            self.buttons[self.first_card_idx].config(text=" ", bg="lightgrey")
            self.buttons[self.second_card_idx].config(text=" ", bg="lightgrey")

        # Reset selection state for the next turn
        self.first_card_idx = None
        self.second_card_idx = None
        self.can_click = True

# Application Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGame(root)
    root.mainloop()
