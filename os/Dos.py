import os

if __name__ == '__main__':

    pipeline = os.popen("dir")
    print(pipeline.read())
