from collections import deque

# INPUT (Assignment Data)

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

# iSLIP (Arrival Priority)

def islip_arrival_priority(packets):
    queues = [[deque() for _ in range(3)] for _ in range(3)]
    remaining = packets.copy()

    time = 0
    served = 0
    total = len(packets)

    backlog = []

    print("\n iSLIP (Arrival-Time Priority) \n")

    while served < total:

        print(f"Time Slot t = {time}")

     
        # Step 1: Arrivals
   
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]][pkt[3]].append(pkt)
                print(f"  Arrival: {pkt[0]} -> I{pkt[2]} to O{pkt[3]}")
                remaining.remove(pkt)

        # Step 2: Collect Requests
        
        candidates = []
        for i in range(3):
            for o in range(3):
                if queues[i][o]:
                    candidates.append(queues[i][o][0])  # head packet

        # Step 3: Arrival Priority
        
        candidates.sort(key=lambda x: (x[1], x[2])) 
 
        # sort by arrival time, then input (tie-break)
        # Step 4: Matching
       
        used_inputs = set()
        used_outputs = set()
        sent_packets = []

        for pkt in candidates:
            inp, out = pkt[2], pkt[3]

            if inp not in used_inputs and out not in used_outputs:
                queues[inp][out].popleft()
                used_inputs.add(inp)
                used_outputs.add(out)
                sent_packets.append(pkt[0])
                served += 1

        print("  Sent:", sent_packets if sent_packets else "None")

        backlog.append(total - served)
        time += 1

    print("\n Simulation Complete ")
    print("Total Time Slots:", time)
    print("Backlog:", backlog)

    return time, backlog

# RUN

islip_arrival_priority(packets)