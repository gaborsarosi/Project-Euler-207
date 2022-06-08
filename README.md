# Project-Euler-207

# Introduction

The purpose of these notes is to walk through the solution to [Problem 207](https://projecteuler.net/problem=207) on [projecteuler.net](http://projecteuler.net), and its programming version on [HackerRank](https://www.hackerrank.com/contests/projecteuler/challenges/euler207/problem).

## The problem

Consider the equation
$$4^t=2^t+k.$$
We will call values of $t$ for which $2^t,4^t,k$ are all positive integers a **partition**. We will call the partition **perfect**, when $t$ is also an integer. Let $P(m)$ be the fraction of perfect partitions to all partitions for $k\leq m$. The goal is to find the smallest $m$ for which $P(m)\leq \frac{a}{b}$, for given $a$ and $b$, both integers. In the HackerRank version of the problem, we are promised $a,b\leq 10^{18}$.

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

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png)

## Implementing the solution in Python

```python
def calcm(a,b):
    ql,qr=1,70
    while ql<qr-1:
        q=(ql+qr)/2
        if b*q>=(2**q-1)*a and b*(q+1)<(2**(q+1)-1)*a:
            break
        if b*q>(2**q-1)*a:
            ql=q
        else:
            qr=q
    if b*(q-1)<(2**q-1)*a:
        q+=-1
    xcand=1+b*q/a+1
    if xcand==2**(q+1):
        q+=1
        xcand=1+b*q/a+1
    m=xcand**2-xcand
    return m
``` 
