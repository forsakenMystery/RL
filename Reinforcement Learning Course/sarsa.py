from Wampus import Wampus as Wampus
from graphics import *
import random
import matplotlib.pyplot as plt
import numpy as np


class SARSA:

    def __init__(self, width, height, obstacles, me, vampires, gold, arrows):
        self.width = width
        self.height = height
        self.me = me
        self.arrows = arrows
        self.gold = gold
        self.remember_me = me
        self.vampires = vampires
        self.obstacles = obstacles
        self.game = Wampus.start_desired_world(self.width, self.height, self.obstacles, self.me, self.vampires, self.gold, self.arrows)

    def __go_loading(self, i, total, show):
        percentage = i * 100 / total
        p = percentage
        s = "["
        k = 0
        while percentage > 0:
            s += "*"
            percentage -= 2
            k += 1
        k_prime = k
        while k < 50:
            k += 1
            s += " "
        if not (show == k_prime):
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(
                s + "]" + str("{:2.3f}".format(p)).zfill(6) + "%  -->  " + str(i).zfill(5) + "/" + str(total).zfill(4))
        return k_prime

    def sarsa(self, episodes=600, maximum_movements=200, random=0.98, discount=0.999, gamma=0.99):
        show = -1
        lol = []
        epsilon = 1
        lamda = 1
        fk = []
        ans = []
        Q = np.multiply(np.ones((self.width, self.height, self.game.ACTION_NUMBERS)), 1)
        for i in np.arange(episodes):
            summ = 0
            lol.append(i + 1)
            # input()
            show = self.__go_loading(i, episodes, show)
            self.game.reset()

            what = np.random.random(1)[0]
            S = self.game.me
            x, y = S
            if what < epsilon:
                phase = np.random.randint(0, self.game.ACTION_NUMBERS)
            else:
                phase = np.argmax(Q[x, y])
            action = self.game.ACTIONS[phase]
            for j in np.arange(maximum_movements):
                finish, reward = self.game.move(action)
                summ += reward
                what = np.random.random(1)[0]
                S_prime = self.game.me
                x_new, y_new = S_prime
                if what < epsilon:
                    phase_prime = np.random.randint(0, self.game.ACTION_NUMBERS)
                else:
                    phase_prime = np.argmax(Q[x_new, y_new])
                action_prime = self.game.ACTIONS[phase_prime]
                Q[x, y, phase] = lamda * (reward + gamma * Q[x_new, y_new, phase_prime]) + (1 - lamda) * Q[x, y, phase]
                action = action_prime
                phase = phase_prime
                S = S_prime
                x, y = S
                if finish:
                    if reward == self.game.WINNING_PRIZE:
                        ans.append([{"episode": str(i)}, {"moves": str(j)}])
                    break
            fk.append(summ)
            lamda *= discount
            if i % 16 == 0:
                epsilon *= random
                # print(epsilon)
        print(ans)
        self.Q = Q
        return Q, lol, fk

    def test_Sarsa(self):
        episode = []
        self.game.reset()
        finish = False
        while not finish:
            time_step = []
            x, y = self.game.me
            time_step.append(self.game.me)
            action = self.game.ACTIONS[np.argmax(self.Q[x, y])]
            time_step.append(np.argmax(self.Q[x, y]))
            finish, r = self.game.move(action)
            time_step.append(r)
            episode.append(time_step)
        return episode



