import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd

np.random.seed(42)

# ---------------- DATA GENERATION ---------------- #
def generate_campaign_data():
    channels = ['Google Ads', 'Facebook', 'Instagram', 'LinkedIn', 'Email']
    data = {
        'Channel': channels,
        'Impressions': np.random.randint(5000, 20000, size=5),
        'Clicks': np.random.randint(500, 5000, size=5),
        'Conversions': np.random.randint(50, 500, size=5),
        'Cost': np.random.randint(10000, 50000, size=5),
        'Revenue': np.random.randint(20000, 100000, size=5)
    }
    return pd.DataFrame(data)

# ---------------- ANALYSIS ---------------- #
def analyze_data(df):
    df['CTR'] = (df['Clicks'] / df['Impressions']) * 100
    df['ConversionRate'] = (df['Conversions'] / df['Clicks']) * 100
    df['ROI'] = ((df['Revenue'] - df['Cost']) / df['Cost']) * 100
    return df

# ---------------- GUI ---------------- #
class MarketingAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Marketing Campaign Analyzer")
        self.root.geometry("900x500")

        title = tk.Label(
            root,
            text="📊Marketing Campaign Performance Analyzer",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        # IMPORTANT: column IDs simple rakho
        self.tree = ttk.Treeview(
            root,
            columns=("channel", "imp", "clicks", "conv",
                     "cost", "rev", "ctr", "cr", "roi"),
            show="headings"
        )

        # Headings (display text)
        self.tree.heading("channel", text="Channel")
        self.tree.heading("imp", text="Impressions")
        self.tree.heading("clicks", text="Clicks")
        self.tree.heading("conv", text="Conversions")
        self.tree.heading("cost", text="Cost (₹)")
        self.tree.heading("rev", text="Revenue (₹)")
        self.tree.heading("ctr", text="CTR (%)")
        self.tree.heading("cr", text="Conversion Rate (%)")
        self.tree.heading("roi", text="ROI (%)")

        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center", width=100)

        self.tree.pack(expand=True, fill="both", padx=10)

        btn = tk.Button(
            root,
            text="Analyze Campaign",
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.run_analysis
        )
        btn.pack(pady=10)

        self.summary = tk.Label(root, text="", font=("Arial", 12))
        self.summary.pack(pady=10)

    def run_analysis(self):
        df = generate_campaign_data()
        df = analyze_data(df)

        self.tree.delete(*self.tree.get_children())

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row['Channel'],
                int(row['Impressions']),
                int(row['Clicks']),
                int(row['Conversions']),
                f"₹{int(row['Cost'])}",
                f"₹{int(row['Revenue'])}",
                f"{row['CTR']:.2f}",
                f"{row['ConversionRate']:.2f}",
                f"{row['ROI']:.2f}"
            ))

        best = df.loc[df['ROI'].idxmax()]['Channel']
        worst = df.loc[df['ROI'].idxmin()]['Channel']

        self.summary.config(
            text=f"✅ Best Channel: {best}   |   ❌ Worst Channel: {worst}"
        )

# ---------------- RUN APP ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = MarketingAnalyzerGUI(root)
    root.mainloop()
