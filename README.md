# Project-Euler-207

# Introduction

The purpose of these notes is to walk through the solution to [Problem 207](https://projecteuler.net/problem=207) on [projecteuler.net](http://projecteuler.net), and its programming version on [HackerRank](https://www.hackerrank.com/contests/projecteuler/challenges/euler207/problem). The problem can be solved with elementary math and programming knowledge. We provide a Python implementation. 

## The problem

Consider the equation $4^t=2^t+k$.
We will call values of $t$ for which $2^t,4^t,k$ are all positive integers a __*partition*__. For example, the first two partitions are $4^1=2^1+2$ and $4^{1.58496...}=2^{1.58496...}+6$. We will such a partition __*perfect*__, when $t$ is also an integer. For example, $4^1=2^1+2$ is a perfect partition, and the next one is $4^2=2^2+12$.
Let $P(m)$ denote the fraction of perfect partitions to all partitions for $k\leq m$. We are given $a$ and $b$, both positive integers. The goal is to find the smallest $m$ for which $P(m)\leq \frac{a}{b}$. In the HackerRank version of the problem, we are promised $a,b\leq 10^{18}$.

# Solution

## The function

Let's start by understanding the function $P(m)$. In order to do this, we need to count all partitions and the perfect ones. 

Let's start with counting all partitions. Since for a partition $2^t$ is an integer, let's call this $n=2^t$. Notice that this automatically makes $4^t=n^2$ an integer as well. So on partitions, our equations reads as
$$k=n(n-1),$$
which, for $n=2,3,4,...$ gives the list of $k$ values that give rise to partitions
$$k=2,6,12,20,...$$
To count how many such $k\leq m$ integers there are, let's look at a figure:

<img src="https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotP.png" width="300">

we just need to find the positive root of the equation $m=n(n-1)$ in $n$ and check how many integers $n=2,3,4,...,N$ fit below this value. The positive root of $m=n(n-1)$ is $\frac{1}{2}(1+\sqrt{1+4m})$. This is just given by the integer part minus one, because we should not count $n=1$ since it corresponds to $k=0$. The number of partitions is then
$$\lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor -1,$$
where $\lfloor . \rfloor$ denotes the [floor function](https://en.wikipedia.org/wiki/Floor_and_ceiling_functions). Note that the largest integer $N$ giving rise to a partition is just the integer part without the subtraction, $N= \lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor$.


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

Our task is to find the smallest $m$ for which $P(m)\leq a/b$, given $a$ and $b$ positive integers. It is useful to plot the function $P(m)$ in terms of $N=\lfloor \frac{1}{2}(1+\sqrt{1+4m}) \rfloor$:

<img src="https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotP.png" width="300">

We can solve our problem by finding a real (but not neccessarily integer) solution to the equation
$$\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$$

<img src="https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotP_w_aperb.png" width="300">

Once we have a solution, we may take the nearest integer to the right of it: $n=\lfloor N \rfloor +1$. We translate this back to $m$ by $m=n(n-1)=\lfloor N \rfloor(\lfloor N \rfloor+1)$. If the function $P(m)$ was monotonic, this would have been our answer.

However, the function is not monotonic. Instead it is piecewise monotonic between jumps that happen when $\log_2 N$ is an integer, that is, at the location of perfect partitions $N=2^t$. Around these points, our equation has two solutions:

<img src="https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotP_w_aperb_2.png" width="300">

Since we need the **smallest** $m$ for which $P(m)\leq a/b$, we should correspondingly take the smaller solution $N$ and take the nearest integer to the right of it: $n=\lfloor N \rfloor +1$. When this $n$ stays on the same branch, we are done, because the function will take smaller value at $n$ than at $N$. On the other hand, when $n$ moves past the jump point of the function, it violates $P(m=n(n-1))\leq a/b$! So we need to check for this separately and in this case take the larger solution.

So the practical problem boils down to solving the equation $\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$. How do we do this? 

The first and simplest thought that we can have is to simply scan the solution space one-by-one $N=2,3,4,5,...$. However, when $a$ is small (say 1) and $b$ is large (say $10^{18}$), we have $\frac{\log_2 N}{N} \approx 10^{-18}$ or $N\approx 6.6 \cdot 10^{19}$. Quite a space to scan over, we cannot afford that! We need to do something better.

Readers with some experience in numerical methods might be tempted to apply standard techniques such as the [Newton method](https://en.wikipedia.org/wiki/Newton%27s_method) to solve the equation $\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$. While this works in theory, it requires us to work with floating point numbers, which leads to a numerical instability in evaluating $P(m)$ for large values of $m$. For instance, suppose that $a=1$ and $b=10^{18}$. In this case, the smallest $m$ such that $P(m)\leq 10^{-18}$ is
$$m=4225000000000000000195000000000000000002.$$
We then have a problem finding this solution because a float with 7 digits of precision (or a double with 15) will never see the 2 at the end. So we should come up with a method that allows us to use only integers.

Luckily, the equation $\frac{\lfloor \log_2 N \rfloor}{N-1}  = \frac{a}{b}$ can be easily solved by hand once we know which branch of the left hand side are we on, since on each branch, $\lfloor \log_2 N \rfloor$ is just a constant! So suppose that $2^{t}\leq N <2^{t+1}$. Then, $\lfloor \log_2 N \rfloor=t$ and
$$N=1+\frac{b t}{a}.$$
In summary, we solve the equation in two steps:
1. For given $a$, $b$, find the correct branch of $P(m)$, that is, a $t$ for which $2^{t}\leq N <2^{t+1}$,
2. Write the solution as $N=1+bt/a$ on the given branch.

Now we explain how to implement point 1. It is useful again to explain this on a figure: 

![alt text](https://github.com/gaborsarosi/Project-Euler-207/blob/main/plotPbranchlimiters.png)

The function jumps at the points $N=2^t$ and the blue dots show the points $\left(2^t,\frac{t-1}{2^t-1}\right)$. We wish to determine the $t$ for which $\frac{a}{b}$ (the gray dashed line) runs between the blue dotted line corresponding to $t$ and $t+1$. On the figure, $a=6$, $b=1000$ and the correct $t$ is $t=10$. 

In equations, we are looking for an integer $t$ satisfying
$$\frac{t-1}{2^t-1}\geq \frac{a}{b} > \frac{t}{2^{t+1}-1} ,$$
or written in a form when we can evaluate all sides using only **integers**:
$$ b(t-1) \geq a (2^t-1) \quad \quad \text{and} \quad \quad b t < a (2^{t+1}-1).$$
These two inequalities uniquely determine $t$.

In practice, the simplest way to determine the correct value of $t$ is by increasing it one-by-one. First we check if we are on the $t=1$ branch. If not, we increase $t$ one-by-one until the two inequalities are satisfied simulaneously.

```python
if b*(1)<=(2**(2)-1)*a:
  t=1
else:
    t=2
    while not (b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a):
        t+=1
```

As noted before, we need to be able to reach $N\approx 2^t \approx 10^{20}$, or $t\approx 67$. So now we should succeed in just 67 steps!

However, we can make our algorithm even faster, by using [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) to determine $t$. This allows us to finish in just $\log t_{\rm max}$ time, where $t_{\rm max}$ is the maximal allowed value for $t$. Let's throw in a few extra and take this to be 70:

```python
if b*(1)<=(2**(2)-1)*a:
  t=1
else:
#Binary search for t
  tl,tr=2,70
  while tl<tr-1:
      t=(tl+tr)//2
      if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
          break
      if b*(t-1)>(2**t-1)*a:
          tl=t
      else:
          tr=t
    
``` 

Now let us put everything together and wrap it into a function giving the solution. First, we determine the correct branch (the value of $t$) using binary search. Then we write the solution of the equation on the given branch, as discussed before. Finally we check if $n=\lfloor N \rfloor +1\geq 2^{t+1}$, in which case we need to move to the next branch, as described before. In summary:

```python
def calcm(a,b):
    #Check the t=1 edge case:
    if b*(1)<=(2**(2)-1)*a:
      t=1
    else:
    #Binary search for t
      tl,tr=2,70
      while tl<tr-1:
          t=(tl+tr)//2
          if b*(t-1)>=(2**t-1)*a and b*(t)<(2**(t+1)-1)*a:
              break
          if b*(t-1)>(2**t-1)*a:
              tl=t
          else:
              tr=t
    
    #Write the candidate solution, given t
    ncand=1+b*t//a+1
    
    #Check if ncand moved to the next branch; if yes, move to the next branch
    while ncand>=2**(t+1):
        t+=1
        ncand=1+b*t//a+1
        
    #recover m from n
    m=ncand**2-ncand
    return m
``` 