def background(weight, obstacles, vampires, gold, arrows):
    length = weight*100
    win = GraphWin('My WORLD', length, length)
    back = Rectangle(Point(0, 0), Point(length*100, length*100))
    back.setFill("white")
    back.draw(win)
    for i in range(weight+1):
        l = Line(Point(100 * i, length), Point(100 * i, 0))
        l.setWidth(5)
        l.draw(win)
    for i in range(weight+1):
        l = Line(Point(0, 100 * i), Point(length, 100 * i))
        l.setWidth(5)
        l.draw(win)
    for obstacle in obstacles:
        x, y = obstacle
        obst = Rectangle(Point(y*100, x*100), Point((y+1)*100, (x+1)*100))
        obst.setFill("black")
        obst.draw(win)
    for arrow in arrows:
        x, y = arrow
        arr = Rectangle(Point(y*100+25, x*100+25), Point((y+1)*100-25, (x+1)*100-25))
        arr.setFill("olive")
        arr.draw(win)
    x, y = gold
    back = Rectangle(Point(y * 100, x * 100), Point((y + 1) * 100, (x + 1) * 100))
    back.setFill("cyan")
    back.draw(win)
    goal = Rectangle(Point(y*100+25, x*100+25), Point((y+1)*100-25, (x+1)*100-25))
    goal.setFill("brown")
    circle = Circle(Point(y*100+50, x*100+25), 25)
    circle.setFill("gold")
    circle.draw(win)
    goal.draw(win)
    line = Rectangle(Point(y*100+30, x*100+40), Point(y*100+70, x*100+45))
    line.setFill("black")
    lined = Rectangle(Point(y * 100 + 30, x * 100 + 30), Point((y + 1) * 100 - 30, (x + 1) * 100 - 30))
    lined.setFill("pink")
    lined.draw(win)
    lind = Rectangle(Point(y * 100 + 30, x * 100 + 55), Point(y * 100 + 70, x * 100 + 60))
    lind.setFill("black")
    lind.draw(win)
    line.draw(win)

    for vampire in vampires:
        x, y = vampire

        back = Rectangle(Point(y * 100, x * 100), Point((y + 1) * 100, (x + 1) * 100))
        back.setFill("purple")
        back.draw(win)

        head = Circle(Point(((weight-1)*100+50)-(weight-1-y)*100, ((weight-1)*100+50)-(weight-1-x)*100), 25)
        head.setFill("yellow")
        head.draw(win)

        eye1 = Circle(Point(((weight-1)*100+40)-(weight-1-y)*100, ((weight-1)*100+45)-(weight-1-x)*100), 5)
        eye1.setFill('red')
        eye1.draw(win)

        eye2 = Circle(Point(((weight-1)*100+60)-(weight-1-y)*100, ((weight-1)*100+45)-(weight-1-x)*100), 5)
        eye2.setFill('red')
        eye2.draw(win)

        mouth = Oval(Point(((weight-1)*100+40)-(weight-1-y)*100, ((weight-1)*100+65)-(weight-1-x)*100), Point(((weight-1)*100+60)-(weight-1-y)*100, ((weight-1)*100+65)-(weight-1-x)*100))
        mouth.setFill("red")
        mouth.draw(win)

        teeth_1 = []
        v1 = Point(((weight-1)*100+40)-(weight-1-y)*100, ((weight-1)*100+65)-(weight-1-x)*100)
        v2 = Point(((weight-1)*100+40)-(weight-1-y)*100+10, ((weight-1)*100+65)-(weight-1-x)*100)
        v3 = Point(((weight-1)*100+40)-(weight-1-y)*100+5, ((weight-1)*100+65)-(weight-1-x)*100+5)
        teeth_1.append(v1)
        teeth_1.append(v2)
        teeth_1.append(v3)
        triangle = Polygon(teeth_1)
        triangle.setFill("white")
        triangle.draw(win)

        teeth_2 = []
        v1 = Point(((weight-1)*100+60)-(weight-1-y)*100, ((weight-1)*100+65)-(weight-1-x)*100)
        v2 = Point(((weight-1)*100+60)-(weight-1-y)*100-10, ((weight-1)*100+65)-(weight-1-x)*100)
        v3 = Point(((weight-1)*100+60)-(weight-1-y)*100-5, ((weight-1)*100+65)-(weight-1-x)*100+5)
        teeth_2.append(v1)
        teeth_2.append(v2)
        teeth_2.append(v3)
        triangle = Polygon(teeth_2)
        triangle.setFill("white")
        triangle.draw(win)
    return win


def i_got_the_move(win, shape_list, x, y, reward, action, color, weight):
    print(reward)
    for shape in shape_list:
        shape.undraw()
        head = Circle(Point(((weight-1)*100+50) - (weight - 1 - y) * 100, ((weight-1)*100+50) - (weight - 1 - x) * 100), 25)
    if reward == Wampus.WAMPUS_PRIZE:
        xx, yy = Wampus.ACTIONS[action]
        # print(action)
        # print(xx)
        # print(yy)
        if action == 0:
            did = Rectangle(Point((y) * 100, (x-1) * 100), Point((y+1) * 100, (x) * 100))
            did.setFill("red")
            did.draw(win)
        if action == 1:
            did = Rectangle(Point((y) * 100, (x+1) * 100), Point((y-1) * 100, (x) * 100))
            did.setFill("red")
            did.draw(win)
        if action == 2:
            did = Rectangle(Point((y-1) * 100, (x) * 100), Point((y) * 100, (x+1) * 100))
            did.setFill("red")
            did.draw(win)
        if action == 3:
            did = Rectangle(Point((y+1) * 100, (x) * 100), Point((y) * 100, (x-1) * 100))
            did.setFill("red")
            did.draw(win)
    if reward == Wampus.COLLECTING_PRIZE:
        if action == 0:
            did = Rectangle(Point((y) * 100, (x-1) * 100), Point((y+1) * 100, (x) * 100))
            did.setFill("blue")
            did.draw(win)
        if action == 1:
            did = Rectangle(Point((y) * 100, (x+1) * 100), Point((y-1) * 100, (x) * 100))
            did.setFill("blue")
            did.draw(win)
        if action == 2:
            did = Rectangle(Point((y-1) * 100, (x) * 100), Point((y) * 100, (x+1) * 100))
            did.setFill("blue")
            did.draw(win)
        if action == 3:
            did = Rectangle(Point((y+1) * 100, (x) * 100), Point((y) * 100, (x-1) * 100))
            did.setFill("blue")
            did.draw(win)

    head.setFill(color[0])
    head.draw(win)

    eye1 = Circle(Point(((weight-1)*100+40) - (weight - 1 - y) * 100, ((weight-1)*100+45) - (weight - 1 - x) * 100), 5)
    eye1.setFill(color[1])
    eye1.draw(win)

    eye2 = Circle(Point(((weight-1)*100+60) - (weight - 1 - y) * 100, ((weight-1)*100+45) - (weight - 1 - x) * 100), 5)
    eye2.setFill(color[1])
    eye2.draw(win)

    mouth = Oval(Point(((weight-1)*100+40) - (weight - 1 - y) * 100, ((weight-1)*100+65) - (weight - 1 - x) * 100),
                 Point(((weight-1)*100+60) - (weight - 1 - y) * 100, ((weight-1)*100+65) - (weight - 1 - x) * 100))
    mouth.setFill(color[2])
    mouth.draw(win)

    shape_list = [head, eye1, eye2, mouth]
    return shape_list


