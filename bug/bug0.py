"""
Bug Planning Algorithm
author: Mahima Arora
Source: https://sites.google.com/site/ece452bugalgorithms/
"""

import numpy as np
import matplotlib.pyplot as plt

show_animation = True
class BugPlanner:
    def __init__(this, start_x, start_y, goal_x, goal_y, obs_x, obs_y):
        this.goal_x = goal_x
        this.goal_y = goal_y
        this.obs_x = obs_x
        this.obs_y = obs_y
        this.r_x = [start_x]
        this.r_y = [start_y]
        this.out_x = []
        this.out_y = []
        for o_x, o_y in zip(obs_x, obs_y):
            for add_x, add_y in zip([1, 0, -1, -1, -1, 0, 1, 1],
                                    [1, 1, 1, 0, -1, -1, -1, 0]):
                cand_x, cand_y = o_x+add_x, o_y+add_y
                valid_point = True
                for _x, _y in zip(obs_x, obs_y):
                    if cand_x == _x and cand_y == _y:
                        valid_point = False
                        break
                if valid_point:
                    this.out_x.append(cand_x), this.out_y.append(cand_y)

    def mov_normal(this):
            return this.r_x[-1] + np.sign(this.goal_x - this.r_x[-1]), \
               this.r_y[-1] + np.sign(this.goal_y - this.r_y[-1])

    def mov_to_next_obs(this, visited_x, visited_y):
        for add_x, add_y in zip([1, 0, -1, 0], [0, 1, 0, -1]):
            c_x, c_y = this.r_x[-1] + add_x, this.r_y[-1] + add_y
            for _x, _y in zip(this.out_x, this.out_y):
                use_pt = True
                if c_x == _x and c_y == _y:
                    for v_x, v_y in zip(visited_x, visited_y):
                        if c_x == v_x and c_y == v_y:
                            use_pt = False
                            break
                    if use_pt:
                        return c_x, c_y, False
                if not use_pt:
                    break
        return this.r_x[-1], this.r_y[-1], True               

    def bug0(this):
        """
        Greedy algorithm where you move towards goal
        until you hit an obstacle. Then you go around it
        (pick an arbitrary direction), until it is possible
        for you to start moving towards goal in a greedy manner again
        """
        mov_dir = 'normal'
        cand_x, cand_y = -np.inf, -np.inf
        if show_animation:
            plt.plot(this.obs_x, this.obs_y, ".k")
            plt.plot(this.r_x[-1], this.r_y[-1], "og")
            plt.plot(this.goal_x, this.goal_y, "xb")
            plt.plot(this.out_x, this.out_y, ".")
            plt.grid(True)
            plt.title('BUG 0')

        for x_ob, y_ob in zip(this.out_x, this.out_y):
            if this.r_x[-1] == x_ob and this.r_y[-1] == y_ob:
                mov_dir = 'obs'
                break

        visited_x, visited_y = [], []
        while True:
            if this.r_x[-1] == this.goal_x and \
                    this.r_y[-1] == this.goal_y:
                break
            if mov_dir == 'normal':
                cand_x, cand_y = this.mov_normal()
            if mov_dir == 'obs':
                cand_x, cand_y, _ = this.mov_to_next_obs(visited_x, visited_y)
            if mov_dir == 'normal':
                found_boundary = False
                for x_ob, y_ob in zip(this.out_x, this.out_y):
                    if cand_x == x_ob and cand_y == y_ob:
                        this.r_x.append(cand_x), this.r_y.append(cand_y)
                        visited_x[:], visited_y[:] = [], []
                        visited_x.append(cand_x), visited_y.append(cand_y)
                        mov_dir = 'obs'
                        found_boundary = True
                        break
                if not found_boundary:
                    this.r_x.append(cand_x), this.r_y.append(cand_y)
            elif mov_dir == 'obs':
                can_go_normal = True
                for x_ob, y_ob in zip(this.obs_x, this.obs_y):
                    if this.mov_normal()[0] == x_ob and \
                            this.mov_normal()[1] == y_ob:
                        can_go_normal = False
                        break
                if can_go_normal:
                    mov_dir = 'normal'
                else:
                    this.r_x.append(cand_x), this.r_y.append(cand_y)
                    visited_x.append(cand_x), visited_y.append(cand_y)
            if show_animation:
                plt.plot(this.r_x, this.r_y, "-r")
                plt.pause(0.001)
        if show_animation:
            plt.show()


def main(bug_0):
    # set obstacle positions
    o_x, o_y = [],[]

    s_x = 0.0
    s_y = 0.0
    g_x = 167.0
    g_y = 50.0

    for i in range(20, 40):
        for j in range(20, 40):
            o_x.append(i)
            o_y.append(j)

    for i in range(60, 100):
        for j in range(40, 80):
            o_x.append(i)
            o_y.append(j)

    for i in range(120, 140):
        for j in range(80, 100):
            o_x.append(i)
            o_y.append(j)

    for i in range(80, 140):
        for j in range(0, 20):
            o_x.append(i)
            o_y.append(j)

    for i in range(0, 20):
        for j in range(60, 100):
            o_x.append(i)
            o_y.append(j)

    for i in range(20, 40):
        for j in range(80, 100):
            o_x.append(i)
            o_y.append(j)

    for i in range(120, 160):
        for j in range(40, 60):
            o_x.append(i)
            o_y.append(j)

    if bug_0:
        my_Bug = BugPlanner(s_x, s_y, g_x, g_y, o_x, o_y)
        my_Bug.bug0()


if __name__ == '__main__':
    main(bug_0=True)           