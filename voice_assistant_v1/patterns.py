import re

def get_best_patterns(data):
    return {
        re.compile(r"[\w\s]+ most goals"): data.get_player_most_goals,
        re.compile(r"[\w\s]+ most assists"): data.get_player_most_assists,
        re.compile(r"[\w\s]+ most points"): data.get_player_most_points,
        re.compile(r"[\w\s]+ best plus-minus"): data.get_player_most_PlusMinus,
        re.compile(r"[\w\s]+ most penalties in minutes"): data.get_player_most_PenaltiesInMinutes,
        re.compile(r"[\w\s]+ best points per game average"): data.get_player_most_PointsPerGame,
        re.compile(r"[\w\s]+ most points per game"): data.get_player_most_PointsPerGame
    }

def get_player_patterns(data):
    return {
        re.compile('which hand did [\w\s]+ shoot with'): lambda player: data.get_player_data_skater(player),
        re.compile('[\w\s]+ handed [\w\s]'): lambda player: data.get_player_data_skater(player),
        re.compile('[\w\s]+ position [\w\s]'): lambda player: data.get_player_data_pos(player),
        re.compile('[\w\s]+ position'): lambda player: data.get_player_data_pos(player),
        re.compile('[\w\s]+ games [\w\s]'): lambda player: data.get_player_data_GP(player),
        re.compile('[\w\s]+ games [\w\s]+ play'): lambda player: data.get_player_data_GP(player),
        re.compile('[\w\s]+ goals [\w\s]'): lambda player: data.get_player_data_Goals(player),
        re.compile('[\w\s]+ goals'): lambda player: data.get_player_data_Goals(player),
        re.compile('[\w\s]+ assists [\w\s]'): lambda player: data.get_player_data_Assists(player),
        re.compile('[\w\s]+ assists'): lambda player: data.get_player_data_Assists(player),
        re.compile('[\w\s]+ points [\w\s]'): lambda player: data.get_player_data_Points(player),
        re.compile('[\w\s]+ points'): lambda player: data.get_player_data_Points(player),
        re.compile('[\w\s]+ plus minus [\w\s]'): lambda player: data.get_player_data_PlusMinus(player),
        re.compile('[\w\s]+ plus minus'): lambda player: data.get_player_data_PlusMinus(player),
        re.compile('[\w\s]+ penalties'): lambda player: data.get_player_data_PIM(player),
        re.compile('[\w\s]+ penalties in minutes'): lambda player: data.get_player_data_PIM(player),
        re.compile('[\w\s]+ points per game [\w\s]'): lambda player: data.get_player_data_PPG(player),
        re.compile('[\w\s]+ points per game'): lambda player: data.get_player_data_PPG(player)
    }