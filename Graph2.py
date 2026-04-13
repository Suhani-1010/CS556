
# GRAPH 2: BACKLOG VS TIME (Arrival Priority)


from collections import deque
import matplotlib.pyplot as plt

packets = [
    ("p1", 0, 0, 0), ("p2", 0, 0, 1),
    ("p3", 0, 1, 0), ("p4", 0, 1, 2),
    ("p5", 0, 2, 0),

    ("p6", 1, 0, 2), ("p7", 1, 2, 1),

    ("p8", 2, 1, 1),
    ("p9", 2, 2, 2),

    ("p10", 3, 0, 1), ("p11", 3, 1, 0),
    ("p12", 3, 2, 1),

    ("p13", 4, 0, 0), ("p14", 4, 1, 2),
    ("p15", 4, 2, 2),

    ("p16", 5, 0, 2), ("p17", 5, 1, 1),
    ("p18", 5, 2, 0)
]


def simulate_backlog(packets, mode):
    if mode == "fifo":
        queues = [deque() for _ in range(3)]
    else:
        queues = [[deque() for _ in range(3)] for _ in range(3)]

    remaining = packets.copy()
    time, served = 0, 0
    backlog = []

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

        else:
            candidates = [queues[i][o][0]
                          for i in range(3) for o in range(3)
                          if queues[i][o]]

            candidates.sort(key=lambda x: (x[1], x[2]))

            for pkt in candidates:
                if pkt[2] not in used_inputs and pkt[3] not in used_outputs:
                    queues[pkt[2]][pkt[3]].popleft()
                    used_inputs.add(pkt[2])
                    used_outputs.add(pkt[3])
                    served += 1

        backlog.append(len(packets) - served)
        time += 1

    return backlog


# RUN
fifo_b = simulate_backlog(packets, "fifo")
voq_b = simulate_backlog(packets, "voq")
islip_b = simulate_backlog(packets, "islip")

# GRAPH
plt.figure()

plt.plot(range(len(fifo_b)), fifo_b, 'o-', label="FIFO")
plt.plot(range(len(voq_b)), voq_b, 's--', label="VOQ")
plt.plot(range(len(islip_b)), islip_b, '^:', label="iSLIP")

plt.xlabel("Time Slots")
plt.ylabel("Packets Remaining")
plt.title("Graph 2: Backlog vs Time (Arrival Priority)")
plt.legend()
plt.grid()

plt.show()