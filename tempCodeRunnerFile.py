import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import numpy as np
from random import randint
import time
import threading

# Dark theme colors
BG_COLOR = "#1e1e1e"  # Dark background
FG_COLOR = "#ffffff"  # White text
ACCENT_COLOR = "#4a6fa5"  # Blue accent
HIGHLIGHT_COLOR = "#2d5985"  # Darker blue for highlights
DANGER_COLOR = "#d9534f"  # Red for important elements
SUCCESS_COLOR = "#5cb85c"  # Green for positive actions     
ENTRY_BG = "#2d2d2d"  # Darker background for entry widgets
TREE_BG = "#252526"  # Background for treeview
TREE_FG = "#d4d4d4"  # Text color for treeview
TREE_SEL = "#3e3e42"  # Selection color for treeview

# Set matplotlib style to dark
plt.style.use('dark_background')

# Load and process the dataset
def process_data():
    # Create sample data if file doesn't exist
    data = {
        "Country": ["India", "Pakistan", "China", "Japan", "Bangladesh"] * 5,
        "Year": [2020, 2020, 2020, 2020, 2020, 
                2021, 2021, 2021, 2021, 2021,
                2022, 2022, 2022, 2022, 2022,
                2023, 2023, 2023, 2023, 2023,
                2024, 2024, 2024, 2024, 2024],
        "Attacks": [45, 32, 78, 23, 12,
                   52, 38, 85, 27, 15,
                   60, 42, 92, 30, 18,
                   65, 48, 105, 35, 22,
                   70, 55, 115, 40, 25],
        "Attack_Type": ["Volumetric", "Protocol", "Application", "Volumetric", "Protocol"] * 5
    }
    df = pd.DataFrame(data)
    return df

def show_data():
    new_win = tk.Toplevel(root)
    new_win.title("Asian DDoS Data - Security Dashboard")
    new_win.geometry("1000x500")
    new_win.configure(bg=BG_COLOR)

    df = process_data()
    frame = tk.Frame(new_win, bg=BG_COLOR)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create custom style for treeview
    style = ttk.Style()
    style.configure("Custom.Treeview", 
                   background=TREE_BG, 
                   foreground=TREE_FG,
                   fieldbackground=TREE_BG)
    style.map("Custom.Treeview", 
              background=[('selected', TREE_SEL)],
              foreground=[('selected', FG_COLOR)])

    tree = ttk.Treeview(frame, columns=list(df.columns), show="headings", style="Custom.Treeview")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

