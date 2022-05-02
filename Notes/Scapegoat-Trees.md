### Scapegoat Trees 

---

#### Amortized Analysis 

last lecture是关于均摊时间的分析，我们引入了势函数potential function：

- $\Phi$ measures how "messy" the data structure is;
- $\Phi_{start}=0$;
- $\Phi\geq 0$.

我们定义一个操作的均摊时间为：amortized-cost = real-cost + $k\cdot \Delta \Phi$.

直觉上：

- 如果一个操作的使得系统变得更混乱了同时需要后续再进行整理，这个均摊的时间代价会比初始的时间代价更高。
- 如果一个操作使得系统变得clean，则均摊的时间代价会比真实的cost更小。

这里的目标是给出一个维护树平衡的更加容易的方式，我们考虑的是均摊的时间成本而非最坏情况下的时间成本。

考虑对于一个完美的平衡二叉树，假设共计有$n > 0$个节点，我们知道这个树的高度为$\log n$. 

但是往往维护这个树的shape是比较困难的，因为一个简单的插入或者删除操作往往会需要多次的reshuffling.

为了更快的添加元素和删除元素，大多数平衡二叉树确保树的高度为$\log n$的倍数。

对于红黑树而言，其高度在最坏情况下是$2\log n$. 

假设我们考虑我们的trees的高度可以是$\alpha \log n$ for some $\alpha > 1$. 

那么我们是否设计一个仅仅基于这个设定的平衡的二叉树而不依赖于其他的结构上的约束？

**Adding Slack Space**

- Pick a fixed constant $\alpha > 1$. 
- Set the maximum height on our tree to $\alpha \log n$. 
- As long as we don not exceed this maximum height, all operations on our BST will run in time $O(\log n)$, and we do not really care about the shape of the tree. 

对于每个节点$v$, 我们定义size(v)表示为以$v$为根节点的子树的节点的个数，height(v)表示的该子树的高度。

我们认为一个节点$v$是$\alpha-balanced$如果满足height(v) $\leq \alpha \log $ size(v). 

 假设插入的时候有一个节点超过了tree的极限高度，我们考虑需要对树进行一些调整：

**Scapegoat Nodes**:

- 我们考虑从root节点到最新插入节点之间的路径

- 我们知道root节点肯定不是$\alpha-$balanced，因为整个树的高度太高了。
- 我们又知道这个新插入的点是$\alpha-$balanced, 因为其没有children.
- 因此一定有一个节点在这个路径上不满足$\alpha-$balanced.
- 我们找到这个节点同时称其为scapegoat节点。

重新构建以这个scapegoat节点的子树成一个perfectly-balanced BST. 

这个能够reduce子树的高度，从而最后使得整个tree达到极限高度的要求。

下面给出Scapegoat Tree的具体构建方法：

- 给出一个常数$\alpha > 1$. 
- 只要树的高度小于$\alpha \log n$, 插入之后不需要进行重新平衡的操作；
- 一旦这个tree高度超出了限制，我们找到scapegoat节点；
- 重新构建以这个scapegoat节点为根节点的子树；

我们需要考虑以下的一些问题：

- 我们如何证明调整了scapegoat节点的子树之后可以成功修正树的高度？
- 我们重新构建这个子树的时间复杂度为多少？
- 我们如何找到这个scapegoat节点？
- 从均摊复杂度的角度分析时间？

**Theorem**: Optimally rebuilding the subtree rooted at the scapegoat node ensures that, as a whole, the tree has height at most $\alpha \log n$. 

**Proof**: 假设我们在插入当前节点时违背了高度限制，则在插入该节点前这个tree的高度应该小于等于$\alpha \log n$. 这也就意味着除了当前节点高度为$\lfloor \alpha \log n\rfloor+ 1$外，其他节点的高度在$\lfloor \alpha \log n\rfloor$以内。

现在我们考虑scapegoat节点，由于仅仅存在一层的超过，我们只需要证明重构后的子树比原子树至少高度下降了1. 

假设$v$表示scapegoat node，由于不平衡我们知道：
$$
height_{before}(v) > \alpha \log size(v)
$$
我们令$r$表示为这个子树重构之后的root，由于我们重新构建这个子树，我们可以得到：
$$
\log size(v) \geq height_{after}(r)
$$
从而进一步：
$$
height_{before}(v) > \alpha \log size(v)\geq height_{after}(r)
$$
也就是说：
$$
height_{before}(v) > height_{after}(r)
$$
因此重构后的子树高度一定至少下降了1. 

**The cost of rebuilding**

我们重构的方式为：

- 首先考虑中序遍历得到这个子树的有序的结果；
- 使用下面的递归方法构建新tree；
  -  如果不存在剩余的节点，我们直接返回一个空树；
  - 否则我们将中间元素放在这个tree的根部，同时递归构建左右子树；

