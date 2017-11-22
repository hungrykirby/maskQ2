import collections

from Config import config
#import StateDate #これはモード変更をして文字入力をするためのコードであり，今回は不要となる

states_list = []
len_max_list = 2
len_all_state = 100
from_define_state = 70 #100フレーム後から判定を始める

history_commands = []

mode_list = ["no input", "words", "number", "others", "move", "delete", "read"]
command_list = ["normal", "smile", "surprised", "right", "left"]
add_modes_count = len(mode_list)
state_face = {
    "smile": False,
    "surprised": False,
    "normal": True,
}

def detect_face_state(predict):
    if len(states_list) > len_all_state:
        del(states_list[0:from_define_state])

    states_list.append(predict)

    if len(states_list) == len_all_state:
        count_dict = collections.Counter(states_list[len(states_list) - from_define_state:len(states_list) - 1])
        command_num = count_dict.most_common(1)[0][0]
        command = command_list[command_num]
        '''
        連続でsmileやsurprisedが出る確率は低そう
        '''
        #
        if command == "smile" or command == "surprised":
            if len(history_commands) > 1 and command == history_commands[len(history_commands) - 1]:
                command = "normal"
        #
        one_bool(command)
        print(state_face, command)
        history_commands.append(command)
        if len(history_commands) > 3:
            history_commands.pop(0)

        return command

def one_bool(command):
    if command != "right" and command != "left":
        for sf in state_face:
            state_face[sf] = False
        if command in state_face.keys():
            state_face[command] = True
        #print(state_face)

my_round=lambda x:(x*2+1)//2
