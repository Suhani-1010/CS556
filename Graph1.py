
# GRAPH 1: TOTAL SERVICE TIME (Arrival Priority)


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

# FIFO (Arrival Priority)
def fifo_time(packets):
    queues = [deque() for _ in range(3)]
    remaining = packets.copy()
    time, served = 0, 0

    while served < len(packets):
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]].append(pkt)
                remaining.remove(pkt)

        front = [q[0] for q in queues if q]
        front.sort(key=lambda x: x[1])

        used_outputs = set()

        for pkt in front:
            if pkt[3] not in used_outputs:
                queues[pkt[2]].popleft()
                used_outputs.add(pkt[3])
                served += 1

        time += 1

    return time


# VOQ / iSLIP (Arrival Priority)
def voq_time(packets):
    queues = [[deque() for _ in range(3)] for _ in range(3)]
    remaining = packets.copy()
    time, served = 0, 0

    while served < len(packets):
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]][pkt[3]].append(pkt)
                remaining.remove(pkt)

        candidates = [queues[i][o][0]
                      for i in range(3) for o in range(3)
                      if queues[i][o]]

        candidates.sort(key=lambda x: (x[1], x[2]))

        used_inputs, used_outputs = set(), set()

        for pkt in candidates:
            if pkt[2] not in used_inputs and pkt[3] not in used_outputs:
                queues[pkt[2]][pkt[3]].popleft()
                used_inputs.add(pkt[2])
                used_outputs.add(pkt[3])
                served += 1

        time += 1

    return time


# RUN
fifo = fifo_time(packets)
voq = voq_time(packets)
islip = voq_time(packets)   # same arrival-priority behavior

print("FIFO:", fifo)
print("VOQ:", voq)
print("iSLIP:", islip)

# GRAPH
plt.figure()
plt.bar(["FIFO", "VOQ", "iSLIP"], [fifo, voq, islip])
plt.xlabel("Algorithms")
plt.ylabel("Time Slots")
plt.title("Graph 1: Total Service Time (Arrival Priority)")
plt.grid()
plt.show()