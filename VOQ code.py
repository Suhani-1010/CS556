from collections import deque

packets = [
    ("p1",0,0,0),("p2",0,0,1),("p3",0,1,0),("p4",0,1,2),("p5",0,2,0),
    ("p6",1,0,2),("p7",1,2,1),
    ("p8",2,1,1),("p9",2,2,2),
    ("p10",3,0,1),("p11",3,1,0),("p12",3,2,1),
    ("p13",4,0,0),("p14",4,1,2),("p15",4,2,2),
    ("p16",5,0,2),("p17",5,1,1),("p18",5,2,0)
]

def voq():
    queues = [[deque() for _ in range(3)] for _ in range(3)]
    remaining = packets.copy()

    time, served = 0, 0

    print("\n VOQ ")

    while served < len(packets):
        print(f"\nTime {time}")

        # arrivals
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]][pkt[3]].append(pkt)
                print(f"Arrival: {pkt}")
                remaining.remove(pkt)

        used_inputs, used_outputs = set(), set()
        sent = []

        # greedy matching
        for i in range(3):
            for o in range(3):
                if queues[i][o] and i not in used_inputs and o not in used_outputs:
                    pkt = queues[i][o].popleft()
                    used_inputs.add(i)
                    used_outputs.add(o)
                    sent.append(pkt[0])
                    served += 1

        print("Sent:", sent if sent else "None")
        time += 1

    print("Total Time:", time)

voq()