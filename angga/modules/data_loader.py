import pandas as pd

def load_data():
    # Load the dataset (assuming it's in CSV format)
    data = pd.read_csv("data/data_asia.csv")
    
    # Remove columns that start with 'ln' (log-transformed columns)
    data = data.loc[:, ~data.columns.str.startswith('ln')]
    
    return data
