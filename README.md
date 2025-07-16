# Predicting DDoS Attacks of Asian Countries
An AI/ML-based desktop application nuilt with python to monitor and predict Distributed Denial of Service (DDoS) attacks across Asian countries using historical data.
Utilized Linear Regression, Scikit-learn, and Pandas for future threat prediction, dynamic threat level assignment, and real-time visualization with Matplotlib.

# Features

# View Threat Data:
Displays full dataset in a styled, scrollable table
Includes columns: Year, Country, Attack Type, and Number of Attacks

# Smart Filtering:
Sort data by any selected column (ascending or descending)
Apply secondary search within filtered results
Results update live in the interface

# Future Threat Prediction:
Predicts attacks for 2025–2029 using Linear Regression
Assigns threat levels (Low, Medium, High) based on dynamic thresholds
Results shown in table and graph
Option to export predictions to CSV

# Historical Pattern Analysis
Plots year-wise attack trends (2019–2024) for each country
Visual comparison using color-coded line graphs

# Top Attack Types:
Shows most frequent attack type for each country
Includes number of occurrences

# Live Attack Monitor (Simulated):
Displays simulated real-time stats (total and active attacks)
Highlights top target country
Animated attack intensity graph over 24 hours

# Technologies Used:
Python 3
Tkinter (GUI)
Pandas (data handling)
Matplotlib (visualization)
Scikit-learn (prediction model)
NumPy (numerical computation)
Threading (animation and updates)

# How to Run
Install dependencies:
pip install pandas matplotlib scikit-learn
Place your dataset (fake_ddos_data.csv) in the correct file path (adjust in process_data() if needed)

# Run the project:
python file.py

# License
This project is for educational and personal use. Feel free to fork and modify for non-commercial purposes.

# Author
Waariha Asim
github: github.com/Wariha-Asim 
linked in: linkedin.com/in/warihaasim 


