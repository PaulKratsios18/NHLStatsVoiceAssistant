import time
import threading
from voice_assistant_v1.data import Data
from voice_assistant_v1.speech import speak, get_audio
from voice_assistant_v1.patterns import get_best_patterns, get_player_patterns

api_key = 'tz9zH6cCChp2'
projectToken = 't17PC8hVrsMp'

def main():
    print('Started Program')
    data = Data(api_key, projectToken)
    player_list = data.get_player_list()

    best_patterns = get_best_patterns(data)
    player_patterns = get_player_patterns(data)

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
            speak('Stopping the program.')
            break

if __name__ == "__main__":
    main()
