# fairdice
Python 3.9 script solving Riddler Classic @ https://fivethirtyeight.com/features/can-you-catch-the-cricket/

# Solution method

Let p1, p2... p6 be the probabilities of rolling 1, 2... 6 with one dice and let q2, q3... q12 be the probabilities of rolling 2, 3... 12 with two equal such dice.
The problem has a natural symmetry around the outcome 7, since the possible ways of forming a 6 are specular to those of forming an 8, 5 to 9, and so on.  Therefore, the 2-dice probability distribution with the lowest variance (i.e. the fairest) must be symmetric around q7, i.e.: q2 = q12, q3 = q11, q4 = q10, q5 = q9, q6 = q8, otherwise it would be possible to lower the variance by rebalancing the probabilities between the two tails.  
It follows that the optimal 1-dice probability distribution must also be symmetric: p1 = p6 := x, p2 = p5 := y, p3 = p4 := z, and z = 1/2 - x - y because all p's must sum up to 1; we have thus reduced the problem to a minimization with only 2 free variables x and y over the triangular domain 0 <= x <= 1/2, 0 <= y <= 1, x + y <= 1/2.  
By evaluating the loss function over a uniform grid of points within the domain, it can be found that the optimal choice is:

- x = 0.244, y = 0.138, yielding:
- [p1, p2, p3, p4, p5, p6] = [0.244, 0.138, 0.118, 0.118, 0.138, 0.244], in turn yielding:
- [q2, q3, ... q12] = [0.059, 0.067, 0.077, 0.09, 0.114, 0.185, 0.114, 0.09, 0.077, 0.067, 0.059]

The fairest possible 2-dice distribution is illustrated in the below charts, where it is contrasted with the "natural" distribution arising from using 2 individually fair dice:

![figure illustrating the optimal solution](https://github.com/stefperf/fairdice/blob/main/figure.png)
