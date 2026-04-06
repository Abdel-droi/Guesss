# my guessing game project lol
# took me a long time but it worked !
#dont judge the code pls

import random
import time
import tkinter as tk

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_primes(a, b):
    return [n for n in range(a, b+1) if is_prime(n)]

def get_evens(a, b):
    return [n for n in range(a, b+1) if n % 2 == 0]

ROUNDS = [
    {"name": "Round 1: Lets gooo 🚀", "desc": "just guess a number between 1 and 30 (easy mode)", "type": "normal", "min": 1, "max": 30},
    {"name": "Round 2: Even numbers only 🔢", "desc": "guess an EVEN number between -10 and 20 (no odd numbers!!)", "type": "even", "min": -10, "max": 20},
    {"name": "Round 3: BIG BRAIN time 🧠", "desc": "guess a PRIME number between 1 and 30 (gl lmao)", "type": "prime", "min": 1, "max": 30},
]

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Guesss 🎯")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.current_round = 0
        self.scores = []
        self.number = None
        self.start_time = None
        self.attempts = 0
        self.timer_id = None

        self.build_ui()
        self.start_round()

    def build_ui(self):
        tk.Label(self.root, text="🎯 Guesss", font=("Arial", 26, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=20)

        self.round_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"),
                                    bg="#1e1e2e", fg="#89b4fa")
        self.round_label.pack()

        self.desc_label = tk.Label(self.root, text="", font=("Arial", 13),
                                   bg="#1e1e2e", fg="#a6e3a1")
        self.desc_label.pack(pady=5)

        # timer (this was so hard to make work omg)
        self.timer_label = tk.Label(self.root, text="⏱️ 0.00s", font=("Arial", 13),
                                    bg="#1e1e2e", fg="#f38ba8")
        self.timer_label.pack()

        self.attempts_label = tk.Label(self.root, text="Attempts: 0", font=("Arial", 12),
                                       bg="#1e1e2e", fg="#cdd6f4")
        self.attempts_label.pack()

        # this shows hints and stuff
        self.message_label = tk.Label(self.root, text="", font=("Arial", 17, "bold"),
                                      bg="#1e1e2e", fg="#fab387", wraplength=650)
        self.message_label.pack(pady=20)

        self.input_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.input_frame.pack()

        self.entry = tk.Entry(self.input_frame, font=("Arial", 18), width=10,
                              justify="center", bg="#313244", fg="#cdd6f4",
                              insertbackground="#cdd6f4", relief="flat")
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.check_guess())  # press enter = guess

        tk.Button(self.input_frame, text="Guess!", font=("Arial", 13, "bold"),
                  bg="#89b4fa", fg="#1e1e2e", relief="flat", padx=15, pady=5,
                  command=self.check_guess, cursor="hand2").pack(side="left")

        self.next_btn = tk.Button(self.root, text="Next Round ➡️", font=("Arial", 13, "bold"),
                                  bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=20, pady=8,
                                  command=self.next_round, cursor="hand2")

        self.score_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.score_frame.pack(pady=10)

    def start_round(self):
        r = ROUNDS[self.current_round]

        # pick the number depending on round type
        if r["type"] == "normal":
            self.number = random.randint(r["min"], r["max"])
        elif r["type"] == "even":
            self.number = random.choice(get_evens(r["min"], r["max"]))
        elif r["type"] == "prime":
            self.number = random.choice(get_primes(r["min"], r["max"]))

        self.attempts = 0
        self.start_time = time.time()

        self.round_label.config(text=r["name"])
        self.desc_label.config(text=r["desc"])
        self.message_label.config(text="type ur guess and hit enter!!", fg="#fab387")
        self.attempts_label.config(text="Attempts: 0")
        self.timer_label.config(text="⏱️ 0.00s")

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.next_btn.pack_forget()

        self.update_timer()

    # updates the timer every 50ms (hope this doesnt lag lol)
    def update_timer(self):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"⏱️ {elapsed:.2f}s")
            self.timer_id = self.root.after(50, self.update_timer)

    def check_guess(self):
        try:
            x = int(self.entry.get())
        except ValueError:
            self.message_label.config(text="bro that's not even a number 💀", fg="#f38ba8")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.entry.delete(0, tk.END)
        diff = abs(x - self.number)

        if x == self.number:
            elapsed = time.time() - self.start_time
            self.start_time = None
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.scores.append({"round": ROUNDS[self.current_round]["name"],
                                 "time": elapsed, "attempts": self.attempts})
            self.message_label.config(
                text=f"YESSS 🎉 it was {self.number}!!\n⏱️ {elapsed:.2f}s — {self.attempts} attempts",
                fg="#a6e3a1")
            self.entry.config(state="disabled")
            label = "see my score 🏆" if self.current_round == len(ROUNDS) - 1 else "Next Round ➡️"
            self.next_btn.config(text=label)
            self.next_btn.pack(pady=10)
        elif diff <= 3:
            self.message_label.config(text="🔥 BRO UR SO CLOSE!!!", fg="#fab387")
        elif diff <= 8:
            self.message_label.config(text="♨️ getting warmer...", fg="#f9e2af")
        elif x > self.number:
            self.message_label.config(text="📉 too high!! go lower", fg="#89dceb")
        else:
            self.message_label.config(text="📈 too low!! go higher", fg="#89dceb")

    def next_round(self):
        self.current_round += 1
        for w in self.score_frame.winfo_children():
            w.destroy()
        if self.current_round >= len(ROUNDS):
            self.show_final_score()
        else:
            self.start_round()

    def show_final_score(self):
        self.round_label.config(text="🏆 ur done!!")
        self.desc_label.config(text="here's how u did lol")
        self.message_label.config(text="")
        self.timer_label.config(text="")
        self.attempts_label.config(text="")
        self.input_frame.pack_forget()
        self.next_btn.pack_forget()

        total_time = sum(s["time"] for s in self.scores)
        for s in self.scores:
            tk.Label(self.score_frame,
                     text=f"✅ {s['round']} — {s['time']:.2f}s | {s['attempts']} attempts",
                     font=("Arial", 12), bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", padx=30)

        tk.Label(self.score_frame, text=f"\ntotal time: {total_time:.2f}s",
                 font=("Arial", 15, "bold"), bg="#1e1e2e", fg="#f9e2af").pack()

        tk.Button(self.score_frame, text="🔄 play again??", font=("Arial", 13, "bold"),
                  bg="#89b4fa", fg="#1e1e2e", relief="flat", padx=20, pady=8,
                  command=self.restart, cursor="hand2").pack(pady=20)

    def restart(self):
        self.current_round = 0
        self.scores = []
        self.input_frame.pack()
        for w in self.score_frame.winfo_children():
            w.destroy()
        self.start_round()

root = tk.Tk()
Game(root)
root.mainloop()