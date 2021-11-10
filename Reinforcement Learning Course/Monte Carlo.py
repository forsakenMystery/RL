from Wampus import Wampus as Wampus
from graphics import *
import random
import matplotlib.pyplot as plt


class MonteCarlo:

    def __init__(self, width, height, obstacles, me, vampires, gold, arrows):
        self.width = width
        self.height = height
        self.me = me
        self.arrows = arrows
        self.gold = gold
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

    def test_mc(self, policy):
        episode = self.game.create_trajectory(policy)
        return episode

    def monte_carlo_e_soft(self, episodes=5000, policy=None, epsilon=0.01):
        if not policy:
            policy = self.game.create_random_uniform_policy()
        Q = self.game.create_state_action_dictionary(policy)
        returns = {}
        i = 0
        show = -1
        start = []
        started = []
        while i < episodes:
            # print(policy)
            start.append(i)
            show = self.__go_loading(i, episodes, show)
            G = 0 # comulative reward
            episode = self.game.create_trajectory(policy)
            summation = 0
            for l in episode:
                summation += l[2]
            started.append(summation)
            # print(episode)
            ready_to_returns = {}
            for j in reversed(range(0, len(episode))):
                s_t, a_t, r_t = episode[j]
                # print(s_t)
                # print(a_t)
                xx, yy = s_t
                state_action = xx, yy, a_t
                # print(state_action)
                G += r_t
                if not state_action in ready_to_returns:
                    ready_to_returns[state_action] = [G]
                    if not state_action in returns:
                        returns[state_action] = [G]
                    else:
                        returns[state_action].append(G)
                    Q[s_t][a_t] = sum(returns[state_action])/len(returns[state_action])
                    Q_list = list(map(lambda x: x[1], Q[s_t].items()))
                    indices = [i for i, x in enumerate(Q_list) if x == max(Q_list)]
                    arg = random.choice(indices)

                    # print("aragh", arg)
                    for action in policy[s_t]:
                        if action is arg:
                            policy[s_t][action] = 1 - epsilon + (epsilon/abs(sum(policy[s_t])))
                        else:
                            policy[s_t][action] = (epsilon/abs(sum(policy[s_t])))
            i += 1
        return policy, start, started


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
    for shape in shape_list:
        shape.undraw()
        head = Circle(Point(((weight-1)*100+50) - (weight - 1 - y) * 100, ((weight-1)*100+50) - (weight - 1 - x) * 100), 25)
    if reward is Wampus.WAMPUS_PRIZE:
        xx, yy = Wampus.ACTIONS[action]
        # print(action)
        # print(xx)
        # print(yy)
        if action is 0:
            did = Rectangle(Point((y) * 100, (x-1) * 100), Point((y+1) * 100, (x) * 100))
            did.setFill("red")
            did.draw(win)
        if action is 1:
            did = Rectangle(Point((y) * 100, (x+1) * 100), Point((y-1) * 100, (x) * 100))
            did.setFill("red")
            did.draw(win)
        if action is 2:
            did = Rectangle(Point((y-1) * 100, (x) * 100), Point((y) * 100, (x+1) * 100))
            did.setFill("red")
            did.draw(win)
        if action is 3:
            did = Rectangle(Point((y+1) * 100, (x) * 100), Point((y) * 100, (x-1) * 100))
            did.setFill("red")
            did.draw(win)
    if reward is Wampus.COLLECTING_PRIZE:
        if action is 0:
            did = Rectangle(Point((y) * 100, (x-1) * 100), Point((y+1) * 100, (x) * 100))
            did.setFill("blue")
            did.draw(win)
        if action is 1:
            did = Rectangle(Point((y) * 100, (x+1) * 100), Point((y-1) * 100, (x) * 100))
            did.setFill("blue")
            did.draw(win)
        if action is 2:
            did = Rectangle(Point((y-1) * 100, (x) * 100), Point((y) * 100, (x+1) * 100))
            did.setFill("blue")
            did.draw(win)
        if action is 3:
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
    width = 5
    height = width
    # obstacles = []
    obstacles = [(2, 3), (2, 2)]
    me = (4, 4)
    vampires = []
    vampires = [(3, 1), (2, 1)]
    # arrows = []
    arrows = [(3, 2), (3, 3)]
    gold = (0, 0)
    MC = MonteCarlo(width, height, obstacles, me, vampires, gold, arrows)
    policy, start, started = MC.monte_carlo_e_soft(episodes=10000)
    episode = MC.test_mc(policy)
    print(episode)
    win = background(width, obstacles, vampires, gold, arrows)
    human, color = human_and_colors(win, height, me[0], me[1])
    time.sleep(1.5)
    for m in range(len(episode)):
        human = i_got_the_move(win, human, episode[m][0][0], episode[m][0][1], episode[m][2], episode[m][1], color, height)
        time.sleep(.75)
    win.close()
    if episode[-1][-1] is Wampus.WINNING_PRIZE:
        win = GraphWin('You Solved the problem', width * 100, 200)
        win.setBackground("yellow")
        text = Text(Point(width * 100 / 2, 100), "The Gold has been found")
        text.setFill("red")
        text.draw(win)
        time.sleep(.8)
        time.sleep(.5)
        win.close()
    plt.plot(start, started, 'r')
    # XXX = 'Monte_Carlo_output_no wampus_no obstacles_end in gold_50000_7,7_' + str(going) + '.txt'
    # MyFile = open(XXX, 'w')
    # for e, l in zip(start, started):
    #     MyFile.write(str(e))
    #     MyFile.write(',')
    #     MyFile.write(str(l))
    #     MyFile.write('\n')
    #
    # MyFile.write(str(episode))
    # MyFile.close()

    plt.ylabel('cumulative rewards')
    plt.show()



if __name__ == '__main__':
    for i in range(1):
        print(i)
        main(i)
