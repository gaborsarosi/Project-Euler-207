# Project-Euler-207

# Introduction

The purpose of these notes is to walk through the solution to [Problem 207](https://projecteuler.net/problem=207) on [projecteuler.net](http://projecteuler.net), and its programming version on [HackerRank](https://www.hackerrank.com/contests/projecteuler/challenges/euler207/problem). The problem can be solved with elementary math and programming knowledge. We provide a Python implementation.

## The problem

Consider the equation
$$4^t=2^t+k.$$
We will call values of $t$ for which $2^t,4^t,k$ are all positive integers a **partition**. We will call the partition **perfect**, when $t$ is also an integer. Let $P(m)$ be the fraction of perfect partitions to all partitions for $k\leq m$. The goal is to find the smallest $m$ for which $P(m)\leq \frac{a}{b}$, for given $a$ and $b$, both positive integers. In the HackerRank version of the problem, we are promised $a,b\leq 10^{18}$.

# Solution

## The function

Let's start by understanding the function $P(m)$. In order to do this, we need to count all partitions and the perfect ones. 

Let's start with counting all partitions. Since for a partition $2^t$ is an integer, let's call this $n=2^t$. Notice that this automatically makes $4^t=n^2$ an integer as well. So on partitions, our equations reads as
$$k=n(n-1),$$
which, for $n=2,3,4,...$ gives the list of $k$s that give rise to partitions
$$k=2,6,12,20,...$$
To count how many such $k\leq m$ integers there are, we merely need to find the positive root of the equation $m=n(n-1)$ in $n$ and check how many integers $n=2,3,4,...,N$ fit below this value. This is just given by the integer part minus one, because we should not count $n=1$ since it corresponds to $k=0$. The number of partitions is then
$$\lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor -1.$$
Note that the largest integer $N$ giving rise to a partition is just the integer part without the subtraction, $N= \lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor$.


Now let us count the number of perfect partitions. A partition is perfect if $t=\log_2 n$ is an integer. To count the number of times that this happens for $n=2,3,4,...,N$, we again just need how many integers we can fit below $\log_2 N$, that is the integer part
$$\lfloor \log_2 N \rfloor.$$
Note that now $n=2$ corresponds to $t=1$ so we do not need to subtract anything from this.

We are now in position to take the ratio between the number of perfect partitions and the number of all partitions, and hence calculate the function $P(m)$:
$$P(m)= \frac{\lfloor \log_2 N \rfloor}{N-1} = \frac{\lfloor \log_2 \left( \lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor  \right) \rfloor}{\lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor -1}.$$

Here are some values of the function:
$$P(10)=1/2$$
$$P(15)=2/3$$
$$P(30)=2/5$$
$$P(2500)=5/49$$



## Describing the solution

Our task is to find the smallest $m$ for which $P(m)\leq a/b$, given $a$ and $b$ positive integers. It is useful to plot the function $P(m)$ in terms of $N=\lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor$, the maximal integer value of $n=2^t$ for a given $m$:

![alt text](https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotP.png)

We can solve our problem by finding a real (but not neccessarily integer) solution to the equation
$$\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$$

put figure

Once we have a solution, we may take the nearest integer to the right of it: $n=\lfloor N \rfloor +1$. We translate this back to $m$ by $m=n(n-1)=\lfloor N \rfloor(\lfloor N \rfloor+1)$.

The function has jumps where $\log_2 N$ is an integer, that is, at the location of perfect partitions $N=2^t$. Around these points, our equation has two solutions:

figure

Since we need the **smallest** $m$ for which $P(m)\leq a/b$, we should correspondingly take the smaller solution $N$. There is one exception to this rule: when the closest integer to the right $n=\lfloor N \rfloor +1$ agrees with the jump point of the function, that is, it gives rise to a perfect partition. In this case, the function already jumps to its next branch at $n$, thus violating $P(m)\leq a/b$! So we need to check for this separately and in this case take the larger solution.

So the practical problem boils down to solving the equation $\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$. How do we do this? 

The first and simplest thought that we can have is to simply scan the solution space one-by-one $N=2,3,4,5,...$.

Readers with some experience in numerical methods might be tempted to apply standard techniques such as the [Newton method](https://en.wikipedia.org/wiki/Newton%27s_method). While this works in theory, it requires us to work with floating point numbers, which leads to a numerical instability in evaluating $P(m)$ for large values of $m$. For instance, suppose that $a=1$ and $b=10^{18}$. In this cases, the smallest $m$ such that $P(m)\leq 10^{-18}$ is
$$m=4225000000000000000195000000000000000002.$$
We then have a problem finding this solution because a float with 7 digits of precision (or a double with 15) will never see the 2 at the end. So we should come up with a method that allows us to use only integers.

Luckily, the equation $\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$ can be easily solved by hand once we know which branch of the left hand side are we on, since on each branch, $\lfloor \log_2 N \rfloor$ is just a constant! So suppose that $2^{t-1}\leq N <2^t$. Then, $\lfloor \log_2 N \rfloor=t-1$ and
$$N=1+b(t-1)/a.$$
In summary, we solve the equation in two steps:
1. For given $a$, $b$, find the correct branch of $P(m)$, that is, a $t$ for which $2^{t-1}\leq N <2^t$,
2. Write the solution as $N=1+b(t-1)/a$ on the given branch.

Now we explain how to implement point 1. The function jumps at the points $N=2^t$ and the left limit at this points if $\frac{t-1}{2^t-1}$. It is useful again to examine this on a figure: 

![alt text](https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotPbranchlimiters.png)

The blue dots show the points $\left(2^t,\frac{t-1}{2^t-1}\right)$. Since these points are monotonically decreasing, to determine the branch, we are looking for an integral $t$ satisfying
$$\frac{t-1}{2^t-1}\geq \frac{a}{b} \geq \frac{t}{2^{t+1}-1} ,$$
or written in a form when we can evaluate all sides using only **integers**:
$$ b(t-1) \geq a (2^t-1) \quad \quad \text{and} \quad \quad b t \leq a (2^{t+1}-1).$$
These two inequalities are satisfied at the same time by only one value of $t$.

In practice, the simplest way to determine the correct value of $t$ is by increasing step-by-step from $t=2$:

```python
t=2
while True:
    if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
        break
```


However, we can make our algorithm substantially faster, by using **binary search** to determine $t$:

```python
tl,tr=1,70
while tl<tr-1:
    t=(tl+tr)/2
    if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
        break
    if b*(t-1)>(2**t-1)*a:
        tl=t
    else:
        tr=t
    
``` 

Now let us put everything together and wrap it into a function giving the solution. First, we determine the correct branch (the value of $t$) using binary search. Then we write the solution of the equation on the given branch, as discussed before. Finally we check for the edge case $n=\lfloor N \rfloor +1=2^{t+1}$, also described before. In summary:

```python
def calcm(a,b):
    #Binary search for t
    tl,tr=1,70
    while tl<tr-1:
        t=(tl+tr)/2
        if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
            break
        if b*(t-1)>(2**t-1)*a:
            tl=t
        else:
            tr=t
            
    #Write the solution, given t
    ncand=1+b*(t-1)/a+1
    
    #Check for the edge case
    if ncand==2**(t+1):
        t+=1
        ncand=1+b*(t-1)/a+1
        
    #recover m from n
    m=ncand**2-ncand
    return m
``` 
