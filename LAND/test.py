'''
KN_B0 = """
   |___|                      /^\\
  __\_/__                    _\_/_
   -_|_-                     \_|_/
    _|_  _________            ||| 
    /|\-|-\______/   -------|-/|\\
    / \\                       / \\
   /   \\                     /   \\
"""

print(KN_B0)

input()




print("""
    MARCUS                      
     |   |
      \/\/\
      /\-\\
     /    \\
     
     """)
     
     
input()
'''

try:
    global counter
    with open("data.txt", "r") as file:
        counter = int(file.read().strip())
except FileNotFoundError:
    # If the file doesn't exist yet, set the counter to 0
    #print("irnfurue")
    counter = 0

def start():
    global counter
    with open("data.txt", "r") as file:
        counter = int(file.read().strip())
    counter += 1
    with open("data.txt", "w") as file:
        #print("is ok")
        file.write(str(counter))
    
def f1():
    global counter
    counter += 1
    print(1)
    with open("data.txt", "w") as file:
        #print("is ok")
        file.write(str(counter))

def f2():
    global counter
    counter += 1
    print(2)
    with open("data.txt", "w") as file:
        #print("is ok")
        file.write(str(counter))
        
if counter == 0:
    start()
if counter == 1:
    f1()
if counter == 2:
    f2()