def filter_data():
    new_win = tk.Toplevel(root)
    new_win.title("Smart Filter - Security Dashboard")
    new_win.geometry("600x400")
    new_win.configure(bg=BG_COLOR)

    df = process_data()

    selected_column = tk.StringVar()
    sort_order = tk.StringVar(value="Ascending")

    tk.Label(new_win, text="Select Column:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    column_dropdown = ttk.Combobox(new_win, textvariable=selected_column, values=list(df.columns), state="readonly", width=30)
    column_dropdown.pack()

    tk.Label(new_win, text="Sort Order:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    sort_dropdown = ttk.Combobox(new_win, textvariable=sort_order, values=["Ascending", "Descending"], state="readonly", width=30)
    sort_dropdown.pack()

    def apply_filter():
        col = selected_column.get()
        sort = sort_order.get()

        if col:
            filtered_df = df.sort_values(by=col, ascending=(sort == "Ascending"))

            result_win = tk.Toplevel(new_win)
            result_win.title(f"Filtered Data - {col} - {sort}")
            result_win.geometry("1000x600")
            result_win.configure(bg=BG_COLOR)

            secondary_value = tk.StringVar()
            search_column = tk.StringVar()

            tk.Label(result_win, text="Search inside results:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
            second_search_entry = tk.Entry(result_win, textvariable=secondary_value, font=("Arial", 12), 
                                         width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR)
            second_search_entry.pack(pady=5)

            tk.Label(result_win, text="Select Attribute for Search:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
            attribute_dropdown = ttk.Combobox(result_win, textvariable=search_column, 
                                             values=list(filtered_df.columns), state="readonly", width=30)
            attribute_dropdown.pack(pady=5)

            # Create frame for treeview and scrollbars
            tree_frame = tk.Frame(result_win, bg=BG_COLOR)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            tree = ttk.Treeview(tree_frame, columns=list(filtered_df.columns), show="headings", style="Custom.Treeview")
            for c in filtered_df.columns:
                tree.heading(c, text=c)
                tree.column(c, width=150, anchor="center")

            for _, row in filtered_df.iterrows():
                tree.insert("", tk.END, values=row.tolist())

            scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            tree.pack(fill=tk.BOTH, expand=True)

            def second_level_filter(*args):
                value = secondary_value.get().lower()
                selected_attr = search_column.get()

                if value and selected_attr:
                    sub_df = filtered_df[filtered_df[selected_attr].astype(str).str.lower().str.contains(value)]
                else:
                    sub_df = filtered_df

                for i in tree.get_children():
                    tree.delete(i)
                for _, row in sub_df.iterrows():
                    tree.insert("", tk.END, values=row.tolist())

            second_search_entry.bind("<KeyRelease>", second_level_filter)
            attribute_dropdown.bind("<<ComboboxSelected>>", second_level_filter)

    tk.Button(new_win, text="Apply Filter", command=apply_filter, font=("Arial", 12), 
             bg=ACCENT_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR).pack(pady=20)

def future_prediction():
    new_win = tk.Toplevel(root)
    new_win.title("Threat Prediction - Security Dashboard")
    new_win.geometry("700x500")
    new_win.configure(bg=BG_COLOR)

    df = process_data()

    # Dropdown for selecting country
    selected_country = tk.StringVar()

    tk.Label(new_win, text="Select Country:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
    country_dropdown = ttk.Combobox(new_win, textvariable=selected_country, 
                                  values=["India", "Pakistan", "China", "Japan", "Bangladesh"], 
                                  state="readonly", width=30)
    country_dropdown.pack()

    prediction_heading = tk.Label(new_win, text="", font=("Arial", 16, "bold"), 
                                bg=BG_COLOR, fg=DANGER_COLOR)
    prediction_heading.pack(pady=10)

    # Frame for buttons to prevent duplication
    button_frame = tk.Frame(new_win, bg=BG_COLOR)
    button_frame.pack(pady=10)

    result_frame = tk.Frame(new_win, bg=BG_COLOR)
    result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def update_prediction_heading(*args):
        selected = selected_country.get()
        prediction_heading.config(text=f"PREDICTED DDOS THREATS FOR {selected.upper()}")

    country_dropdown.bind("<<ComboboxSelected>>", update_prediction_heading)

    def apply_prediction():
        country = selected_country.get()
        if not country:
            return

        country_df = df[df["Country"] == country]
        grouped = country_df.groupby("Year")["Attacks"].sum().reset_index()

        X = grouped["Year"].values.reshape(-1, 1)
        y = grouped["Attacks"].values

        model = LinearRegression()
        model.fit(X, y)

        future_years = np.array([2025, 2026, 2027, 2028, 2029]).reshape(-1, 1)
        future_predictions = model.predict(future_years)

        prediction_df = pd.DataFrame({
            "Year": [2025, 2026, 2027, 2028, 2029],
            "Predicted Attacks": future_predictions.astype(int)
        })

        # Add risk level column
        prediction_df["Risk Level"] = pd.cut(prediction_df["Predicted Attacks"],
                                           bins=[0, 30, 60, 100],
                                           labels=["Low", "Medium", "High"])

        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        # Clear previous buttons
        for widget in button_frame.winfo_children():
            widget.destroy()

        # Create frame for treeview and scrollbar
        tree_container = tk.Frame(result_frame, bg=BG_COLOR)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_container, columns=list(prediction_df.columns), show="headings", style="Custom.Treeview")
        for col in prediction_df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Color coding for risk levels
        tree.tag_configure('High', background=DANGER_COLOR)
        tree.tag_configure('Medium', background="#f0ad4e")  # Orange
        tree.tag_configure('Low', background=SUCCESS_COLOR)  # Green

        for _, row in prediction_df.iterrows():
            tree.insert("", tk.END, values=row.tolist(), tags=(row["Risk Level"],))

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)

        def show_predicted_graph():
            plt.figure(figsize=(10,6), facecolor='#2e2e2e')
            
            # Plot historical data
            plt.plot(grouped["Year"], grouped["Attacks"], color="#4a6fa5", marker="o", 
                    label="Historical Data", linewidth=2)
            
            # Plot future predictions
            plt.plot(future_years.flatten(), future_predictions, color=DANGER_COLOR, marker="o", 
                    linestyle="--", label="Threat Prediction", linewidth=2)
            
            # Add connecting line between last historical and first predicted point
            last_year = grouped["Year"].iloc[-1]
            last_attack = grouped["Attacks"].iloc[-1]
            first_pred_year = future_years[0][0]
            first_pred_attack = future_predictions[0]
            
            plt.plot([last_year, first_pred_year], [last_attack, first_pred_attack], 
                    color=SUCCESS_COLOR, linestyle=":", linewidth=2)
            
            plt.xlabel("Year", color='white')
            plt.ylabel("Number of Attacks", color='white')
            plt.title(f"DDoS Threat Assessment for {country}\n(Historical vs Predicted)", color='white')
            plt.legend(facecolor='#2e2e2e', edgecolor='#2e2e2e', labelcolor='white')
            plt.grid(True, color='#3e3e3e')
            
            # Set x-axis to show all years clearly
            all_years = list(grouped["Year"]) + list(future_years.flatten())
            plt.xticks(all_years, color='white')
            plt.yticks(color='white')
            
            # Set spines color
            for spine in plt.gca().spines.values():
                spine.set_color('#3e3e3e')
            
            plt.tight_layout()
            plt.show()

        def export_report():
            prediction_df.to_csv(f"DDoS_Prediction_{country}.csv", index=False)
            messagebox.showinfo("Success", "Report exported as CSV!")

        # Add new buttons
        graph_btn = tk.Button(button_frame, text="Show Threat Prediction Graph", 
                             command=show_predicted_graph, font=("Arial", 12),
                             bg=ACCENT_COLOR, fg=FG_COLOR, activebackground=HIGHLIGHT_COLOR)
        graph_btn.pack(side="left", padx=5)

        export_btn = tk.Button(button_frame, text="📥 Export Report", 
                             command=export_report, font=("Arial", 12),
                             bg=SUCCESS_COLOR, fg=FG_COLOR)
        export_btn.pack(side="left", padx=5)

    apply_btn = tk.Button(new_win, text="Analyze Threat", command=apply_prediction, 
                         font=("Arial", 12), bg=ACCENT_COLOR, fg=FG_COLOR, 
                         activebackground=HIGHLIGHT_COLOR)
    apply_btn.pack(pady=20)

def show_top_attack_types():
    df = process_data()
    # Group by Country and Attack_Type, count occurrences, and get the most frequent type
    top_attacks = df.groupby(['Country', 'Attack_Type']).size().reset_index(name='Count')
    top_attacks = top_attacks.loc[top_attacks.groupby('Country')['Count'].idxmax()]
    
    # Show in a new window
    popup = tk.Toplevel()
    popup.title("Top Attack Types by Country")
    popup.configure(bg=BG_COLOR)
    tk.Label(popup, text="Most Frequent Attack Types", font=("Arial", 16), bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=10)
    
    for _, row in top_attacks.iterrows():
        tk.Label(popup, 
                 text=f"{row['Country']}: {row['Attack_Type']} ({row['Count']} occurrences)", 
                 font=("Arial", 12), 
                 bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

def show_all_historical_graph():
    df = process_data()

    # Plot historical data for all countries
    plt.figure(figsize=(10,6), facecolor='#2e2e2e')
    countries = df["Country"].unique()
    
    # Color palette for countries
    colors = ['#4a6fa5', '#d9534f', '#5cb85c', '#f0ad4e', '#5bc0de']
    
    for idx, country in enumerate(countries):
        country_df = df[df["Country"] == country]
        grouped = country_df.groupby("Year")["Attacks"].sum().reset_index()
        plt.plot(grouped["Year"], grouped["Attacks"], color=colors[idx], 
                marker="o", label=country, linewidth=2)

    plt.xlabel("Year", color='white')
    plt.ylabel("Number of Attacks", color='white')
    plt.title("Historical DDoS Attack Patterns", color='white')
    plt.legend(facecolor='#2e2e2e', edgecolor='#2e2e2e', labelcolor='white')
    plt.grid(True, color='#3e3e3e')
    
    # Set spines color
    for spine in plt.gca().spines.values():
        spine.set_color('#3e3e3e')
    
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.tight_layout()
    plt.show()

class LiveDashboard:
    def __init__(self, parent):
        self.dash_frame = tk.Frame(parent, bg=BG_COLOR)
        self.dash_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header
        header = tk.Frame(self.dash_frame, bg=BG_COLOR)
        header.pack(fill="x", pady=10)
        
        tk.Label(header, text="🌐 LIVE DDoS ATTACK MONITOR", font=("Arial", 20, "bold"), 
                bg=BG_COLOR, fg=DANGER_COLOR).pack()
        
        # Create stats frame
        self.stats_frame = tk.Frame(self.dash_frame, bg=BG_COLOR)
        self.stats_frame.pack(fill="x", pady=10)
        
        # Initialize stats
        self.total_attacks = randint(5000, 10000)
        self.active_attacks = randint(50, 200)
        self.top_country = self.get_top_country()
        self.update_time = time.strftime('%H:%M:%S')
        
        self.update_stats()
        
        # Create figure for wave graph
        self.fig = plt.figure(figsize=(12, 6), facecolor=BG_COLOR)
        self.ax = self.fig.add_subplot(111)
        
        # Set dark theme for plot
        self.ax.set_facecolor(BG_COLOR)
        for spine in self.ax.spines.values():
            spine.set_color('#3e3e3e')
        self.ax.tick_params(colors=FG_COLOR)
        self.ax.xaxis.label.set_color(FG_COLOR)
        self.ax.yaxis.label.set_color(FG_COLOR)
        self.ax.title.set_color(FG_COLOR)
        
        # Countries data
        self.countries = ["India", "Pakistan", "China", "Japan", "Bangladesh"]
        self.colors = ['#4a6fa5', '#d9534f', '#5cb85c', '#f0ad4e', '#5bc0de']
        
        # Initialize empty lines
        self.lines = []
        for i, country in enumerate(self.countries):
            line, = self.ax.plot([], [], color=self.colors[i], label=country, linewidth=2)
            self.lines.append(line)
        
        # Set up plot
        self.ax.set_xlim(0, 24)  # 24 hours
        self.ax.set_ylim(0, 100)  # Attack intensity
        self.ax.set_xlabel("Time (Hours)", color=FG_COLOR)
        self.ax.set_ylabel("Attack Intensity", color=FG_COLOR)
        self.ax.set_title("Live DDoS Attack Waves by Country", color=FG_COLOR, pad=20)
        self.ax.legend(facecolor=TREE_SEL, labelcolor=FG_COLOR)
        self.ax.grid(True, color='#3e3e3e', alpha=0.5)
        
        # Embed plot in tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.dash_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Flag to control animation
        self.running = True
        
        # Start animation in a separate thread
        self.animation_thread = threading.Thread(target=self.start_animation, daemon=True)
        self.animation_thread.start()
    
    def get_top_country(self):
        df = process_data()
        country_attacks = df.groupby("Country")["Attacks"].sum().reset_index()
        return country_attacks.loc[country_attacks["Attacks"].idxmax()]["Country"]
    
    def update_stats(self):
        # Update random stats but keep top country based on actual data
        self.total_attacks += randint(1, 10)
        self.active_attacks = randint(50, 200)
        self.update_time = time.strftime('%H:%M:%S')
        
        stats = [
            f"🚨 Total Attacks Today: {self.total_attacks}",
            f"🔥 Active Attacks Now: {self.active_attacks}",
            f"🌍 Top Target: {self.top_country}",
            f"⏱ Last Updated: {self.update_time}"
        ]
        
        # Clear and update stats frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        for stat in stats:
            tk.Label(self.stats_frame, text=stat, font=("Arial", 12), 
                    bg=TREE_SEL, fg=FG_COLOR, padx=10, pady=5).pack(side="left", padx=10)
    
    def animate(self, i):
        if not self.running:
            return
        
        x = np.linspace(0, 24, 100)
        for j, line in enumerate(self.lines):
            # Generate wave-like data with random fluctuations
            y = 30 + 50 * np.sin(x/2 + i/5 + j) * np.random.normal(1, 0.1, len(x))
            line.set_data(x, y)
        
        # Update stats every 5 frames
        if i % 5 == 0:
            self.update_stats()
        
        return self.lines
    
    def start_animation(self):
        while self.running:
            for i in range(100):
                if not self.running:
                    break
                self.animate(i)
                self.canvas.draw()
                self.dash_frame.update()
                time.sleep(0.1)  # Match the original interval of 100ms
            self.canvas.draw()
    
    def stop_animation(self):
        self.running = False

# Create main window
root = tk.Tk()
root.title("Cyber Threat Analysis Dashboard")
root.geometry("1200x800")
root.configure(bg=BG_COLOR)

# Configure styles
style = ttk.Style()
style.theme_use('clam')

# Configure button style
style.configure('TButton', 
               font=('Arial', 12),
               foreground=FG_COLOR,
               background=ACCENT_COLOR,
               bordercolor=ACCENT_COLOR,
               lightcolor=ACCENT_COLOR,
               darkcolor=HIGHLIGHT_COLOR,
               padding=10)
style.map('TButton',
          background=[('active', HIGHLIGHT_COLOR)],
          foreground=[('active', FG_COLOR)])

# Configure combobox style
style.configure('TCombobox', 
               fieldbackground=ENTRY_BG,
               foreground=FG_COLOR,
               background=BG_COLOR,
               selectbackground=HIGHLIGHT_COLOR,
               selectforeground=FG_COLOR)

# Create main container
main_container = tk.Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True)

# Header frame
header_frame = tk.Frame(main_container, bg=BG_COLOR)
header_frame.pack(fill="x", pady=10)

# Logo and title
logo_frame = tk.Frame(header_frame, bg=BG_COLOR)
logo_frame.pack()

tk.Label(logo_frame, text="🔒", font=("Arial", 24), bg=BG_COLOR, fg=ACCENT_COLOR).pack(side="left")
welcome_label = tk.Label(logo_frame, text="Cyber Threat Analysis Dashboard", 
                        font=("Arial", 24, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
welcome_label.pack(side="left", padx=10)

# Subtitle
tk.Label(header_frame, text="DDoS Attack Monitoring & Prediction System", 
        font=("Arial", 14), fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)

# Create left panel for buttons
left_panel = tk.Frame(main_container, bg=BG_COLOR, width=200)
left_panel.pack(side="left", fill="y", padx=10, pady=10)

# Create buttons with consistent styling
btn1 = ttk.Button(left_panel, text="View Threat Data", command=show_data, width=20)
btn2 = ttk.Button(left_panel, text="Filter Threat Data", command=filter_data, width=20)
btn3 = ttk.Button(left_panel, text="Threat Prediction", command=future_prediction, width=20)
btn4 = ttk.Button(left_panel, text="Historical Patterns", command=show_all_historical_graph, width=20)
btn5 = ttk.Button(left_panel, text="Top Attack Types", command=show_top_attack_types, width=20)

btn1.pack(pady=10, ipady=5)
btn2.pack(pady=10, ipady=5)
btn3.pack(pady=10, ipady=5)
btn4.pack(pady=10, ipady=5)
btn5.pack(pady=10, ipady=5)

# Create right panel for live dashboard
right_panel = tk.Frame(main_container, bg=BG_COLOR)
right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Initialize live dashboard immediately
live_dash = LiveDashboard(right_panel)

# Footer
footer_frame = tk.Frame(root, bg=BG_COLOR)
footer_frame.pack(side="bottom", fill="x", pady=10)
tk.Label(footer_frame, text="© 2023 Cyber Security Analytics | For authorized use only", 
        font=("Arial", 10), fg=FG_COLOR, bg=BG_COLOR).pack()

# Handle window close event
def on_closing():
    live_dash.stop_animation()  # Stop the animation thread
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
