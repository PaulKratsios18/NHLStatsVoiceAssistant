import json
import time
import requests
import re
import threading
import pyttsx3
import speech_recognition as sr


api_key = 'tz9zH6cCChp2'
projectToken = 't17PC8hVrsMp'
runToken = 'toj9Nprksma4'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        print(response.text)  # Add this line to inspect the response
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        data = json.loads(response.text)
        return data['Players']

    def get_player_most_goals(self):
        data = self.data
        g = int(data[-1]['Goals'])
        n = data[-1]['name']
        for content in data:
            if int(content['Goals']) > g:
                g = int(content['Goals'])
                n = content['name']
        return n + ' has the most goals, scoring ' + str(g)

    def get_player_most_assists(self):
        data = self.data
        a = int(data[-1]['Assists'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['Assists'].replace(',', '')) > a:
                a = int(content['Assists'].replace(",", ''))
                n = content['name']
        return n + ' has the most assists, with ' + str(a)

    def get_player_most_points(self):
        data = self.data
        p = int(data[-1]['Points'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['Points'].replace(',', '')) > p:
                p = int(content['Points'].replace(",", ''))
                n = content['name']
        return n + ' has the most points, with ' + str(p)

    def get_player_most_PlusMinus(self):
        data = self.data
        pm = int(data[-1]['PlusMinus'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['PlusMinus'].replace(",", '')) > pm:
                pm = int(content['PlusMinus'].replace(",", ''))
                n = content['name']
        return n + ' has the best plus minus, with a ' + str(pm)

    def get_player_most_PenaltiesInMinutes(self):
        data = self.data
        pim = int(data[-1]['PenaltiesInMinutes'].replace(',', ''))
        n = data[-1]['name']
        for content in data:
            if int(content['PenaltiesInMinutes'].replace(',', '')) > pim:
                pim = int(content['PenaltiesInMinutes'].replace(',', ''))
                n = content['name']
        return n + ' has the most penalty minutes, with ' + str(pim)

    def get_player_most_PointsPerGame(self):
        data = self.data
        ppg = float(data[-1]['PointsPerGame'])
        n = data[-1]['name']
        for content in data:
            if float(content['PointsPerGame']) > ppg:
                ppg = float(content['PointsPerGame'])
                n = content['name']
        return 'Morgan Geekie has the highest average points per game, with a ratio of 2.0. He scored a whopping total of four points in the two games he played in the NHL. The next highest player is ' + n + ' with a ' + str(
            ppg) + ' points per game average.'

    def get_player_data_skater(self, player):
        data = self.data
        hand = ''
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                if stuff['SkaterShoots'] == 'L':
                    hand = 'left'
                if stuff['SkaterShoots'] == 'R':
                    hand = 'right'
                return stuff['name'] + ' shoots ' + hand + 'handed'
        return '0'

    def get_player_data_pos(self, player):
        data = self.data
        pos = ''
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                if stuff['Position'] == 'L':
                    pos = 'leftwing'
                if stuff['Position'] == 'R':
                    pos = 'rightwing'
                if stuff['Position'] == 'C':
                    pos = 'center'
                if stuff['Position'] == 'D':
                    pos = 'defense'
                return stuff['name'] + ' plays ' + pos
        return '0'

    def get_player_data_GP(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has played' + stuff['GamesPlayed'] + ' games'
        return '0'

    def get_player_data_Goals(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' scored ' + stuff['Goals'] + ' goals'
        return '0'

    def get_player_data_Assists(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + stuff['Assists'] + ' assists'
        return '0'

    def get_player_data_Points(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + str(stuff['Points']) + ' points'
        return '0'

    def get_player_data_PlusMinus(self, player):
        data = self.data
        player = player.capitalize()
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has a plus minus of ' + stuff['PlusMinus']
        return '0'

    def get_player_data_PIM(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + stuff['PenaltiesInMinutes'] + ' penalty minutes'
        return '0'

    def get_player_data_PPG(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has an average of ' + stuff['PointsPerGame'] + ' points per game'
        return '0'

    def get_player_list(self):
        players = [p['name'].lower() for p in self.data]
        return players

    def update_data(self):
        response = requests.post('https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('Data Updated')
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('Exception:', e)
            speak('boogely boogely')

    return said.lower()


def main():
    print('Started Program')
    data = Data(api_key, projectToken)
    player_list = data.get_player_list()

    best_patterns = {
        re.compile(r"[\w\s]+ most goals"): data.get_player_most_goals,
        re.compile(r"[\w\s]+ most assists"): data.get_player_most_assists,
        re.compile(r"[\w\s]+ most points"): data.get_player_most_points,
        re.compile(r"[\w\s]+ best plus-minus"): data.get_player_most_PlusMinus,
        re.compile(r"[\w\s]+ most penalties in minutes"): data.get_player_most_PenaltiesInMinutes,
        re.compile(r"[\w\s]+ best points per game average"): data.get_player_most_PointsPerGame,
        re.compile(r"[\w\s]+ most points per game"): data.get_player_most_PointsPerGame
    }

    player_patterns = {
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

    update_command = 'update'
    stop_command = 'stop'


api_key = 'tz9zH6cCChp2'
projectToken = 't17PC8hVrsMp'
runToken = 'tP23WSjdnVC2'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        print(response.text)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        data = json.loads(response.text)
        return data['Players']

    def get_player_most_goals(self):
        data = self.data
        g = int(data[-1]['Goals'])
        n = data[-1]['name']
        for content in data:
            if int(content['Goals']) > g:
                g = int(content['Goals'])
                n = content['name']
        return n + ' has the most goals, scoring ' + str(g)

    def get_player_most_assists(self):
        data = self.data
        a = int(data[-1]['Assists'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['Assists'].replace(',', '')) > a:
                a = int(content['Assists'].replace(",", ''))
                n = content['name']
        return n + ' has the most assists, with ' + str(a)

    def get_player_most_points(self):
        data = self.data
        p = int(data[-1]['Points'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['Points'].replace(',', '')) > p:
                p = int(content['Points'].replace(",", ''))
                n = content['name']
        return n + ' has the most points, with ' + str(p)

    def get_player_most_PlusMinus(self):
        data = self.data
        pm = int(data[-1]['PlusMinus'].replace(",", ''))
        n = data[-1]['name']
        for content in data:
            if int(content['PlusMinus'].replace(",", '')) > pm:
                pm = int(content['PlusMinus'].replace(",", ''))
                n = content['name']
        return n + ' has the best plus minus, with a ' + str(pm)

    def get_player_most_PenaltiesInMinutes(self):
        data = self.data
        pim = int(data[-1]['PenaltiesInMinutes'].replace(',', ''))
        n = data[-1]['name']
        for content in data:
            if int(content['PenaltiesInMinutes'].replace(',', '')) > pim:
                pim = int(content['PenaltiesInMinutes'].replace(',', ''))
                n = content['name']
        return n + ' has the most penalty minutes, with ' + str(pim)

    def get_player_most_PointsPerGame(self):
        data = self.data
        ppg = float(data[-1]['PointsPerGame'])
        n = data[-1]['name']
        for content in data:
            if float(content['PointsPerGame']) > ppg:
                ppg = float(content['PointsPerGame'])
                n = content['name']
        return 'Morgan Geekie has the highest average points per game, with a ratio of 2.0. He scored a whopping total of four points in the two games he played in the NHL. The next highest player is ' + n + ' with a ' + str(
            ppg) + ' points per game average.'

    def get_player_data_skater(self, player):
        data = self.data
        hand = ''
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                if stuff['SkaterShoots'] == 'L':
                    hand = 'left'
                if stuff['SkaterShoots'] == 'R':
                    hand = 'right'
                return stuff['name'] + ' shoots ' + hand + 'handed'
        return '0'

    def get_player_data_pos(self, player):
        data = self.data
        pos = ''
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                if stuff['Position'] == 'L':
                    pos = 'leftwing'
                if stuff['Position'] == 'R':
                    pos = 'rightwing'
                if stuff['Position'] == 'C':
                    pos = 'center'
                if stuff['Position'] == 'D':
                    pos = 'defense'
                return stuff['name'] + ' plays ' + pos
        return '0'

    def get_player_data_GP(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has played' + stuff['GamesPlayed'] + ' games'
        return '0'

    def get_player_data_Goals(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' scored ' + stuff['Goals'] + ' goals'
        return '0'

    def get_player_data_Assists(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + stuff['Assists'] + ' assists'
        return '0'

    def get_player_data_Points(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + str(stuff['Points']) + ' points'
        return '0'

    def get_player_data_PlusMinus(self, player):
        data = self.data
        player = player.capitalize()
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has a plus minus of ' + stuff['PlusMinus']
        return '0'

    def get_player_data_PIM(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has ' + stuff['PenaltiesInMinutes'] + ' penalty minutes'
        return '0'

    def get_player_data_PPG(self, player):
        data = self.data
        for stuff in data:
            if stuff['name'].lower() == player.lower():
                return stuff['name'] + ' has an average of ' + stuff['PointsPerGame'] + ' points per game'
        return '0'

    def get_player_list(self):
        players = [p['name'].lower() for p in self.data]
        return players

    def update_data(self):
        response = requests.post('https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('Data Updated')
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('Exception:', e)
            speak('boogely boogely')

    return said.lower()


def main():
    print('Started Program')
    data = Data(api_key, projectToken)
    player_list = data.get_player_list()

    best_patterns = {
        re.compile(r"[\w\s]+ most goals"): data.get_player_most_goals,
        re.compile(r"[\w\s]+ most assists"): data.get_player_most_assists,
        re.compile(r"[\w\s]+ most points"): data.get_player_most_points,
        re.compile(r"[\w\s]+ best plus-minus"): data.get_player_most_PlusMinus,
        re.compile(r"[\w\s]+ most penalties in minutes"): data.get_player_most_PenaltiesInMinutes,
        re.compile(r"[\w\s]+ best points per game average"): data.get_player_most_PointsPerGame,
        re.compile(r"[\w\s]+ most points per game"): data.get_player_most_PointsPerGame
    }

    player_patterns = {
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

    update_command = 'update'
    stop_command = 'stop'

    while True:
        print('Listening...')
        text = get_audio()
        print(text)
        result = None

        for pattern, func in player_patterns.items():
            if pattern.match(text):
                words = set(text.split(' '))
                for player in player_list:
                    if player.split(' ')[0] in words and player.split(' ')[1] in words:
                        result = func(player)
                        break

        for pattern, func in best_patterns.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            speak(result)
            print(result)

        if text == update_command:
            result = 'Data is being updated. This may take a moment.'
            speak(result)
            print(result)
            data.update_data()

        if text.find(stop_command) != -1:
            speak('Exit')
            print('Exit')
            break


data = Data(api_key, projectToken)
main()
