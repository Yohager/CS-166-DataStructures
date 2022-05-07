### Tries and Suffix Trees 

---

#### Tries and Patricia Tries 

自动补全问题：假设我们有一个text的序列：$T_1,T_2,\cdots,T_k$, 共计$m$个。同时我们有一个长度为$n$的pattern string $P$. 我们的目标是找到所有的以$P$为开头的串。

如果我们只有一个这样的$P$我们可以很容易地遍历一遍所有的$T_i$然后check是否是以$P$打头。但是问题在于，如果我们的patterns是varying的，我们是否能够加速这个过程？

我们使用一种叫做trie的结构，trie这个词源于"retrieval"检索。我们用一个tree表示所有的text，每一条边表示一个字母，一些节点被标记为存在的单词。

build the trie: $O(m)$. 如果忽略字母表的大小的话，我们构建这个字典树的时间大概为$O(m)$. 

check the pattern: $O(n)$. 如果忽略字母表的大小的话，我们check这个pattern的时间为$O(n)$. 

考虑我们需要多少时间能够找到所有的以pattern打头的text strings.

这取决于我们希望得到什么样子结构的结果？

1. 如果我们希望得到的是所有的matches.

   - search for the prefix. 
   - do a DFS, recording the letters seen on each branch and rebuild all the words.

2. 假设每个text有一个label或者id，我们只希望得到所有匹配的ids.

   我们可以使用时间复杂度为$O(n+z)$的算法的答案，其中$z$表示为匹配的数量。

我们对刚刚最基础的trie tree进行一点改进，我们在每个单词结尾处增加一个dollar符号\$, 这个\$符号表示为sentinel或者说end-marker. 

有了\$符号之后我们可以将所有的节点分为两类：叶子节点和中间节点。

我们定义一个节点叫做silly node如果它是一个非root节点且只有一个child. 

我们定义Patricia Trie表示为那一类所有的silly node都和parents节点融合的trie. 

我们有如下观察：

- 在Patricia Trie中的中间节点都有超过2个及以上的children. 
- 叶子节点对应于单词，同时中间节点都是用于routing的。

**Theorem**: The number of nodes in a Patricia trie with $k$ words is always $O(k)$ regardless of what those words are. 

**Claim**: If each leaf in a Patricia trie is annotated with the index of the word it comes from, the indices of strings starting with a given prefix can be found in time $O(n+z)$, where $n$ is the length of that prefix and $z$ is the number of matches. 

同样使用RMQ的表示方式，我们使用$\langle O(m),O(n+z) \rangle$的solution得到prefix matching. 

#### Suffix Trees 

The fundamental theorem of stringology says that, given two strings $w$ and $x$, that $w$ is a substring of $x$ iff $w$ is a prefix of a suffix of $x$. 

为了找到所有的$w$在$x$中的匹配，我们只需要找到所有以$w$为打头的$x$的后缀。

A suffix tree for a string $T$ is a Patricia trie of all suffixes of $T$. 

Each leaf is labeled with the starting index of that suffix. 

我们可以知道：

- 对于一个长度为$m$的string我们可以在$O(m)$内构建一个suffix tree. 
- 我们可以使用$O(m)$的空间复杂度来存储这样的一个string的suffix tree. 

**Longest Repeated Substrings**: The longest repeated substring of a string $T$ must be a branching word in $T\$$. 

Proof: 如果$w$不是branching，则其不可能成为最长的重复子串。找最长的重复子串，我们只需要在从root到叶子节点的路径上最长的中间节点代表的string，这个string即为我们希望找到的最长的重复子串。

这个lecture的内容比较少。

额外的一些内容：

- generalized suffix trees: Solves fast substring searching over multiple text strings, not just a single text string. 
- Approximate string matching: given a text string $T$ and a pattern $P$, see the closest match to $P$ in $T$. 
- Fast matrix multiplication: the matrix multiplications needed in computing word embeddings can, amazingly, be optimized using suffix trees. 

Next time: 

- Suffix Arrays.

  A space-efficient alternative to suffix trees. 

- LCP Arrays. 

  Implicitly capturing suffix tree structure.

##### 补充一点KMP

