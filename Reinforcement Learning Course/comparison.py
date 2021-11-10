import matplotlib.pyplot as plt
import numpy as np

Monte_Carlo_Path = []
Monte_Carlo_Game = []
Monte_Carlo_obstacle = []

QLearning_Path = []
QLearning_Game = []
QLearning_obstacle = []

Sarsa_Path = []
Sarsa_Game = []
Sarsa_obstacle = []

counter = np.arange(250)
print(counter)
for i in range(30):
    f = open('Monte_Carlo_output_no wampus_no obstacles_end in gold_10000_' + str(i) + '.txt', 'r')
    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line)-1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Monte_Carlo_Path.append(mc)

    f = open('Monte_Carlo_output_two wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Monte_Carlo_Game.append(mc)


    f = open('Monte_Carlo_output_no wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Monte_Carlo_obstacle.append(mc)

    f = open('QLearning_output_no wampus_no obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    QLearning_Path.append(mc)

    f = open('QLearning_output_two wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    QLearning_Game.append(mc)

    f = open('QLearning_output_no wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    QLearning_obstacle.append(mc)

    f = open('Sarsa_output_no wampus_no obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Sarsa_Path.append(mc)

    f = open('Sarsa_output_two wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Sarsa_Game.append(mc)

    f = open('Sarsa_output_no wampus_two obstacles_end in gold_10000_' + str(i) + '.txt', 'r')

    mc = []
    line = []
    for x in f:
        line.append(x)

    for j in range(len(line) - 1):
        ml = line[j].split(',')
        mc.append(int(ml[1]))
    Sarsa_obstacle.append(mc)


Sarsa_Path = np.array(Sarsa_Path)
Sarsa_Path = Sarsa_Path[:, ::40]


Sarsa_Game = np.array(Sarsa_Game)
Sarsa_Game = Sarsa_Game[:, ::40]

Sarsa_obstacle = np.array(Sarsa_obstacle)
Sarsa_obstacle = Sarsa_obstacle[:, ::40]

QLearning_Path = np.array(QLearning_Path)
QLearning_Path = QLearning_Path[:, ::40]

QLearning_Game = np.array(QLearning_Game)
QLearning_Game = QLearning_Game[:, ::40]

QLearning_obstacle = np.array(QLearning_obstacle)
QLearning_obstacle = QLearning_obstacle[:, ::40]

Monte_Carlo_Path = np.array(Monte_Carlo_Path)
Monte_Carlo_Path = Monte_Carlo_Path[:, ::40]

Monte_Carlo_Game = np.array(Monte_Carlo_Game)
Monte_Carlo_Game = Monte_Carlo_Game[:, ::40]

Monte_Carlo_obstacle = np.array(Monte_Carlo_obstacle)
Monte_Carlo_obstacle = Monte_Carlo_obstacle[:, ::40]


# print(Sarsa_Game.shape)
# print(np.max(Sarsa_Game, 0, keepdims=True).shape)
plt.plot(counter, np.average(Sarsa_Game, 0).T, 'r')
plt.plot(counter, np.average(QLearning_Game, 0).T, 'b')
plt.plot(counter, np.average(Monte_Carlo_Game, 0).T, 'g')
plt.title('RL in Game with average')
plt.legend(['sarsa', 'Qlearning', 'monte carlo'])

# plt.boxplot(Sarsa_Game)
print("well")
plt.show()

plt.plot(counter, np.average(Sarsa_Path, 0).T, 'r')
plt.plot(counter, np.average(QLearning_Path, 0).T, 'b')
plt.plot(counter, np.average(Monte_Carlo_Path, 0).T, 'g')
plt.title('RL in Path with average')
plt.legend(['sarsa', 'Qlearning', 'monte carlo'])

# plt.boxplot(Sarsa_Game)
print("well")
plt.show()

plt.plot(counter, np.average(Sarsa_obstacle, 0).T, 'r')
plt.plot(counter, np.average(QLearning_obstacle, 0).T, 'b')
plt.plot(counter, np.average(Monte_Carlo_obstacle, 0).T, 'g')
plt.title('RL in obstacle with average')
plt.legend(['sarsa', 'Qlearning', 'monte carlo'])

# plt.boxplot(Sarsa_Game)
print("well")
plt.show()

plt.plot(counter, np.max(Sarsa_obstacle, 0).T, 'r')
plt.plot(counter, np.max(QLearning_obstacle, 0).T, 'b')
plt.plot(counter, np.max(Monte_Carlo_obstacle, 0).T, 'g')
plt.title('RL in obstacle with max')
plt.legend(['sarsa', 'Qlearning', 'monte carlo'])

# plt.boxplot(Sarsa_Game)
print("well")
plt.show()