
if __name__ == '__main__':
    with open('../data/new.json', mode='r', encoding='utf-8') as f:
        read = f.read()
        print(read%("1","2","3","4","5"))
        # for line in f:
        #     print(line)
