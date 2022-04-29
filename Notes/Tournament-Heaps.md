### Tournament Heaps

---

Tournamet heaps是一种simple, flexible and versatile的优先队列。

对于优先队列而言，一般的操作有三个：`enqueue`入队，`find-min`返回最小元素，`extract-min`最小元素出队同时返回。

一般的优先队列使用的时binary heaps: 入队和出队的时间复杂度为$O(\log n)$，返回最小值的时间为$O(1)$. 

这种heaps在实际使用中已经很快了，但是我们已知的还有d-ary heaps可能通过给出一个好的d值达到更好的效果，其他的还有sequence heap.

在实际应用中很多地方会使用到优先队列的数据结构，尤其是一些图算法：

- `meld(pq1,pq2)`: 销毁`pq1,pq2`同时将他们的元素合并到一个新的优先队列中。(MSTs via Cheriton-Tarjan)
- `pq.decrease-key(v,k')`: 给定一个指向已经在队列中的元素v的指针，以一个更小的k'去调整key（带堆优化的最短路径算法，global min-cut via Stoer-Wagner）
- `pq.add-to-all(Δk)`: 将Δk添加给每个在队列中的元素的keys，typically used with meld. (Optimum branchings via Chu-Edmonds-Liu)

这一讲中会介绍的内容包括：构建tournament heaps来有效的支持meld，abdication heaps来有效的支持meld和decrease-key. 

#### Meldable Priority Queues

一般使用的基于binary heaps的优先队列是不支持meld的操作的，因此两个二叉树没有办法直接合并到一起。

给定两个数$n,m$的二进制表示，我们可以在$O(\log m + \log n)$的时间内将两个数加到一起。直觉上，我们将$m$和$n$表示为一个packets的集合，这个packets中的元素都是2的幂次方，我们将$n,m$加到一起可以认为是将所有的packets合到一起。基于这个思想，我们可以用于构建一个优先队列。

我们考虑这样的packet需要具备什么样的性质？

- 首先size一定要是2的整数次幂（1,2,4,8,...）。

- 其次我们需要有效的将同等size的packets之间进行融合（只要每个packet需要提供O(1)时间返回最小值，我们可以在O(log n)的时间内获取最小）。
- 能够有效的找到每个packet的最小元素。
- 能够有效的拆分packets.

对于入队操作，我们可以有效的合并两个队列：用一个数据包将队列和一个新队列融合在一起。
对于出队操作：存在一个问题，删除一个元素后packet的元素不满足2的整数幂次方。此时要将packet进行拆分。我们可以通过对包含最小值的数据包进行拆分，并将碎片重新加入，来提取最小值。

下面引入Tournament Heaps: 一个tournament heap是一个tournament trees的集合，其以size的升序存储这些trees.

这个heap定义了以下的操作：

- `meld(pq1,pq2)`: 合并所有的trees，融合$O(\log n + \log m)$个trees，代价为$O(\log n + \log m)$，这里我们假设一个tournament heap包含$n$个点，另一个包含$m$个.
- `pq.enqueue(v,k)`: 将当前的队列与一个单元素的heap合并。$O(\log n)$.
- `pq.find-min()`: 找到所有trees的roots的最小元素。$O(\log n)$. 
- `pq.extract-min`: 找到最小值，同时删除tree的root节点，合并队列。$O(\log n)$. 

具体的构建过程比较简单，可以看[slides](http://web.stanford.edu/class/cs166/lectures/09/Slides09.pdf)的第116页开始的内容，详细给出了构建一个tournament heap的过程以及删除元素维护这个队列的过程。

考虑对于这个入队的操作是在meld中实现的。假设我们希望入队的时间为$O(1)$则我们需要meld的时间为$O(1)$. 如何实现这样的想法？

回顾均摊复杂度的概念，考虑如下的lazy的融合策略：

为了将两个tournament heaps融合起来，我们直接将两个trees的集合合并。

如果我们用一个循环的双重链表来存储我们的trees，我们可以在$O(1)$的时间下将trees连接到一起。

一个lazy tournament heap是在一个tournament heap的基础上做了以下的调整：

- meld操作是lazy的，即我们直接两个groups的trees直接合并。
- 在进行完一次extract-min操作后，我们进行一次合并操作直到每种高度的tree至多有一棵。

对于这个聚合(Coalescing)的操作，我们考虑如果将所有的trees按照高度的顺序维护，则可以省掉很多的操作。我们可以将group中的$t$个trees按照高度排序($O(t\log t)$). （一个更好的想法是我们使用计数排序，因为所有的size都比较小）

下面给出一个实现聚合操作的方法：

- 将trees分到an array of buckets: $0,1,2,\cdots,\lceil \log_2(n+1)\rceil$.
- 从bucket 0开始，只要有超过2个trees在这个bucket中，将他们进行融合同时将结果放到更大的一个bucket中。

这样的聚合操作的时间复杂度为：$O(t+\log n)$其中t表示为这个group的tree的数量。

- time to create the array of buckets: $O(\log n)$.
- time to distribute trees into buckets: $O(t)$. 
- time to fuse trees: $O(t+\log n)$. (number of fuse is $O(t)$, each fuse decreases the number of trees by one. cost per fuse is $O(1)$. Need to iterate across $O(\log  n)$ buckets) 

最坏情况是$O(n)$. 

对于一个带lazy melding的tournament heap我们有如下的最坏case的时间复杂度上界：

- `enqueue`: $O(1)$.
- `meld`: $O(1)$. 
- `find-min`: $O(1)$.
- `extract-min`: $O(n)$.

我们最后重点分析一下extract-min的均摊时间复杂度：

这里定义的势函数为$\Phi$表示在heap中的trees的数量。

考虑extract-min的流程：

- Find tree with minimum key: $O(t)$, $\Phi=t$.
- Remove min, add children to list of trees: $O(\log n)$. 
- Run the coalesce algorithm: $O(t+\log n)$, $\Phi=O(\log n)$. 

从而我们知道$\Delta\Phi=O(-t+\log n)$. 

Amortized cost:
$$
\begin{split}
&O(t+\log n) + k \cdot (-t+O(\log n))\\
=&O(t) - k\cdot t + k\cdot O(\log n)\\
=& O(\log n)
\end{split}
$$
因此对于`extract-min`操作，其均摊时间复杂度为$O(\log n)$. 

---

#### Next time:

- The need for decrease-key 
- Abdication heaps
- Analyzing Abdication heaps