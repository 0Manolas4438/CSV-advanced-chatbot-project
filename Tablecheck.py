import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CSVMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV check")
        self.df = None

        # UI Elements
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.query_label = tk.Label(root, text="Enter query for matching:")
        self.query_label.pack()
        self.query_entry = tk.Entry(root, width=80)
        self.query_entry.pack(pady=5)

        self.match_button = tk.Button(root, text="Find Closest Match", command=self.find_match)
        self.match_button.pack(pady=10)

        self.result_text = tk.Text(root, width=100, height=15)
        self.result_text.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            messagebox.showinfo("Success", f"Loaded CSV with {len(self.df)} rows.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{e}")

    def find_match(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please load a CSV first!")
            return
        
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a query!")
            return

        # Combine Keywords and Context for matching
        self.df['CombinedText'] = self.df['Keywords'].fillna('') + " " + self.df['Context'].fillna('')

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.df['CombinedText'])
        query_vec = vectorizer.transform([query])

        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        best_idx = similarities.argmax()

        best_row = self.df.iloc[best_idx]
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Best Match (Score: {similarities[best_idx]:.3f}):\n\n")
        for col in self.df.columns:
            if col != 'CombinedText':
                self.result_text.insert(tk.END, f"{col}: {best_row[col]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVMatcherApp(root)
    root.mainloop()
