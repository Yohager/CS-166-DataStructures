### Building Suffix Arrays

---

回顾关于后缀数组的关键点：

- 保证所有的后缀按照字典序进行排序；
- exposing的分支词；

**Idea**:

我们不直接存储这些后缀，而是只存这些后缀开始的位置；

空间复杂度$\Theta(m)$, 同时对于每个输入的字母有一个machine word;

对于LCP Arrays我们可以使用Kasai's Algorithm在时间复杂度为$O(m)$内进行计算。

一些运行时间的分析：

- Suffix trees give an
  - $\langle O(m),O(n+z) \rangle$-time数据结构用于子字符串的搜索问题；
  - $O(m)$-time用于找到最长重复子字符串。
- Suffix Arrays, combined with LCP arrays, give an
  - $\langle O(m),O(n+\log m + z) \rangle$-time 数据结构用于子字符串的搜索问题；
  - $O(m)$-time用于找到最长重复子字符串。
- 以上的所有的时间复杂度的计算都是基于以下的假设：
  - 在$O(m)$的时间内构建一个后缀树；
  - 在$O(m)$的时间内构建一个后缀数组；

考虑第一个问题：如果有suffix tree如何在$O(m)$的时间内构建后缀数组和LCP数组。

首先在这个后缀树上进行dfs，按照排序的顺序访问所有的children；其次追踪最后一个被回溯的内部节点上的标签长度用于构建LCP数组。

下一个问题，反过来，如果有后缀数组和LCP数组，如何在$O(m)$的时间内构建后缀树。

这里给一个线性时间的算法：

- 首先从suffix array中构建LCP array.
- 从LCP array构建一个笛卡尔树。
- 在笛卡尔树上dfs，当一个节点有一个丢失的子节点时，按照它们出现的顺序加入后缀。
- 将数字相同的任意的parent和child节点融合起来。
- 基于LCP的值在对应的边上添加labels.

关于在$O(m)$的时间内构建后缀树的算法：

- 最早是1973年Weiner给出的STCA算法 (suffix tree)。
- 1976年 simplified $O(m)$的STCA (suffix tree)算法。
- 1990年 Manber and Myers给出了$O(m\log m)$的suffix array算法(SACA). 
- 1995年 Ukkonen 给出了一个popular的$O(m)$的STCA算法。
- ...

这里要介绍的是2008年提出的更快的SA-IS算法。

我们考虑对于suffix array可以将这些后缀按照首字母进行分桶的操作。

我们把一类后缀称为$S$型后缀，因为它在字典序上排序先于紧随其后的后缀。

相对应的我们就有另一类后缀称为$L$型后缀，因为其在字典序上排序后于紧随其后的后缀。

**Theorem**: A suffix starting at position $k$ is an $S$-type suffix if:

- `Text[k]<Text[k+1]`, or 
- `Text[k]=Text[k+1]` and the suffix at index $k+1$ is $S$-type, or 
- `Text[k]=$`.

A suffix starting at position $k$ is a $L$-type suffix if 

- `Text[k] > Text[k+1]`, or 
- `Text[k]=Text[k+1]` and the suffix at position $k+1$ is $L$-type.