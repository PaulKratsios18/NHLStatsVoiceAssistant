import pandas as pd
from typing import Dict, List
import os

class NHLDataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.dataframes: Dict[str, pd.DataFrame] = {}
        self.load_all_data()
        
    def load_all_data(self):
        # Load all CSV files
        categories = [
            'skaters_alltime_regular',
            'skaters_alltime_playoffs',
            'skaters_current',
            'teams_alltime_regular',
            'teams_alltime_playoffs',
            'teams_current',
            'goalies_alltime_regular',
            'goalies_alltime_playoffs',
            'goalies_current'
        ]
        
        for category in categories:
            file_path = os.path.join(self.data_dir, f"{category}.csv")
            if os.path.exists(file_path):
                self.dataframes[category] = pd.read_csv(file_path)
    
    def create_context_string(self) -> str:
        """Creates a formatted string containing key statistics for LLM context"""
        context = []
        
        # Add skater stats
        if 'skaters_alltime_regular' in self.dataframes:
            top_scorers = self.dataframes['skaters_alltime_regular'].nlargest(10, 'P')
            context.append("Top 10 NHL All-Time Points Leaders (Regular Season):")
            for _, player in top_scorers.iterrows():
                context.append(f"{player['Player']}: {player['P']} points ({player['G']} goals, {player['A']} assists) in {player['GP']} games")
        
        # Add similar sections for other key statistics...
        
        return "\n".join(context) 