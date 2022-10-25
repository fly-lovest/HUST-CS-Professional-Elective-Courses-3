import threading


def run(readfileName, writefileName):
    fileread = open(readfileName, 'r')
    filewrite = open(writefileName, 'w')
    rst_dict = {}
    for line in fileread:
        line = line.strip()
        word, count = line.split(',', 1)
        count = int(count)
        if word in rst_dict.keys():
            rst_dict[word] = rst_dict[word] + count
        else:
            rst_dict[word] = count

    rst_list = sorted(rst_dict.items(), key=lambda x: x[0])
    for key, value in rst_list:
        filewrite.write("{},{}\n".format(key, value))


if __name__ == '__main__':
    t1 = threading.Thread(target=run('shuf01', 'result01'), args=("t1",))
    t2 = threading.Thread(target=run('shuf02', 'result02'), args=("t2",))
    t3 = threading.Thread(target=run('shuf03', 'result03'), args=("t3",))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("ALL DONE")
