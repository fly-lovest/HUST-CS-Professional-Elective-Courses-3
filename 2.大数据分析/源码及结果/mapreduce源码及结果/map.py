import threading


def read_lines(file):
    for line in file:
        line = line.strip()
        yield line.split(', ')


def run(readfilename, writefilename):
    fileread = open(readfilename, 'r')
    filewrite = open(writefilename, 'w')
    lines = read_lines(fileread)
    with filewrite as f:
        for line in lines:
            for word in line:
                f.write(word+",1\n")


if __name__ == '__main__':
    t1 = threading.Thread(target=run('source01', 'map01'), args=("t1",))
    t2 = threading.Thread(target=run('source02', 'map02'), args=("t2",))
    t3 = threading.Thread(target=run('source03', 'map03'), args=("t3",))
    t4 = threading.Thread(target=run('source04', 'map04'), args=("t4",))
    t5 = threading.Thread(target=run('source05', 'map05'), args=("t5",))
    t6 = threading.Thread(target=run('source06', 'map06'), args=("t6",))
    t7 = threading.Thread(target=run('source07', 'map07'), args=("t7",))
    t8 = threading.Thread(target=run('source08', 'map08'), args=("t8",))
    t9 = threading.Thread(target=run('source09', 'map09'), args=("t9",))
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
