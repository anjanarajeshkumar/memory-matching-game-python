import tkinter as tk
import random

class PawPairQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Paw Pair Quest")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # --- Color Palette ---
        self.bg_color = "#E6E6FA"          # Lavender
        self.card_hidden_color = "#AEC6CF" # Pastel Blue
        self.card_visible_color = "#FFFFFF"# White
        self.card_matched_color = "#77DD77"# Light Green
        self.card_error_color = "#FF6961"  # Soft Red
        self.btn_color = "#20B2AA"         # Bright Teal
        self.text_color = "#333333"        # Dark Gray
        
        # --- Fonts ---
        self.font_title = ("Helvetica", 36, "bold")
        self.font_subtitle = ("Helvetica", 14, "italic")
        self.font_stats = ("Helvetica", 14, "bold")
        self.font_emoji = ("Helvetica", 32)
        
        # --- Game Variables ---
        self.animals = ['🐶', '🐱', '🐰', '🐼', '🦊', '🐸', '🐵', '🐧'] * 2
        self.timer_id = None
        self.cards = [] # Stores dictionary for each card: button widget, animal, state
        
        # Launch Start Screen
        self.show_start_screen()

    # ==========================================
    # 1. UI CREATION: START SCREEN & GAME SCREEN
    # ==========================================
    
    def clear_screen(self):
        """Destroys all widgets currently on the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        """Displays the welcoming start menu."""
        self.clear_screen()
        self.root.configure(bg=self.bg_color)
        
        # Cancel any lingering timers
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Title
        tk.Label(self.root, text="🐾 Paw Pair Quest 🐾", font=self.font_title, 
                 bg=self.bg_color, fg="#8A2BE2").pack(pady=(100, 10))
        
        # Subtitle
        tk.Label(self.root, text="Match the adorable animals before time runs out!", 
                 font=self.font_subtitle, bg=self.bg_color, fg=self.text_color).pack(pady=10)
        
        # Decorative Emojis
        tk.Label(self.root, text="🐶 🐱 🐰 🐼 🦊 🐧", font=("Helvetica", 28), 
                 bg=self.bg_color).pack(pady=20)
        
        # Instructions
        instructions = "Flip cards and find matching animal pairs\nbefore the 90-second timer runs out."
        tk.Label(self.root, text=instructions, font=("Helvetica", 12), 
                 bg=self.bg_color, fg="#555555").pack(pady=20)
        
        # Start Button
        tk.Button(self.root, text="Start Game", font=("Helvetica", 18, "bold"), 
                  bg=self.btn_color, fg="white", activebackground="#17807A", 
                  activeforeground="white", command=self.start_game, 
                  padx=30, pady=10, relief="raised", bd=3).pack(pady=40)

    def start_game(self):
        """Initializes game variables and builds the game board."""
        self.clear_screen()
        
        # Reset State Variables
        self.time_left = 90
        self.moves = 0
        self.matches = 0
        self.score = 0
        self.first_card_index = None
        self.can_click = True
        self.cards = []
        
        random.shuffle(self.animals) # Shuffle the deck
        
        self.build_game_ui()
        self.update_stats()
        self.run_timer()

    def build_game_ui(self):
        """Constructs the stats panel, game grid, and bottom controls."""
        # Stats Panel (Top)
        self.stats_frame = tk.Frame(self.root, bg=self.bg_color)
        self.stats_frame.pack(fill=tk.X, pady=20, padx=20)
        
        self.lbl_moves = tk.Label(self.stats_frame, text="Moves: 0", font=self.font_stats, bg=self.bg_color)
        self.lbl_moves.pack(side=tk.LEFT, padx=10)
        
        self.lbl_matches = tk.Label(self.stats_frame, text="Matches: 0/8", font=self.font_stats, bg=self.bg_color)
        self.lbl_matches.pack(side=tk.LEFT, padx=10)
        
        self.lbl_score = tk.Label(self.stats_frame, text="Score: 0", font=self.font_stats, bg=self.bg_color)
        self.lbl_score.pack(side=tk.LEFT, padx=10)
        
        self.lbl_timer = tk.Label(self.stats_frame, text="Time Left: 90s", font=self.font_stats, bg=self.bg_color, fg="red")
        self.lbl_timer.pack(side=tk.RIGHT, padx=10)
        
        # Game Board (Middle)
        board_frame = tk.Frame(self.root, bg=self.bg_color)
        board_frame.pack(expand=True)
        
        # Generate 4x4 Grid of Buttons
        for i in range(16):
            btn = tk.Button(board_frame, text="🐾", font=self.font_emoji, width=4, height=2, 
                            bg=self.card_hidden_color, relief="groove", bd=4,
                            command=lambda idx=i: self.on_card_click(idx))
            btn.grid(row=i//4, column=i%4, padx=8, pady=8)
            
            # Store card info
            self.cards.append({
                "btn": btn,
                "animal": self.animals[i],
                "state": "hidden" # States: 'hidden', 'flipped', 'matched'
            })
            
        # Controls (Bottom)
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=20)
        
        tk.Button(control_frame, text="Restart Game", font=("Helvetica", 12, "bold"), 
                  bg=self.btn_color, fg="white", command=self.start_game, 
                  padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="Return to Menu", font=("Helvetica", 12, "bold"), 
                  bg="#9370DB", fg="white", command=self.show_start_screen, 
                  padx=15, pady=5).pack(side=tk.LEFT, padx=10)

    # ==========================================
    # 2. GAME LOGIC: CLICK HANDLING & MATCHING
    # ==========================================

    def on_card_click(self, idx):
        """Handles the logic when a player clicks a card."""
        # Ignore clicks if waiting for cards to flip back, or if card is already revealed
        if not self.can_click or self.cards[idx]["state"] != "hidden":
            return
        
        # Flip the clicked card
        card = self.cards[idx]
        card["btn"].config(text=card["animal"], bg=self.card_visible_color)
        card["state"] = "flipped"
        
        if self.first_card_index is None:
            # This is the first card clicked in a turn
            self.first_card_index = idx
        else:
            # This is the second card clicked
            self.moves += 1
            self.can_click = False # Disable clicking until check is complete
            
            # Use root.after to create a slight delay before checking the match
            self.root.after(500, self.check_match, self.first_card_index, idx)
            self.first_card_index = None
            self.update_stats()

    def check_match(self, idx1, idx2):
        """Compares two flipped cards and applies scoring."""
        card1 = self.cards[idx1]
        card2 = self.cards[idx2]
        
        if card1["animal"] == card2["animal"]:
            # --- MATCH FOUND ---
            card1["state"] = "matched"
            card2["state"] = "matched"
            card1["btn"].config(bg=self.card_matched_color)
            card2["btn"].config(bg=self.card_matched_color)
            
            self.matches += 1
            self.score += 10
            
            # Check for win condition
            if self.matches == 8:
                self.game_over(win=True)
            else:
                self.can_click = True
                
        else:
            # --- WRONG PAIR ---
            card1["btn"].config(bg=self.card_error_color)
            card2["btn"].config(bg=self.card_error_color)
            self.score -= 3
            
            # Wait 800ms to show the red flash before hiding them again
            self.root.after(800, self.hide_cards, idx1, idx2)
            
        self.update_stats()

    def hide_cards(self, idx1, idx2):
        """Flips mismatched cards back face-down."""
        card1 = self.cards[idx1]
        card2 = self.cards[idx2]
        
        card1["state"] = "hidden"
        card2["state"] = "hidden"
        
        card1["btn"].config(text="🐾", bg=self.card_hidden_color)
        card2["btn"].config(text="🐾", bg=self.card_hidden_color)
        
        self.can_click = True # Re-enable clicking

    def update_stats(self):
        """Refreshes the top UI panel with current numbers."""
        self.lbl_moves.config(text=f"Moves: {self.moves}")
        self.lbl_matches.config(text=f"Matches: {self.matches}/8")
        self.lbl_score.config(text=f"Score: {self.score}")
        self.lbl_timer.config(text=f"Time Left: {self.time_left}s")

    # ==========================================
    # 3. TIMER SYSTEM
    # ==========================================

    def run_timer(self):
        """Decrements the 90-second timer every second."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_stats()
            # Schedule the next timer tick in 1000ms (1 second)
            self.timer_id = self.root.after(1000, self.run_timer)
        else:
            # Time has run out
            self.game_over(win=False)

    # ==========================================
    # 4. WIN/LOSE CONDITIONS & POPUPS
    # ==========================================

    def game_over(self, win):
        """Handles end-of-game logic and opens a custom celebratory/loss popup."""
        # Stop the timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        # Disable all remaining buttons
        self.can_click = False 
        
        # Create Custom Popup Window
        popup = tk.Toplevel(self.root)
        popup.geometry("350x300")
        popup.configure(bg="#FFF0F5") # Lavender Blush
        popup.grab_set() # Forces focus on popup
        
        if win:
            popup.title("🎉 You Won! 🎉")
            bonus = self.time_left * 2
            self.score += bonus
            self.update_stats() # Update one last time with bonus
            
            title_text = "🎉 Congratulations! 🎉"
            title_color = "#228B22" # Forest Green
            
            body_text = (f"Memory Master!\n"
                         f"You rescued all the adorable animals!\n\n"
                         f"Moves: {self.moves}\n"
                         f"Time Remaining: {self.time_left} seconds\n"
                         f"Bonus Points: +{bonus}\n"
                         f"Final Score: {self.score}")
        else:
            popup.title("⏰ Game Over")
            title_text = "⏰ Time's Up! ⏰"
            title_color = "#FF4500" # Orange Red
            
            body_text = ("You didn't find all the pairs.\n"
                         "Don't worry, the animals are waiting!\n\n"
                         "Try again to beat the clock!")
            
        # Render Popup Content
        tk.Label(popup, text=title_text, font=("Helvetica", 18, "bold"), 
                 fg=title_color, bg="#FFF0F5").pack(pady=(20, 10))
        
        tk.Label(popup, text=body_text, font=("Helvetica", 12), 
                 bg="#FFF0F5", fg=self.text_color).pack(pady=10)
        
        btn_frame = tk.Frame(popup, bg="#FFF0F5")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Play Again", font=("Helvetica", 12, "bold"),
                  bg=self.btn_color, fg="white", 
                  command=lambda: [popup.destroy(), self.start_game()]).pack(side=tk.LEFT, padx=10)
                  
        tk.Button(btn_frame, text="Menu", font=("Helvetica", 12, "bold"),
                  bg="#9370DB", fg="white", 
                  command=lambda: [popup.destroy(), self.show_start_screen()]).pack(side=tk.LEFT, padx=10)

# --- Main Application Loop ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PawPairQuest(root)
    root.mainloop()
