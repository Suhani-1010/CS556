
# GRAPH 2: BACKLOG VS TIME

from collections import deque
import matplotlib.pyplot as plt

packets = [
    ("p1",0,0,0),("p2",0,0,1),("p3",0,1,0),("p4",0,1,2),("p5",0,2,0),
    ("p6",1,0,2),("p7",1,2,1),
    ("p8",2,1,1),("p9",2,2,2),
    ("p10",3,0,1),("p11",3,1,0),("p12",3,2,1),
    ("p13",4,0,0),("p14",4,1,2),("p15",4,2,2),
    ("p16",5,0,2),("p17",5,1,1),("p18",5,2,0)
]

N = 3


def simulate(mode):
    if mode == "fifo":
        queues = [deque() for _ in range(N)]
    else:
        queues = [[deque() for _ in range(N)] for _ in range(N)]

    remaining = packets.copy()
    time = served = 0
    backlog = []

    input_ptr = [0]*N
    output_ptr = [0]*N

    while served < len(packets):

        for pkt in remaining[:]:
            if pkt[1] == time:
                if mode == "fifo":
                    queues[pkt[2]].append(pkt)
                else:
                    queues[pkt[2]][pkt[3]].append(pkt)
                remaining.remove(pkt)

        used_inputs, used_outputs = set(), set()

        if mode == "fifo":
            front = [q[0] for q in queues if q]
            front.sort(key=lambda x: x[1])

            for pkt in front:
                if pkt[3] not in used_outputs:
                    queues[pkt[2]].popleft()
                    used_outputs.add(pkt[3])
                    served += 1

        elif mode == "voq":
            for i in range(N):
                for o in range(N):
                    if queues[i][o] and i not in used_inputs and o not in used_outputs:
                        queues[i][o].popleft()
                        used_inputs.add(i)
                        used_outputs.add(o)
                        served += 1

        else:  # iSLIP
            requests = [[] for _ in range(N)]

            for i in range(N):
                for o in range(N):
                    if queues[i][o]:
                        requests[o].append(i)

            grants = [None]*N
            for o in range(N):
                for k in range(N):
                    i = (output_ptr[o] + k) % N
                    if i in requests[o]:
                        grants[o] = i
                        break

            accepts = [None]*N
            for i in range(N):
                for k in range(N):
                    o = (input_ptr[i] + k) % N
                    if grants[o] == i:
                        accepts[i] = o
                        break

            for i in range(N):
                if accepts[i] is not None:
                    o = accepts[i]
                    queues[i][o].popleft()
                    served += 1
                    input_ptr[i] = (o + 1) % N
                    output_ptr[o] = (i + 1) % N

        backlog.append(len(packets) - served)
        time += 1

    return backlog


# RUN 
fifo_b = simulate("fifo")
voq_b = simulate("voq")
islip_b = simulate("islip")

# GRAPH 
plt.figure()

plt.plot(range(len(fifo_b)), fifo_b, 'o-', label="FIFO")
plt.plot(range(len(voq_b)), voq_b, 's--', label="VOQ")
plt.plot(range(len(islip_b)), islip_b, '^-', label="iSLIP")

plt.xlabel("Time Slots")
plt.ylabel("Packets Remaining")
plt.title("Graph 2: Backlog vs Time")
plt.legend()
plt.grid()

plt.show()