这样构建的时间成本为$O(size(v))$其中$v$表示的是这个子树的root.

（对于这个构建问题，还存在一些更好的方法：Galperin-Rivest / Day-Stout-Warren算法）

**Finding the scapegoat node**

我们能够以什么样的效率找到这个scapegoat节点呢？

对于每个在从root到新插入节点的路上的节点$v$, $height(v)$表示为在$v$和新添加的节点之间的steps. 

如何计算$size(v)$呢，我们可以有两种做法。

1. 我们可以在边插入节点或者删除节点的时候对于每个节点维护一个cost. 需要额外的空间。
2. 我们也可以自底向上计算这个size. 从新插入的节点开始记为1，我们在反向tree上使用dfs直到搜索到scapegoat节点，返回这个size的值，整个过程需要$O(size(v))$的时间复杂度。

**Analyzing Efficiency**

- 基于我们已经看到的东西，对于一次插入而言，我们可以计算时间复杂度为：
  - 如果这个插入可以使树的高度保持不超过极限高度，那么时间为$O(\log n)$.
  - 如果我们需要调整子树，这个时间为$O(\log n + size(v))$. 
- 极端情况下，我们会发现这个调整tree的时间可以达到$O(n)$，即整个树都要重建。
- 但是我们可以考虑均摊时间复杂度上进行分析，因为上述的情况发生的次数不会很多。

我们的目标现在就是找一个合适的势函数$\Phi$:

- perfectly-balanced trees have low $\Phi$;
- $\alpha-$imbalanced tree have high $\Phi$;

这里定义的不平衡性表示为一个节点左右子树上节点的个数的差值，如果为0表示完美平衡，差值的数量表示不平衡的程度。
$$
(v) = \vert size(v.left) - size(v.right)\vert
$$
直觉上我们可以定义$\Phi=\sum_{v}(v)$因为对于越平衡的树，节点的“不平衡性”就越弱，这个势函数就越小。但是这个并不完全合理，如下图所示：

<img src="../pics/potential-function.png" alt="potential function on different BST" style="zoom:60%;" />

首先看前两个，两个都是完全二叉树，但是势函数的值不太一样，这就意味着当我们想要重新平衡树的时候，我们需要确保使每个节点的左、右子树中的节点数量相等。

对于一个完美平衡二叉树而言，其势函数的是一个关于其节点数量的函数。考虑第二个和第三个tree，我们发现两个都是完美平衡二叉树，因此两个tree的势函数都应该为0，但是这里一个为2一个为4. 

考虑到这个我们重新定义$'(v)$:
$$
'(v) =
\begin{cases}
0 & (v)\leq 1\\
(v) & \text{otherwise}
\end{cases}
$$
重新定义的$'(v)$与原$(v)$的差别在于如果左右子树的节点数量差值小于等于1则认为没有不平衡度。在重新定义后的势函数下：

<img src="../pics/potential-function-2.png" alt="new potential function" style="zoom:60%;" />

直觉上来说，如果一个以$v$为根节点的子树是完美平衡的（完全二叉树）那么我们认为$'(v)=0$.

我们考虑两种情况：

- 插入元素未触发子树重构。
- 插入元素触发了子树重构。

直觉上我们希望case-1的情况得到是一个小的$\Delta\Phi$同时case-2得到的是一个大的负的$\Delta \Phi$. 

revisit一下计算公式：amortized-cost = real-cost + $k\cdot \Delta\Phi$.

首先real-cost为$O(\log n)$, 其次每次我们插入一个节点，$(v)$的变化值应该是$\pm 1$. 在这条access path上共有$O(\log n)$个节点，同时$(v)$每次对于每个点的增量为1，也就是说对于$'(v)$的增量最多为2.从而我们知道$\Delta \Phi = O(\log n)$.

Amortized-cost = $O(\log n) + k\cdot (O(\log n))=O(\log n)$. 

直觉上来说对于每一个新插入的点，如果没有触发重构，则显然$\Delta \Phi = O(\log n)$，我们假设未来这个点的祖先节点可能会发生重构，直觉上我们可以认为这个$O(\log n)$的添加操作对应于未来的$O(\log n)$重构中贡献了$O(1)$的量的工作。

假设$v$是scapegoat节点，我们考虑$(v)$:

假设有新添加节点的分支为$x$同时另一个子树为$y$，我们考虑计算$(v) = \vert size(x) - size(y) \vert $.

由于$v$是不平衡的：$\alpha-$imbalanced. 显然我们有$height(v) > \alpha \log size(v)$. 

同时由于$v$是最深的那个不满足平衡的点显然我们知道$x,y$都是平衡的：$height(x)\leq \alpha \log size(x)$.

由于新插入的点是子树中最深的点，我们还知道$height(v) = height(x) + 1$. 

