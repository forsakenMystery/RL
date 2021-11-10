import numpy as np


ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3

actions = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]
theta = 0.0001
_lambda = 0.99

policy = np.multiply(.25, np.ones((16, 4)))
value = np.zeros(16)
print(value)
value = np.random.rand(16)
print(value)
P = {}
grid = np.arange(16).reshape([4, 4])
iteration = np.nditer(grid, flags=['multi_index'])
# im gonna change cell 1 to trap!
# changed
while not iteration.finished:
    s = iteration.iterindex
    y, x = iteration.multi_index
    P[s] = {a: [] for a in range(4)}
    done = lambda s: s == 0 or s == 15
    reward = 0 if done(s) else -1
    if done(s):
        P[s][ACTION_UP] = [(1, s, reward, True)]
        P[s][ACTION_DOWN] = [(1, s, reward, True)]
        P[s][ACTION_LEFT] = [(1, s, reward, True)]
        P[s][ACTION_RIGHT] = [(1, s, reward, True)]
        # print(P[s])
        # input()
    else:
        up = s if y == 0 else s - 4
        down = s if y == 3 else s + 4
        left = s if x == 0 else s - 1
        right = s if x == 3 else s + 1
        P[s][ACTION_UP] = [(1, up, reward, done(up))]
        P[s][ACTION_DOWN] = [(1, down, reward, done(down))]
        P[s][ACTION_LEFT] = [(1, left, reward, done(left))]
        P[s][ACTION_RIGHT] = [(1, right, reward, done(right))]
        # print(P[s])
        # input()
        if s is 2:
            print("raste yek")
            P[s][ACTION_LEFT] = [(1, 2, reward, done(left))]
        elif s is 5:
            print("paeene yek")
            P[s][ACTION_UP] = [(1, 5, reward, done(up))]

    iteration.iternext()
print("p")
print(P)
while True:
    delta = 0
    for s in range(16):
        v = 0
        for action, action_probability in enumerate(policy[s]):
            for probability, next_state, reward, done in P[s][action]:
                v += action_probability * probability * (reward + _lambda * value[next_state])
        delta = max(delta, np.abs(v - value[s]))
        value[s] = v
    print(value)
    # input()
    print("delta ", delta)
    print("theta ", theta)
    print("================\n")
    # print(value.reshape((4, 4)))
    if delta < theta:
        break

print(value)
value = value.reshape((4, 4))
print(value)
print("that's the jadval for you :P")
