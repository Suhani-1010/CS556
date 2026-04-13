from collections import deque
# ASSIGNMENT INPUT 

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

# FIFO WITH ARRIVAL PRIORITY

def simulate_fifo_arrival_priority(packets):
    time = 0
    served = 0
    total_packets = len(packets)

    queues = [deque() for _ in range(3)]
    remaining = packets.copy()

    print("\n FIFO (Arrival Priority) Simulation \n")

    while served < total_packets:

        print(f"\nTime Slot t = {time}")

        # Step 1: Add arriving packets
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]].append(pkt)
                print(f"  Arrival: {pkt[0]} added to I{pkt[2]} (dest O{pkt[3]})")
                remaining.remove(pkt)

        # Step 2: Collect all FRONT packets
        front_packets = []
        for i in range(3):
            if queues[i]:
                pkt = queues[i][0]
                front_packets.append(pkt)

        # Step 3: Sort by arrival time (priority)
        front_packets.sort(key=lambda x: x[1])  # sort by arrival time

        used_outputs = set()
        sent_packets = []

        # Step 4: Try sending in priority order
        for pkt in front_packets:
            inp = pkt[2]
            out = pkt[3]

            if out not in used_outputs:
                used_outputs.add(out)
                queues[inp].popleft()
                sent_packets.append(pkt[0])
                served += 1

        # Step 5: Print results
        print(f"  Sent: {sent_packets if sent_packets else 'None'}")

        time += 1

    print("\n Simulation Complete ")
    print(f"Total Time Slots Required: {time}")

    return time


# RUN

simulate_fifo_arrival_priority(packets)