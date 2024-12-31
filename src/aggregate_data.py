import pandas as pd
import os
import glob
import numpy as np

# Directory containing the downloaded files
data_dir = "data"

# Define data types for different categories
DTYPE_CONFIGS = {
    'skaters_season': {
        'Player': str,
        'Season': str,
        'Team': str,
        'S/C': str,
        'Pos': str,
        'GP': 'Int64',
        'G': 'Int64',
        'A': 'Int64',
        'P': 'Int64',
        '+/-': 'Int64',
        'PIM': 'Int64',
        'P/GP': float,
        'EVG': 'Int64',
        'EVP': 'Int64',
        'PPG': 'Int64',
        'PPP': 'Int64',
        'SHG': 'Int64',
        'SHP': 'Int64',
        'OTG': 'Int64',
        'GWG': 'Int64',
        'S': 'Int64',
        'S%': float,
        'TOI/GP': float,
        'FOW%': float
    },
    'skaters_alltime': {
        'Player': str,
        'S/C': str,
        'Pos': str,
        'GP': 'Int64',
        'G': 'Int64',
        'A': 'Int64',
        'P': 'Int64',
        '+/-': 'Int64',
        'PIM': 'Int64',
        'P/GP': float,
        'EVG': 'Int64',
        'EVP': 'Int64',
        'PPG': 'Int64',
        'PPP': 'Int64',
        'SHG': 'Int64',
        'SHP': 'Int64',
        'OTG': 'Int64',
        'GWG': 'Int64',
        'S': 'Int64',
        'S%': float,
        'TOI/GP': float,
        'FOW%': float
    },
    'teams_season': {
        'Team': str,
        'Season': str,
        'GP': 'Int64',
        'W': 'Int64',
        'L': 'Int64',
        'T': 'Int64',
        'OT': 'Int64',
        'P': 'Int64',
        'P%': float,
        'RW': 'Int64',
        'ROW': 'Int64',
        'S/O Win': float,
        'GF': 'Int64',
        'GA': 'Int64',
        'GF/GP': float,
        'GA/GP': float,
        'PP%': float,
        'PK%': float,
        'Net PP%': float,
        'Net PK%': float,
        'Shots/GP': float,
        'SA/GP': float,
        'FOW%': float
    },
    'teams_alltime': {
        'Team': str,
        'GP': 'Int64',
        'W': 'Int64',
        'L': 'Int64',
        'T': 'Int64',
        'OT': 'Int64',
        'P': 'Int64',
        'P%': float,
        'RW': 'Int64',
        'ROW': 'Int64',
        'S/O Win': float,
        'GF': 'Int64',
        'GA': 'Int64',
        'GF/GP': float,
        'GA/GP': float,
        'PP%': float,
        'PK%': float,
        'Net PP%': float,
        'Net PK%': float,
        'Shots/GP': float,
        'SA/GP': float,
        'FOW%': float
    },
    'goalies_season': {
        'Player': str,
        'Season': str,
        'Team': str,
        'S/C': str,
        'GP': 'Int64',
        'GS': 'Int64',
        'W': 'Int64',
        'L': 'Int64',
        'T': 'Int64',
        'OT': 'Int64',
        'SA': 'Int64',
        'Svs': 'Int64',
        'GA': 'Int64',
        'SV%': float,
        'GAA': float,
        'TOI': str,
        'SO': 'Int64',
        'G': 'Int64',
        'A': 'Int64',
        'P': 'Int64',
        'PIM': 'Int64'
    },
    'goalies_alltime': {
        'Player': str,
        'S/C': str,
        'GP': 'Int64',
        'GS': 'Int64',
        'W': 'Int64',
        'L': 'Int64',
        'T': 'Int64',
        'OT': 'Int64',
        'SA': 'Int64',
        'Svs': 'Int64',
        'GA': 'Int64',
        'SV%': float,
        'GAA': float,
        'TOI': str,
        'SO': 'Int64',
        'G': 'Int64',
        'A': 'Int64',
        'P': 'Int64',
        'PIM': 'Int64'
    }
}

def process_category(prefix, dtype_dict):
    excel_files = glob.glob(os.path.join(data_dir, f"{prefix}_*.xlsx"))
    if not excel_files:
        return None
        
    dfs = []
    for file in sorted(excel_files, key=lambda x: int(x.split('_')[-1].split('.')[0])):
        print(f"Reading file: {file}")
        df = pd.read_excel(file)
        
        for col in df.columns:
            if col in dtype_dict:
                try:
                    if dtype_dict[col] == 'Int64':
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), 
                                              errors='coerce').astype('Int64')
                    elif dtype_dict[col] == float:
                        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), 
                                              errors='coerce')
                    else:
                        df[col] = df[col].astype(dtype_dict[col])
                except Exception as e:
                    print(f"Warning converting {col}: {str(e)}")
        
        dfs.append(df)
    
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.drop_duplicates()
        
        # Save as CSV
        output_file = os.path.join(data_dir, f"{prefix}.csv")
        combined_df.to_csv(output_file, index=False)
        print(f"Saved {prefix} data to: {output_file}")
        
        # Delete Excel files
        for file in excel_files:
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {str(e)}")
        
        return combined_df
    return None

def main():
    categories = [
        ('skaters_alltime_regular', 'skaters_alltime'),
        ('skaters_alltime_playoffs', 'skaters_alltime'),
        ('skaters_current', 'skaters_season'),
        ('teams_alltime_regular', 'teams_alltime'),
        ('teams_alltime_playoffs', 'teams_alltime'),
        ('teams_current', 'teams_season'),
        ('goalies_alltime_regular', 'goalies_alltime'),
        ('goalies_alltime_playoffs', 'goalies_alltime'),
        ('goalies_current', 'goalies_season')
    ]
    
    for prefix, category_type in categories:
        print(f"\nProcessing {prefix}...")
        df = process_category(prefix, DTYPE_CONFIGS[category_type])
        if df is not None:
            print(f"Total rows in {prefix}: {len(df)}")

if __name__ == "__main__":
    main() 