import random

channel = [0] * 50
n = 0
tf = 5
ttemp = [0] * 10
a = 0
k = 2
w = 0
ds = [1] * 10
is_ = [0] * 10
js = [0] * 10
status = [1] * 10

class Station:
    def init(self):
        self.data = [0] * 5
        self.dest = 0
        self.time = 0

def collision(sno):
    global channel
    global is_
    global js

    for i in range(1, n + 1):
        if status[i] != 1:
            stat[i].time = ttemp[i]
            is_[i] = 0
            js[i] = 0

    for i in range(1, (n * 5) + 1):
        channel[i] = 0

    print("Jamming signal sent")
    tb = backoff()
    stat[sno].time += tb
    print("Station backoff by:", tb)
    send_data()

def backoff():
    global k

    kmax = 15
    if k > kmax:
        print("Station exceeded its limit\n", k)
        exit(0)
    else:
        s = (2 ** k) - 1
        r = random.randint(0, s)
        tb = r * tf
        k += 1
    return tb

def stat_ini():
    x = min((stat[i].time for i in range(1, n + 1) if stat[i].time != 0), default=0)
    for i in range(1, n + 1):
        if x > stat[i].time > 0:
            x = stat[i].time
    print("Time:", x)
    return x

def send_data():
    global channel
    global w

    tmin = stat_ini()
    for t in range(tmin, tmin + 100):
        for i in range(1, n + 1):
            if t == stat[i].time:
                if ds[i] == 1 and channel[i * 5 - 4] != 0:
                    tb = backoff()
                    print("Channel not free backing off by:", tb, "sec")
                    stat[i].time += tb
                else:
                    send(i)
                    stat[i].time += 1
        print("\n", "".join(map(str, channel)))
        input()

def send(sno):
    global ds
    global is_
    global js

    databit = 0
    if ds[sno] <= 3:
        databit = stat[sno].data[ds[sno]]
    print("\nData bit =", databit, "\nSno:", sno)

    if is_[sno] == 0 and js[sno] == 0:
        is_[sno] = js[sno] = sno * 5 - 4
        channel[sno * 5 - 4] = databit
    else:
        if channel[is_[sno] + 1] != 0 or channel[js[sno] - 1] != 0:
            print("\nCollision!!")
            input()
            collision(sno)
        else:
            if ds[sno] <= 3:
                x = is_[sno]
                for j in range(x, sno * 5 - 4, -1):
                    channel[j] = channel[j - 1]
            else:
                x = is_[sno]
                for j in range(1, 4):
                    channel[x] = channel[x - 1]
            channel[sno * 5 - 4] = databit

            if channel[stat[sno].dest * 5 + 3] == stat[sno].data[3]:
                print("\nData sending successful.")
                status[sno] = 1
                w += 1
                input()
                if a == w:
                    print("All signals sent successfully")
                    exit(0)

            ds[sno] += 1

if __name__== "__main__":
    print("")
    print("\n\tCARRIER SENSE MULTIPLE ACCESS WITH COLLISION DETECTION\t\n")
    print("\t\t\t\tCSMA/CD\t\t\t\t\n")
    print("*")
    n = int(input("Enter the number of stations: "))
    stat = [Station() for _ in range(n)]

    for i in range(n):
        ch = int(input(f"\nEnter 1 if station {i + 1} wants to transmit signal: "))
        stat[i].time = 0
        if ch == 1:
            stat[i].time = int(input(f"Enter time of sending signal of station {i + 1}: "))
            a += 1
            status[i] = 0
            while True:
                stat[i].dest = int(input(f"Enter destination of station {i + 1}: "))
                if stat[i].dest == i + 1 or stat[i].dest < 1 or stat[i].dest > n:
                    print("Wrong destination, try again")
                else:
                    break
            print(f"Enter the data (3-Bit data) for station {i + 1}:")
            for j in range(1, 4):
                stat[i].data[j] = int(input())

    for i in range(n):
        ttemp[i] = stat[i].time

    send_data()
