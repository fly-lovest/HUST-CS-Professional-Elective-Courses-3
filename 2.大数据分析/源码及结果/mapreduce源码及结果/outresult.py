

if __name__ == '__main__':
    filewrite = open("outresult", 'w')
    fileread1 = open("result01", 'r')
    fileread2 = open("result02", 'r')
    fileread3 = open("result03", 'r')
    final_dict = {}
    for line in fileread1:
        line = line.strip()
        word, count = line.split(',', 1)
        final_dict[word] = count
    for line in fileread2:
        line = line.strip()
        word, count = line.split(',', 1)
        final_dict[word] = count
    for line in fileread3:
        line = line.strip()
        word, count = line.split(',', 1)
        final_dict[word] = count

    fin_list = sorted(final_dict.items(), key=lambda x: x[0])
    for key, value in fin_list:
        filewrite.write("{},{}\n".format(key, value))

    print("ALL DONE")
