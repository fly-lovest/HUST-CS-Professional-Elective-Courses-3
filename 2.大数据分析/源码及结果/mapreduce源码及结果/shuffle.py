import threading


def run(readfileName):
    fileread = open(readfileName, 'r')
    filewrite1 = open("shuf01", 'a')
    filewrite2 = open("shuf02", 'a')
    filewrite3 = open("shuf03", 'a')
    for line in fileread:
        line = line.strip()
        word, count = line.split(',', 1)
        if word[0] == 'a' or word[0] == 'A' or word[0] == 'b' or word[0] == 'B' or word[0] == 'c' or word[0] == 'C':
            filewrite1.write("{},{}\n".format(word, count))
        elif word[0] == 'd' or word[0] == 'D' or word[0] == 'e' or word[0] == 'E' or word[0] == 'f' or word[0] == 'F':
            filewrite1.write("{},{}\n".format(word, count))
        elif word[0] == 'g' or word[0] == 'G' or word[0] == 'h' or word[0] == 'H':
            filewrite1.write("{},{}\n".format(word, count))
        elif word[0] == 'h' or word[0] == 'H' or word[0] == 'i' or word[0] == 'I' or word[0] == 'j' or word[0] == 'J':
            filewrite2.write("{},{}\n".format(word, count))
        elif word[0] == 'k' or word[0] == 'K' or word[0] == 'l' or word[0] == 'L' or word[0] == 'm' or word[0] == 'M':
            filewrite2.write("{},{}\n".format(word, count))
        elif word[0] == 'n' or word[0] == 'N' or word[0] == 'o' or word[0] == 'O' or word[0] == 'p' or word[0] == 'P':
            filewrite2.write("{},{}\n".format(word, count))
        else:
            filewrite3.write("{},{}\n".format(word, count))


if __name__ == '__main__':
    t1 = threading.Thread(target=run('comb01'), args=("t1",))
    t2 = threading.Thread(target=run('comb02'), args=("t2",))
    t3 = threading.Thread(target=run('comb03'), args=("t3",))
    t4 = threading.Thread(target=run('comb04'), args=("t4",))
    t5 = threading.Thread(target=run('comb05'), args=("t5",))
    t6 = threading.Thread(target=run('comb06'), args=("t6",))
    t7 = threading.Thread(target=run('comb07'), args=("t7",))
    t8 = threading.Thread(target=run('comb08'), args=("t8",))
    t9 = threading.Thread(target=run('comb09'), args=("t9",))
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
