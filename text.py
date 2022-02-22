text = "<^>v<^>v"

visited = 1

x = 0
y = 0

for i in text:
    if i == "^":
        y += 1
    elif i == "v":
        y -= 1
    elif i == "<":
        x -= 1
    elif i == ">":
        x += 1
    
    if x == 0 and y == 0:
        visited += 1
print(visited)