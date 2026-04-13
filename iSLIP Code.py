from collections import deque

packets = [
    ("p1",0,0,0),("p2",0,0,1),("p3",0,1,0),("p4",0,1,2),("p5",0,2,0),
    ("p6",1,0,2),("p7",1,2,1),
    ("p8",2,1,1),("p9",2,2,2),
    ("p10",3,0,1),("p11",3,1,0),("p12",3,2,1),
    ("p13",4,0,0),("p14",4,1,2),("p15",4,2,2),
    ("p16",5,0,2),("p17",5,1,1),("p18",5,2,0)
]

def islip():
    N = 3
    queues = [[deque() for _ in range(N)] for _ in range(N)]
    remaining = packets.copy()

    input_ptr = [0]*N
    output_ptr = [0]*N

    time, served = 0, 0

    print("\n iSLIP (Round Robin) ")

    while served < len(packets):
        print(f"\nTime {time}")

        # arrivals
        for pkt in remaining[:]:
            if pkt[1] == time:
                queues[pkt[2]][pkt[3]].append(pkt)
                print(f"Arrival: {pkt}")
                remaining.remove(pkt)

        # REQUEST
        requests = [[] for _ in range(N)]
        for i in range(N):
            for o in range(N):
                if queues[i][o]:
                    requests[o].append(i)

        # GRANT
        grants = [None]*N
        for o in range(N):
            for k in range(N):
                i = (output_ptr[o] + k) % N
                if i in requests[o]:
                    grants[o] = i
                    break

        # ACCEPT
        accepts = [None]*N
        for i in range(N):
            for k in range(N):
                o = (input_ptr[i] + k) % N
                if grants[o] == i:
                    accepts[i] = o
                    break

        # SEND
        sent = []
        for i in range(N):
            if accepts[i] is not None:
                o = accepts[i]
                pkt = queues[i][o].popleft()
                sent.append(pkt[0])
                served += 1

                input_ptr[i] = (o + 1) % N
                output_ptr[o] = (i + 1) % N

        print("Sent:", sent if sent else "None")
        time += 1

    print("Total Time:", time)

islip()