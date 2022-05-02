### Amortized Analysis 

---

情景引入：假设我需要洗厨房的盘子和器皿，我有两种选择，手洗或者洗碗机。两者的利弊在于：前者会慢一点但是我可以随时拿到洗干净的盘子；后者会快一点但是得等所有洗完才能拿。

**Key Idea**: Design data structures that trade per-operation efficiency for overall efficiency. 

#### Examples of Amortization 

##### Two-Stack Queues 

一个**In** stack和一个**Out** stack

- To enqueue an element, push it onto the **In** stack. 
- To dequeue an element:
  - If the **Out** stack is nonempty, pop it. 
  - If the **Out** stack is empty, pop elements from the **In** stack, pushing them into the **Out** stack. Then dequeue as usual. 

Each enqueue takes time $O(1)$. 

Dequeue can vary in runtime.

- If **Out** stack is not empty: $O(1)$. 
- If **Out** stack is empty: $\Theta(n)$.

对于这个双栈队列分析：

**Theorem**: Any series of $n$ operations on an (initially empty) two-stack queue will take time $O(n)$. 

**Proof**: 

- 每个元素最多被push进入两个stacks同时最多从两个stacks被pop出来。
- 将$n$次操作中每个元素的工作加起来，我们会发现用时最多$O(n)$. 

对于这个双栈队列，dequeue的时间复杂度我们认为既不能说是$O(n)$也不能直接说是$O(1)$. 

所以下面的问题是我们应该如何衡量这个双栈队列的运行时间？

##### Dynamic Arrays 

动态数组的思路大概是：首先我们维护一个比你需要的数组稍稍大一些的数组，当空间不够的时候，直接double一下这个array的size，同时将元素复制过去。

- 大多数的append操作的时间是$O(1)$.
- 但是我们有时候需要$\Theta(n)$的work来复制前面的$n$个元素.

The cost of doing $n$ appends to an initially empty dynamic array is always $O(n)$. 

数组扩展的size为：$2^0,2^1,\cdots, 2^k,$ etc. 

最后一次扩展是在小于n的最大2次方的时候，$2^{\lfloor \log_2 n \rfloor}$. 

合计的所有的doubling最多为：
$$
\begin{split}
2^0+2^1+\cdots + 2^{\lfloor \log_2 n \rfloor} &= 2^{\lfloor \log_2 n \rfloor + 1} - 1 \\
&\leq 2^{\lfloor \log_2 n \rfloor+1}\\
&= 2n
\end{split}
$$

##### Building B-Trees 

给定一个包含了$n$个元素的sorted list和一个值$b$. 

基于这$n$个元素，什么方式构建一个order为$b$的B-Trees是最有效的？

一种比较直接的方式是我们计算这个B-tree的shape然后将元素按照顺序一个一个放进去。

另一种方式我们是自底向上构建这个B-tree.  Cost: $\Omega(n\log_b n)$. 

再换一种方式我们知道插入的时候都是从最右边的叶子插入的，我们可以考虑在最右边的叶子节点直接进行插入同时考虑是否需要做split操作。

基于这种方式，一次插入的时间代价会基于tree的shape进行考虑：

- 如果不要求split，这个cost为$O(1)$. 
- 如果要求一次split, 这个cost为$O(b)$. 
- 如果一直向上都需要split，那么这个cost为$O(b\log_b n)$. 

所以最坏情况下我们$n$次插入的时间为$O(n b\log_b n)$. 

而实际上我们认为平均意义上$n$次插入的时间cost为$O(n)$. 

具体分析来看，对于$n$次插入，大概有$\frac{1}{b}$次在最底层叶子节点的分裂。

再到次底层，又有$\frac{1}{b}$次节点的分裂，依次往上。

Total number of splits:
$$
\begin{split}
&\frac{n}{b}(1+\frac{1}{b}(1+\frac{1}{b}(1+\frac{1}{b}(\cdots))))\\
=& \frac{n}{b} \cdot(1+\frac{1}{b}+\frac{1}{b^2} + \frac{1}{b^3}+\cdots)\\
=& \frac{n}{b}\cdot \Theta(1) = \Theta(\frac{n}{b})=\Theta(n)
\end{split}
$$
所以这样分析可以发现整体的splits的cost为$\Theta(n)$. 

#### Amortized Analysis 

共同的特质：

- 单次操作可能会有些慢；
- 任意序列的操作会很快；

我们给出单次操作的weak upper bounds对于预测运行时间是不够有效的。

**Key Idea**: Assign each operation a (fake!) cost called its amortized cost such that, for any series of operations performed, the following is true:
$$
\sum \text{amortized-cost} \geq \sum \text{real-cost}
$$
对于双栈队列来说，其出队入队的均摊时间复杂度为$O(1)$, 但是单次操作的时间复杂度可能会比$O(1)$高。动态数组和构建b树也是类似的。

#### Potential Functions

计算均摊成本之前，我们需要找到一种方式来衡量这个数据结构的messy性（混乱程度）。

对于每个数据结构我们定义其势函数$\Phi$:

- $\Phi$ is small when the data structure is clean;
- $\Phi$ is large when the data structure is messy. 

当我们选定了势函数后，我们考虑均摊的时间成本和实际的时间成本之间的关系：
$$
\text{amortized-cost = real-cost} + k\cdot \Delta\Phi
$$
$k$是一个我们可以控制的参数，$\Delta\Phi=\Phi_{after}-\Phi_{before}$. （进行操作之后和进行操作之前的势能的变化。）

$\Phi$变大表示数据结构变得更加messy了，变小说明数据结构变得更加clean了。

对于均摊成本和实际成本之间我们可以进一步写为：
$$
\begin{split}
\sum \text{amortized-cost} &= \sum \text{real-cost} + k\cdot \sum\Delta\Phi\\
&=\sum \text{real-cost} + k\cdot (\Phi_{end}-\Phi_{start})\\
\end{split}
$$
进一步我们假设$\Phi\geq 0,\Phi_{start}=0$. 则：
$$
\sum \text{amortized-cost}\geq  \sum \text{real-cost}
$$
仍然用之前的例子：双栈队列

我们首先定义势函数为$\Phi$表示In stack的高度。下面证明双栈队列下入队和出队的均摊时间复杂度为$O(1)$. 

**Proof**: $\Phi$表示In stack的高度，每次入队操作只会进行一次push操作同时In stack的高度加1，因此其均摊时间复杂度表示为：$O(1)+k\cdot \Delta\Phi=O(1) + k\cdot 1=O(1)$. 下面我们考虑出队操作，(1). 如果Out Stack不为空，出队的时间复杂度为$O(1)$同时这个操作对于$\Phi$没有任何影响，所以其cost为：$O(1)+k\cdot \Delta\Phi=O(1)+k\cdot 0=O(1)$；(2). 假设Out Stack为空，同时当前In Stack的高度为$h$，我们定义将所有In Stack元素出队的时间为$O(h)$同时再将他们放入Out Stack，接着进行一次pop操作，整体的时间复杂度为$O(h)$. 考虑前后势函数的变化$\Delta\Phi=0-h=-h$. 从而这里的均摊时间成本为：$O(h)+k\cdot (-h)=O(1)$ (这里只要我们选择一个$k$来抵消在$O(h)$中的常数因子).

类似地我们可以证明对于dynamic arrays和building B-tree的均摊时间成本。

- Dynamic Arrays: 设置$\Phi$表示为元素的数量-空的slots的数量；
- Building B-trees: 设置$\Phi$表示为在右边spine的keys的数量；

