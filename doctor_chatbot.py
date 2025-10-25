import json
import difflib
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load advice data from JSON file
def load_advice_data(filename="doctor_advice.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Could not find {filename}. Please ensure it is in the same folder.")
        return {}
    except json.JSONDecodeError:
        messagebox.showerror("JSON Error", f"Failed to decode {filename}. Please check JSON format.")
        return {}

def find_best_match(user_input, advice_data, cutoff=0.4):
    lower_keys = {key.lower(): key for key in advice_data.keys()}
    user_input = user_input.lower().strip()

    close_matches = difflib.get_close_matches(user_input, lower_keys.keys(), n=1, cutoff=cutoff)
    if close_matches:
        return lower_keys[close_matches[0]]

    for key_lower, original_key in lower_keys.items():
        if user_input in key_lower:
            return original_key

    return None

def get_advice(user_input, advice_data):
    matched_key = find_best_match(user_input, advice_data)
    if matched_key:
        advice_list = advice_data[matched_key]
        advice = "\n".join(advice_list)
        if matched_key.lower() == user_input.lower().strip():
            return advice
        else:
            return f"Did you mean '{matched_key}'?\n\nAdvice:\n{advice}"
    else:
        return "Sorry, I couldn't find advice for that problem. Please try a different or more general symptom."

class DoctorChatbotGUI:
    def __init__(self, root, advice_data):
        self.root = root
        self.root.title("Doctor Chatbot - Health Advice Assistant")
        self.advice_data = advice_data

        # Window size and background color
        self.root.geometry("650x550")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)

        # Title label
        self.title_label = tk.Label(
            root,
            text="Doctor Chatbot",
            font=("Arial Black", 24, "bold"),
            fg="#2C3E50",
            bg="#f0f4f8"
        )
        self.title_label.pack(pady=(20,10))

        # Instructions label
        self.instruction_label = tk.Label(
            root,
            text="Enter your health problem below and click 'Get Advice'",
            font=("Segoe UI", 14),
            fg="#34495E",
            bg="#f0f4f8"
        )
        self.instruction_label.pack(pady=(0,15))

        # Input frame
        input_frame = tk.Frame(root, bg="#f0f4f8")
        input_frame.pack(pady=10)

        # Input box
        self.input_entry = tk.Entry(
            input_frame,
            width=45,
            font=("Segoe UI", 14),
            bd=2,
            relief="groove",
            highlightthickness=2,
            highlightcolor="#2980B9",
            highlightbackground="#95A5A6"
        )
        self.input_entry.pack(side=tk.LEFT, padx=(0,10))
        self.input_entry.bind("<Return>", self.on_get_advice)
        self.input_entry.focus_set()

        # Get Advice button
        self.get_advice_button = tk.Button(
            input_frame,
            text="Get Advice",
            command=self.on_get_advice,
            bg="#2980B9",
            fg="white",
            activebackground="#1F618D",
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.get_advice_button.pack(side=tk.LEFT)

        # Chat frame with padding and background
        chat_frame = tk.Frame(root, bg="#ecf0f1")
        chat_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Chat display scrolledtext
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            width=75,
            height=20,
            font=("Segoe UI", 12),
            state=tk.DISABLED,
            wrap=tk.WORD,
            bd=0,
            relief=tk.FLAT,
            bg="white",
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Initialize welcome message centered
        self.display_message("Doctor Chatbot", 
            "Hello! Please type your health problem above and I will try to give you advice.", 
            center=True)

    def display_message(self, sender, message, center=False):
        self.chat_display.config(state=tk.NORMAL)
        if center:
            centered_text = "\n".join(line.center(70) for line in message.split('\n'))
            self.chat_display.insert(tk.END, f"{sender}:\n{centered_text}\n\n")
        else:
            self.chat_display.insert(tk.END, f"{sender}:\n{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def on_get_advice(self, event=None):
        user_text = self.input_entry.get().strip()
        if not user_text:
            messagebox.showinfo("Input Required", "Please enter a health problem to get advice.")
            return
        self.display_message("You", user_text)
        advice = get_advice(user_text, self.advice_data)
        self.display_message("Doctor Chatbot", advice, center=True)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()

def main():
    advice_data = load_advice_data()
    if not advice_data:
        return
    root = tk.Tk()
    gui = DoctorChatbotGUI(root, advice_data)
    root.mainloop()

if __name__ == "__main__":
    main()
