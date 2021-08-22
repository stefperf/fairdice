# solving Riddler Classic @ https://fivethirtyeight.com/features/can-you-catch-the-cricket/

import matplotlib.pyplot as plt
import numpy as np


def X2P(x, y):
    """
    translate the optimization variables x, y into the vector of probabilities p1...p6 for one dice
    """
    z = 0.5 - x - y
    return x, y, z, z, y, x


def P2Q(p1, p2, p3, p4, p5, p6):
    """
    compute the vector of probabilities q2..q12 for 2 dice from the vector of probabilities p1...p6 for one dice
    """
    q2 = p1 ** 2
    q3 = 2 * p1 * p2
    q4 = 2 * p1 * p3 + p2 ** 2
    q5 = 2 * (p1 * p4 + p2 * p3)
    q6 = 2 * (p1 * p5 + p2 * p4) + p3 ** 2
    q7 = 2 * (p1 * p6 + p2 * p5 + p3 * p4)
    return q2, q3, q4, q5, q6, q7, q6, q5, q4, q3, q2


def loss(x, y):
    """
    loss func. = log. variance of 2-dice probabilities from the optimization variables x, y; semi-optimized computation
    """
    z = 0.5 - x - y
    (p1, p2, p3, p4, p5, p6) = (x, y, z, z, y, x)
    q2 = p1 ** 2
    q3 = 2 * p1 * p2
    q4 = 2 * p1 * p3 + p2 ** 2
    q5 = 2 * (p1 * p4 + p2 * p3)
    q6 = 2 * (p1 * p5 + p2 * p4) + p3 ** 2
    q7 = 2 * (p1 * p6 + p2 * p5 + p3 * p4)
    return np.log(2 * sum((q ** 2 for q in (q2, q3, q4, q5, q6))) + q7 ** 2 - (1 / 11) ** 2)


if __name__ == '__main__':
    # find the optimal (x, y) among a grid of coordinated over the triangular admissible area
    X_min, L_min = None, 1e10  # init optimal coordinates and corresponding loss function value
    L_max = -1.  # for nicer plotting
    steps = 10000  # nr. of uniform grid intervals over the unit
    steps = steps // 2  # halving because the admissible region for x is [0, 0.5]
    xa = np.linspace(0.0, 0.5, steps + 1)
    ya = np.linspace(0.0, 0.5, steps + 1)
    xv, yv = np.meshgrid(xa, ya)
    zv = np.full(xv.shape, None, dtype=float)
    for ix, x in enumerate(xa):
        for iy, y in enumerate(ya[:steps - ix + 1]):  # the admissible y's are in [0, 0.5 - x]
            L = loss(x, y)
            zv[iy, ix] = L
            if L < L_min:
                X_min, L_min = (x, y), L  # update optimal coordinates and corresponding loss function value
            if L > L_max:
                L_max = L
    x_min, y_min = X_min
    P_opt = X2P(x_min, y_min)
    Q_opt = P2Q(*P_opt)
    print(f'The best probabilities p1...p6 found for one dice are: {P_opt}, sumcheck = {sum(P_opt)},')
    print(f'yielding these probabilities q2...q12 for two dice: {Q_opt}, sumcheck = {sum(Q_opt)};')
    print(f'the 2-dice probabilities have log variance = {L_min}.')
    fig, axs = plt.subplots(2, 1, figsize=(5.6, 10.4), gridspec_kw={'height_ratios': [1, 1]})
    fig.suptitle('"FAIREST" POSSIBLE 2-DICE ROLL')
    ax1 = axs[0]
    ax1.set_title('log variance of 2-dice probabilities')
    ax1.set_xlabel('x = p1 = p6')
    ax1.set_ylabel('y = p2 = p5')
    c = ax1.pcolormesh(xv, yv, zv, cmap='RdBu', vmin=L_min, vmax=L_max, shading='nearest')
    ax1.axis([xv.min(), xv.max(), yv.min(), yv.max()])
    fig.colorbar(c, ax=ax1)
    dot_col = 'k'
    ax1.plot(x_min, y_min, dot_col + 'o', markersize=3)
    ax1.annotate('fairest possible (min)', xy=X_min, xycoords='data', xytext=(3, 3), textcoords='offset points', color=dot_col)
    x_nat, y_nat = 1 / 6, 1 / 6
    X_nat = [x_nat, y_nat]
    ax1.plot(x_nat, y_nat, dot_col + 'o', markersize=3)
    ax1.annotate('"natural"', xy=X_nat, xycoords='data', xytext=(3, 3), textcoords='offset points', color=dot_col)
    ax2 = axs[1]
    ax2.set_title('probability distribution of sum of 2 dice')
    ax2.set_xlabel('sum of the 2 dice rolled')
    ax2.set_ylabel('probability')
    q_labels = np.array(list(range(2, 13)))
    P_natural = [1 / 6] * 6
    Q_natural = P2Q(*P_natural)
    bw = 0.3
    ax2.bar(q_labels - bw / 2, Q_natural, width=bw, label='"natural"')
    ax2.bar(q_labels + bw / 2, Q_opt, width=bw, label='fairest possible')
    q_uni = 1 / 11
    l_col = 'k'
    plt.plot([2 - bw, 12 + bw / 2], [q_uni, q_uni], color=l_col)
    ax2.annotate('uniform', xy=[10, q_uni], xycoords='data', xytext=(3, 3), textcoords='offset points', color=l_col)
    ax2.legend()
    plt.xticks(np.arange(min(q_labels), max(q_labels) + 1, 1))
    plt.subplots_adjust(hspace=0.3)
    plt.show()