假设我们将所有的条件放在一起我们会得到：$\alpha \log size(v) < \alpha \log size(x) + 1$. 即：$size(v)< size(x)\cdot 2^{1/\alpha}$. 

另外显然我们知道：$size(v) = size(x)+size(y)+1$.从而$size(x)+size(y) < size(x)\cdot 2^{1/\alpha}$. 这也就意味着$size(y) < size(x)\cdot(2^{1/\alpha}-1)$. 从而我们就能说明y分支上的节点个数一定要少于x分支。

除此之外：
$$
\begin{split}
(v) &= \vert size(x)-size(y) \vert\\
&= size(x) - size(x) \cdot (2^{1/\alpha}-1)\\
&= size(x)\cdot (2-2^{1/\alpha})
\end{split}
$$
与不等式$size(v)<size(x)\cdot 2^{1/\alpha}$我们可以得到：$(v)> size(v)\cdot (2^{1-1/\alpha}-1)$. 

考虑$\alpha$的取值，如果$\alpha$接近1，我们就要求这个tree是非常严格的平衡树，因此当一个不平衡的情况出现时，我们会发现$(v)$与$size(v)$的关系很小。反之关系很密切。

对于任意的确定的$\alpha$而言，我们有$(v)=\Omega(size(v))$. 

换句话说，这个scapegoat点总是会不平衡且至少是关于这个子树的节点的线性关系。

总之这个均摊的时间复杂度为：$O(\log n)+O(size(v)) - k\cdot \Omega(size(v))$.

直觉上来说，如果我们选择一个更小的$\alpha$我们会得到一个更加平衡的tree（更快的查找但是重构子树的代价会增加，即插入时间增加）；如果选择一个大的$\alpha$我们将会得到一个更加不平衡的树（查找时间增加，但是插入时间减少）。

**考虑删除操作的时间成本**

首先跟插入操作完全不一样的地方是，删除可能影响的是很多个节点的位置，删除一个节点可能会导致一个不相关的节点的高度超过阈值，或者使得多个不相关的节点的子树高度超过阈值。

我们考虑假设原树的节点个数为$n$同时阈值高度为$\alpha\log n$, 同时假设删除完节点之后新的树的节点个数为$n_{new}$个，现在我们要考虑的就是：$\alpha \log n_{new}<\alpha \log n -1$. 结果就是$n_{new}< n \cdot 2 ^{-1/\alpha}$, 由于我们又知道这里的$\alpha$的范围是$(0,1)$，因此我们可以知道我们需要删除超过$n(1-2^{-1/\alpha})$的情况下才会出现整个tree需要重新平衡的问题。

如果出现这种情况，我们考虑如何重新平衡这个tree:

我们的做法是，不需要考虑太多关于这个树的结构的问题，直接重构以root节点的整个tree，得到一个新的完全二叉树即可。

我们考虑分析删除操作的均摊复杂度，此时我们将势函数修改为：$\Phi=D+\sum_{v}'(v)$. 这里的$D$表示的是总计的删除次数。

(1). 当我们不需要重构整个tree的时候删除的时间复杂度为$O(\log n)$, 对于新的势函数考虑如下条件：

- $D$是一个一个增长的，因为我们每次是一个一个删除的。
- $'(v)$对于每个在access path的节点来说，每次最多改变两次，同时这条路径上有$O(\log n)$个这样的点。

均摊复杂度：$O(\log n) + k\cdot O(\log n) = O(\log n)$. 

(2). 当我们需要重构整颗tree的时候，我们考虑这个势函数，重构完成之后$\sum_{v}'(v)=0$, 因此对于这个势函数而言存在一个未知的且非正的改变值。考虑$D$的改变值：

- 当我们开始重构时，我们有$n=n_{\max}\cdot 2^{-1/\alpha}$个节点在tree中；
- 这就意味着$D\geq n_{\max}\cdot (1-2^{-1/\alpha})$，也就是说$D\geq n\cdot (2^{1/\alpha}-1)=\Omega(n)$;
- 而从这一步之后，我们将$D$重置为0，所以我们知道$\Delta D\leq -\Omega(n)$;

因此我们一定有$\Delta \Phi \leq -\Omega(n)$.

事实上，我们可以知道，对于单步删除成本是$O(\log n)$同时对于重构整个tree而言成本是$O(n)$;

从均摊时间复杂度的角度来说：$O(\log n)+O(n) - K\cdot \Omega(n)$我们可以调整$K$从而使得最终的均摊复杂度为$O(\log n)$. 

总结来看，对于这个scapegoat tree，也就是我们说的替罪羊树：首先查找的时间为$O(\log n)$，对于插入和删除操作来说，我们都证明了其从均摊时间复杂度的角度来说都是$O(\log n)$. 

#### Next time:

Tournament Heaps 

Lazy Tournament Heaps 