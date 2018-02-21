import random

for j in range(100):
    line=''
    for i in range(144):
        line=line.join(','+str(int(random.random()*255)))
    print(line)