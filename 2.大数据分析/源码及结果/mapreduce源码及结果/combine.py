import threading


def run(readfileName, writefileName):
    fileread = open(readfileName, 'r')
    filewrite = open(writefileName, 'w')
    comb_dict = {}
    for line in fileread:
        line = line.strip()
        word, count = line.split(',', 1)
        count = int(count)
        if word in comb_dict.keys():
            comb_dict[word] = comb_dict[word] + count
        else:
            comb_dict[word] = count

    for key, value in comb_dict.items():
        filewrite.write("{},{}\n".format(key, value))


if __name__ == '__main__':
    t1 = threading.Thread(target=run('map01', 'comb01'), args=("t1",))
    t2 = threading.Thread(target=run('map02', 'comb02'), args=("t2",))
    t3 = threading.Thread(target=run('map03', 'comb03'), args=("t3",))
    t4 = threading.Thread(target=run('map04', 'comb04'), args=("t4",))
    t5 = threading.Thread(target=run('map05', 'comb05'), args=("t5",))
    t6 = threading.Thread(target=run('map06', 'comb06'), args=("t6",))
    t7 = threading.Thread(target=run('map07', 'comb07'), args=("t7",))
    t8 = threading.Thread(target=run('map08', 'comb08'), args=("t8",))
    t9 = threading.Thread(target=run('map09', 'comb09'), args=("t9",))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    print("ALL DONE")