def human_and_colors(win, weight, x, y):
    head = Circle(Point(((weight-1)*100+50) - (weight - 1 - y) * 100, ((weight-1)*100+50) - (weight - 1 - x) * 100), 25)
    head.setFill("yellow")
    head.draw(win)

    eye1 = Circle(Point(((weight-1)*100+40) - (weight - 1 - y) * 100, ((weight-1)*100+45) - (weight - 1 - x) * 100), 5)
    eye1.setFill('blue')
    eye1.draw(win)

    eye2 = Circle(Point(((weight-1)*100+60) - (weight - 1 - y) * 100, ((weight-1)*100+45) - (weight - 1 - x) * 100), 5)
    eye2.setFill('blue')
    eye2.draw(win)

    mouth = Oval(Point(((weight-1)*100+40) - (weight - 1 - y) * 100, ((weight-1)*100+65) - (weight - 1 - x) * 100),
                 Point(((weight-1)*100+60) - (weight - 1 - y) * 100, ((weight-1)*100+65) - (weight - 1 - x) * 100))
    mouth.setFill("red")
    mouth.draw(win)

    human = []
    human.append(head)
    human.append(eye1)
    human.append(eye2)
    human.append(mouth)
    colors = []
    colors.append("yellow")
    colors.append("blue")
    colors.append("red")
    return human, colors


def main(going):
    width = 9
    height = width
    # obstacles = [(2, 3), (2, 2)]
    obstacles = []
    me = (8, 8)
    # vampires = [(3, 1), (2, 1)]
    vampires = []
    # arrows = [(3, 2), (3, 3)]
    arrows = []
    gold = (0, 0)
    # print("Asdoasdsjksn")
    sarsa = SARSA(width, height, obstacles, me, vampires, gold, arrows)
    # print(QL.game)
    _, start, started = sarsa.sarsa(episodes=50000)
    episode = sarsa.test_Sarsa()
    print(episode)
    # width = 5
    # print(episode)
    # win = background(width, obstacles, vampires, gold, arrows)
    # human, color = human_and_colors(win, height, me[0], me[1])
    # time.sleep(1.5)
    # for m in range(len(episode)):
    #     human = i_got_the_move(win, human, episode[m][0][0], episode[m][0][1], episode[m][2], episode[m][1], color,
    #                            height)
    #     time.sleep(.75)
    # win.close()
    # if episode[-1][-1] is Wampus.WINNING_PRIZE:
    #     win = GraphWin('You Solved the problem', width * 100, 200)
    #     win.setBackground("yellow")
    #     text = Text(Point(width * 100 / 2, 100), "The Gold has been found")
    #     text.setFill("red")
    #     text.draw(win)
    #     time.sleep(.8)
    #     time.sleep(.5)
    #     win.close()
    # plt.plot(start, started, 'r')
    # plt.ylabel('cumulative rewards')
    # plt.show()
    XXX = 'Sarsa_output_no wampus_no obstacles_end in gold_50000_7,7_' + str(going) + '.txt'
    MyFile = open(XXX, 'w')
    for e, l in zip(start, started):
        MyFile.write(str(e))
        MyFile.write(',')
        MyFile.write(str(l))
        MyFile.write('\n')

    MyFile.write(str(episode))
    MyFile.close()


if __name__ == '__main__':
    for i in range(10):
        print(i)
        main(i)