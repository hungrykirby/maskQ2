import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

import face2data
from Config import config

osc_type = input("raw osc(r), face osc(f) or no osc(n)")

'''
OSC
'''
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=12345,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)

def send(predict=0):
    if osc_type == "n":
        print("predict + no osc", predict)
        return
    elif osc_type == "r":
        print("predict + send predict osc", predict)
        msg = osc_message_builder.OscMessageBuilder(address="/predict")
        msg.add_arg(predict)
        msg = msg.build()
        client.send(msg)
    elif osc_type == "t": # Train
        msg = osc_message_builder.OscMessageBuilder(address="/key_send")
        print("Send : ", config.console_input_number)
        msg.add_arg(int(config.console_input_number))
        msg = msg.build()
        client.send(msg)
    elif osc_type == "f":
        command = face2data.detect_face_state(predict)
        if command is None:
            #print("command is not setted")
            return

        msg = {}
        builded_msg = {}
        addresses = {"/predict": predict, "/command": command}
        #print(addresses)
        for a in addresses.items():
            msg[a[0]] = osc_message_builder.OscMessageBuilder(address=a[0])
            #print(a[1])
            msg[a[0]].add_arg(str(a[1]))
            builded_msg[a[0]] = msg[a[0]].build()
            client.send(builded_msg[a[0]])
