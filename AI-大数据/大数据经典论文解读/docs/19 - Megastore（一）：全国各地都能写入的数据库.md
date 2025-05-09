你好，我是徐文浩。

大数据技术一开始，更像一个专有系统。但是随着时间的推移，工程师们越来越多地让这些大数据系统支持上了SQL的特性。于是我们看到了Hive让大家可以用SQL来执行MapReduce任务，Dremel这样的系统更是一开始就支持了SQL。对于OLAP的分析类系统来说，支持Schema定义、支持字段类型、支持直接用类SQL的语言进行数据分析，很快就成为了新一代大数据分析系统的标准。

所以，Google想要在Bigtable这样的OLTP数据库上支持SQL，也不会让我们意外了。那么接下来，我们就一起来看一看《Megastore: Providing scalable, highly available storage for interactive services》这篇论文，为我们带来了一个什么样的分布式系统。

Megastore是一个雄心勃勃的系统，支持SQL这样的接口只是它想要做到的所有事情中的一小项。如果列出Megastore支持的所有特性，相信也是一个让人两眼放光的系统，好像是分布式数据库的终极答案：

- 跨数据中心的多副本同步数据复制；
- 支持为数据表的字段建立Schema，并且可以通过SQL接口来访问；
- 支持数据库的二级索引；
- 支持数据库的事务。

不过，**Megastore最终只是Google迈向Spanner中的一个里程碑。Megastore的大部分高级特性，都基于实际的应用场景做了取舍和妥协。**相比于略显高深的Spanner，Megastore的设计对大部分工程师和架构师来说更有实践意义。我会通过接下来的三讲，带你解读Megastore的论文：

- 第一讲，主要讲解论文中的第二部分，也就是Megastore的整体系统架构，以及这个架构是怎么从我们的应用场景需求妥协而来的。
- 第二讲，我们会来看一看Megastore的API设计、数据模型以及事务和并发控制是怎么做的，看看Megastore是怎么利用好Bigtable的特性来实现一个更高级的数据库。这个也是论文中的第三部分。
- 第三讲，我们会深入论文的第四部分，研究Megastore的数据复制机制，一起来看看，一个为跨数据中心复制而优化的Paxos算法实现，是怎么样的。

那么，通过今天第一讲的学习，相信对你根据业务实践来设计系统，以及如何在各种工程实践上进行取舍的能力有所裨益。

## 互联网时代的数据库

在我们前面介绍过的那些论文里，会发现工程师们对于“可用性”问题的考虑，往往是局限在一个数据中心里。GFS里我们会对数据做三份备份，但是这三份数据还是在同一个数据中心的三台服务器里；针对Chubby这样的服务，我们用了五个节点，放到不同的交换机下，但这仍然是在一个数据中心里。

可是，如果我们的分布式数据库只能在一个数据中心里，那无论是在“可用性”上，还是在“性能”上，在互联网时代都有点不够看。

- 在“**可用性**”这个角度，尽管我们在数据中心内部可以有非常完善的分布式、多路供电以及柴油发电机等方案，但是一旦遇上像水灾、地震这样的自然灾害，这些手段都无济于事。而往往在这个时候，让每个人能够访问到网络、发送消息又是特别重要的。前一阵我们遇到的郑州水灾就是一个很典型的例子。
- 在“**性能**”这个角度，如果我们的数据中心设在旧金山，那么一个上海用户的一个请求，在最理想的情况下，也至少需要100毫秒以上才能够完成一个网络请求的往返。在真实的网络环境里，其实100毫秒是远不够的，往往要到150乃至200毫秒。而这个访问速度，显然会让很多用户觉得“网络慢”，体验不好，容易流失用户。

![图片](https://static001.geekbang.org/resource/image/6e/8b/6e8598f54dbbd6eac69c3880db8e298b.jpg?wh=1920x1080 "真正高可用的架构里，数据会在多个数据中心同步，用户会就近访问最近的数据中心[br]如果特定数据中心出现问题，可以访问附近的其他数据中心[br]其实过去几年，大型的互联网公司都在建设“异地多活”的系统架构，就是为了保障系统的可用性和访问性能")

那么，解决这两个问题最好的办法，就是我们**有多个数据中心**。每个用户的请求都可以访问到就近的本地数据中心，对应的数据也直接就近写入本地数据中心里的数据库，也都从本地数据中心的数据库里读。而各个数据中心的数据库之间，会进行数据复制，确保你在旧金山写入的数据，我在上海一样可以读到。

而且既然是一个互联网层面的数据库，也就是用户量可能像Facebook或Google这样，达到几十亿，那这个数据库也需要有非常强的水平扩展能力，通过简单地增加服务器就能够服务更多的用户。

这些需求点，也就是Google需要Megastore这样一个系统的起因。而论文在第二部分的一开始，就写明了Megastore的解决方案：

- **对于可用性问题，通过实现一个为远距离链接优化过的同步的、容错的日志复制器。**
- **对于伸缩性问题，通过把数据分区成大量的“小数据库”，每一个都有独立进行同步复制的数据库日志，存放在每个副本的NoSQL的数据存储里。**

那么接下来，我们就一起看看这个方案具体是怎么样的。

## 复制、分区和数据本地化

和Hive没有重写计算引擎而是直接用了MapReduce一样，Megastore也没有重写数据存储层，而是直接使用了Bigtable。那么，Megastore想要解决的第一个问题，就是**如何在多个数据中心的Bigtable之间复制数据**。

我们常见的数据复制的方案，其实无非就是三种：

- 第一种是**异步主从复制（Asynchronous Master/Slave）**，这个我们之前在讲解[Chubby](https://time.geekbang.org/column/article/428116)的时候就讨论过。异步主从复制有两个核心问题，第一个是如果Master节点挂了，Slave如果还没有及时同步数据的话，我们可能会丢数据。第二个是如果写数据在数据中心A，读数据在数据中心B，那么刚写入的数据我们会读不到，也就是无法满足整个系统是“可线性化”的。
- 第二种是**同步主从复制（Synchronous Master/Slave）**，这也是大部分系统的解决方案。
- 第三种叫做**乐观复制（Optimistic Replication）**，这种方案是AP（Availability + Partition Tolerance）系统中常常用到的方案。也就是数据可以在任何一个副本中写入，然后这个改动会异步地同步到其他副本中。因为可以在任何一个副本就近写入，所以系统的可用性很好，延时也很低。但是，什么时候会同步完成我们并不知道，所以系统只能是**最终一致**（eventually-consistent）的。而且，这个系统基本无法实现事务，因为两个并发写入究竟谁先谁后很难判定，所以隔离性就无从谈起了，而“可线性化”自然也就没法做到了。

Megastore在这件事情上的选择非常简单明确，那就是直接使用Paxos算法来进行多个数据中心内的数据库的同步。要注意，Megastore并不是像我们之前讲解Bigtable+Chubby那样，只是采用Paxos来确保只有一个Master。**Megastore是直接在多个数据中心里，采用Paxos同步写入数据，是一个同步复制所有的数据库日志，但是没有主从区分的系统。**

不过，Megastore选择直接使用Paxos，最大的一个问题就是**性能**。

一方面，我们的数据传输无法突破物理学的限制，跨数据中心的延时是省不掉的。所以Megastore对于Paxos算法的实现，专门做了优化。这个优化，我们会在下一讲里专门讲解。

另一方面，即使把Paxos算法优化到极限，我们也避免不了，Paxos算法的每一次“共识”都需要超过半数节点的确认。如果是通过Paxos来保障一个数据库日志的同步复制，那么写入数据的性能就受限于单台服务器了，这也是为什么在Bigtable里，我们只是使用Chubby来管理粗粒度的锁，而不是直接用Paxos来进行同步复制。

那么在Megastore里，我们该怎么解决这个Paxos的性能瓶颈呢？

### 从业务需求到架构设计

我们先来回想一下分布式系统，需要做到“可线性化”的原因是什么。

以最常见的电商为例子，我下订单的数据库操作完成了之后，我再去查询这张订单是否完成，应该要能看到刚刚下的这一张订单。要不然的话，我一定会觉得很奇怪也非常担心，觉得钱付出去了，但是东西可能拿不到。

但是，几乎在我下单之前，另一位在海南的朋友也下单了。那么，他下的这张订单是否在我下单之前可以读取到，我却并不在意。一方面，自然我也没有权限看到他的订单，另一方面，在业务上我们也并不需要分辨，几乎在同一时间下单的人谁先谁后。

根据这个例子我们可以看到，从业务上来说，**我们不一定需要全局的“可线性化”，而只要一些业务上有关联的数据之间，能够保障“可线性化”就好了**。不仅从“可线性化”的角度是这样的，其实数据库事务隔离性的“可串行化”也是这样的。

我的订单，如果从业务上就不会和我在海南的朋友之间有冲突，不会去读写相同的数据。那么我们在下单过程中，互相之间的“可串行化”的隔离性，“有”和“没有”是没有区别的。也就是我们的“可串行化”的要求，也不是全局的。

而这个现实业务中，对于数据库事务的“可串行化”，以及分布式系统的“可线性化”不需要是全局的，就给Megastore带来了解决问题的思路。

Megastore是这么做的。

首先，它引入了一个叫做**“实体组”**（Entity Group）的概念。Megastore里的数据分区，也是按照实体组进行数据分区的。

然后，一个分区的实体组，会在多个数据中心之间通过Paxos进行数据同步读写。本质上，**Megastore其实是把一个大数据表，拆分成了很多个独立的小数据表。**每一个小数据表，在多个数据中心之间是通过Paxos算法进行同步复制的，你可以在任何一个数据中心写入数据。但是各个小数据表之间，并没有“可线性化”和“可串行化”的保障。

![图片](https://static001.geekbang.org/resource/image/36/ee/36192343e66b9d2aa09fabf74328d7ee.jpg?wh=1920x1421 "论文中的图1，Megastore的架构，好像是一个二维矩阵，按行是数据分区，按列是不同的数据中心")

你可以看一看论文里的图1，整个Megastore的架构，就好像是一个二维矩阵。横向按行，是按照数据分区进行了切分，纵向按列，是一个个独立的数据中心。

每一个分区的数据，可以在任意一个数据中心写入，同步复制到其他数据中心去。不过，不同分区的实体组之间的数据，其实就可以看作是两个独立的数据库的写操作，互相之间没有先后顺序和隔离性的关系了。

**那么实体组到底是什么呢？**你可以把实体组，当成是一个实体，以及挂载在这个实体下的一系列实体。

比如在前面电商的例子里，每一个用户是一个实体，这个用户的所有订单，可以以一个List的形式挂载在这个用户下，这个用户的所有和商家的消息，也可以挂载在这个用户下。这些东西打包在一起，就是一个实体组。一个实体组下的数据，往往我们经常会一起操作。比如，我们会去查看自己最近下的订单，意味着一个用户下的所有订单会在一起读取。

Megastore在每一个实体组内，支持一阶段的数据库事务。但是，如果你有跨实体组的操作需求，你该怎么办呢？你有两个选择，第一个，是使用两阶段事务，当然它的代价非常高昂，是一个阻塞的、有单点的解决方案。而第二个，则是抛弃事务性，转而采用Megastore提供的**异步消息机制**。因为一旦跨实体组，我们就不能保障数据操作是在同一个服务器上进行的了，就需要跨服务器的操作需求。

两阶段事务相信你已经非常熟悉了，我们来看看这个消息传递机制是怎么样的。当我们需要同时操作两个实体组A和B的时候，我们可以对第一个实体组，通过一阶段事务完成写入。然后，通过Megastore提供的一个队列（queue），向实体组B发起一个消息。实体组B接收到这个消息之后，可以**原子地**执行这个消息所做的改动。

所以，A和B两边的改动，在这个消息机制下，都是事务性的。但是两边的操作并没有共同组成同一个分布式事务。所以，如果在跨实体组的操作中采用了消息机制，Megastore本质上没有实现数据库事务，它实现的仍然是数据库的最终一致性。

![图片](https://static001.geekbang.org/resource/image/bd/6e/bd314680153734768a9bc70e81744a6e.jpg?wh=1920x1080 "论文中的图2，Megastore只支持单个实体组内的一阶段事务[br]跨实体组要么使用异步队列机制，要么采用两阶段提交")

如果我们拿一个具体的应用案例，可以更容易看清楚Megastore的这个设计。我们就以即时聊天，比如微信这个场景作为例子好了。

- 我们可以把每个微信账号，当成是一个实体组。
- 账号里面的每一条收和发的消息，也挂载在这个实体组里。
- 当你要发一条消息出去的时候，其实会影响到两个实体组，一个是你的微信账号，因为你的聊天记录里会多一条发出的消息。另一个是收件人的微信账号，他的聊天记录里也会多一条消息。
- 但是我们并不需要保证，你这里看到发出消息和他看到收到消息同时发生。那么我们就可以采用Megastore的异步消息机制。
- 我们先用一个一阶段事务，在你的微信账号的实体组里写入这条消息。然后再通过Megastore的异步消息机制，往收件人的微信账号里发送一条“写入消息”的请求。而他的实体组在收到这个“写入消息”的请求之后，把整个消息事务性地写入自己的实体组就可以了。

而之所以这个消息机制是有效可行的，其实还是回到我们开头说的，**在实际应用层面，我们对于“可串行化”以及“可线性化”的需求并不是全局的，而是可以分区的。**我们只需要保障自己发出的消息，在自己的微信界面上，看起来是按照顺序出现的就可以了。而并不要求收件人的微信和发件人的微信之间，也是“可线性化”的。

## 小结

好了，这一讲到这里就告一段落。在这一讲里，我们看到Megastore的设计提出了一系列雄心勃勃的目标。首先是跨数据中心的同步复制，让数据可以在任意一个离用户最近的数据中心写入。然后是支持为数据表建立Schema、定义字段类型、支持SQL接口和二级索引、支持数据库事务，想让工程师们像使用关系型数据库一样使用Megastore。而这些目标，既是顺应互联网时代的用户需求，也是大数据OLTP数据库不断发展的必然目标。

当然，Megastore并没有选择从头开始、另起炉灶，而是准备直接基于Bigtable和Paxos算法来实现这些目标。不过，无论是多么天才的工程师，也逃脱不了地心引力。Paxos算法本身的性能是有限的，所以Megastore采取了分区这个办法。**本质上，Megastore不是一个“可线性化”的分布式数据库，而是很多个分布式数据库的一个合集。**

而在事务性上，Megastore也作出了种种限制。**Megastore只支持一个实体组下的一阶段事务**，如果你需要跨实体组进行操作，那么要么你得使用代价高昂的二阶段提交，要么你可以使用Megastore提供的异步消息机制。而实体组这个概念本身，就是把一些经常要在一起操作的数据，组合在一起，方便进行快速操作。

可以看到，Megastore虽然提出了雄心勃勃的目标，但是在实际最终的实现上，作出了种种的妥协和限制。Megastore并不是一个“透明”的分布式数据库，而是要你在充分了解它的特性之后，对于你自己的数据库表进行对应的适配性设计，才能发挥出它的这些有意思的特性。

那么，在下一讲里，我们就来看看Megastore的API、数据模型是怎么回事儿，以及它的事务和并发控制是怎么做的。如果我们要基于Megastore来实现我们的业务系统，搞清楚这些原理是至关重要的。

## 推荐阅读

相比开创时代的Bigtable，和成为最终答案的Spanner，Megastore在网络上的资料相对少一些。实体组的概念，也和大部分你熟悉的关系型数据库和KV数据库都有些区别。不过，你可以直接去用一下Google Cloud里的[Datastore](https://cloud.google.com/datastore/docs/)这个产品，它其实就是进化多年之后的Megastore。当然，我也推荐你反复读一下Megastore的[论文原文](https://research.google/pubs/pub36971/)，这是一个每一个优秀工程师都能通过自己的思考和分析找出的解决方案。

## 思考题

Megastore通过把“实体组”分区，让各个分区相互独立，使得可以有很多组Paxos的日志复制在并行进行。但是，对实体组分区，让它们之间没有业务关联并不是一个很容易的事情。我在这一讲里举了很多电商的例子，你能想一想其中哪些例子，看似各个实体组之间是相互独立没有关联的，但是在实际业务中仍然可能会存在各种关联么？

欢迎你在留言区中分享你的答案和思考，和你的朋友、同学一起讨论，互相交流，共同进步。
<div><strong>精选留言（11）</strong></div><ul>
<li><span>密码123456</span> 👍（1） 💬（1）<p>用paxos，来同步数据。虽然一致性，可以保障。但是更新数据那么频繁，每次同步数据都要2轮通信。而且还是跨数据中心，天然就是慢。那基于什么样的考虑，使用的呢？</p>2023-05-13</li><br/><li><span>在路上</span> 👍（20） 💬（0）<p>徐老师好，Megastore通过对实体组分区，让数据库日志能并行复制，很像在编程的时候，用线程池来处理用户请求，通过对用户id取模的方法，将请求分发给不同的线程，使得用户请求可以被并行处理。用户请求一般只操作自身数据，如果需要操作其他用户的数据，要么加锁，要么丢给对应的线程处理。

在APRG游戏开发中，玩家的数据一般以文档的形式存储，类似于实体组的概念，这份数据包括玩家等级、属性、技能、装备、背包等各种信息。玩家的很多行为都不涉及其他玩家，比如在游戏中签到并领取奖励，只会改变自己的数据。不过如果他需要和其他玩家交易物品，就涉及到“同时”改变自己和对方的数据，要么加锁，要么丢到其他线程或进程处理。如果玩过“奇迹”这款游戏的同学都知道，两个人需要去到同一场景才能完成交易，去同一场景这个行为其实就是让两个人处于同一个线程或进程内，因为一个场景的所有请求会被顺序处理，工程师们通过这个方法简化了交易逻辑的实现难度。</p>2021-11-08</li><br/><li><span>槑·先生</span> 👍（2） 💬（1）<p>先前了解过 TiDB 这种 NewSQL，再看 MegaStore 似乎非常好理解。 </p>2022-06-07</li><br/><li><span>Helios</span> 👍（2） 💬（0）<p>Megastore号称多数据中心的同步，但是是有前提的，是针对同一个分区即实体组。和很多kv数据库舍弃了数据库事务一样，megastore也只能保证实体组内的事务，做做个人的文章集合还可以。就想发微博这种貌似在一个实体组，但是最终涉及到多个，业务越发展并不能保证实体没有关联</p>2021-12-28</li><br/><li><span>核桃</span> 👍（1） 💬（0）<p>再次理解了一下实体组的概念，这个概念的出现，和传统的数据库中的表级锁，行级锁甚至全局锁是否有关系呢？对于传统的数据库来说，行级锁已经是很细粒度的锁了。但是往往一个用户的操作，是涉及到多个不同的表的数据，而Megastore的实体组概念，其实就是把本该属于一个用户对象下所有涉及的表的数据及对象结构包装成一个整体的概念，然后这样的数据进行操作，就和以前的行级锁思想有点类似了，但是更加适合大数据及分布式环境下。

同时对于跨越实体组的事务，使用异步复制这个方案，这里其实也有一个缺陷的。当队列中如果数据满了，或者前面有一个事务很久都没搞定出现问题，那么队列就可能会出现各种问题了，所以这里可以出现二级队列。 做法就是一级队列是接受到跨越实体组的事务请求，但是如果事务执行失败或者有问题了，那么尝试一定次数之后，直接扔到二级队列去处理，不要影响到后续的处理，同时也可以引入优先队列等尝试，这样就更加完善了。</p>2022-02-26</li><br/><li><span>吴小智</span> 👍（1） 💬（0）<p>实体组的多少需要提前定义嘛？实体组的扩缩容怎么办？</p>2021-11-16</li><br/><li><span>陈迪</span> 👍（1） 💬（0）<p>你下单，我下单，但都要扣共同的、全局的商品</p>2021-11-16</li><br/><li><span>Hadesu</span> 👍（0） 💬（0）<p>1. 异步消息队列是不是分布式的？
2. 实例组请求到异步消息队列失败怎么处理？
3. 异步消息队列请求到实例组失败怎么处理？</p>2024-12-03</li><br/><li><span>核桃</span> 👍（0） 💬（2）<p>这里有个难题，对于同一个实体组里面写入的时候，怎么知道先后顺序呢？例如还是三副本机制下，往A节点的实体组1 写入的数据，然后中断了，再考虑往B中写入的话，怎么知道两次写入的先后呢？

这里的隐藏条件就是实体组之间是否需要分主次副本机制，如果分了，那么还是先找主来写入的话，当用户距离切换了，导致写入主的时候延迟比较大该怎么办？ 

如果不分的话，我想到的一种解决策略就是写入之前，先注销掉当前写入的批次的id，这里需要使用到全局唯一的id的方式来解决，再配合上各种修复逻辑才能完善实体组的概念吧。噢，把其他的内容串联起来了。</p>2022-02-24</li><br/><li><span>CRT</span> 👍（0） 💬（0）<p>不同数据中心之间的数据分区，这里的分区应该理解为数据副本更加合适？</p>2021-11-19</li><br/><li><span>扭高达💨🌪</span> 👍（0） 💬（0）<p>Megastore有点像hdfs同步元数据，通过journal node或者bookkeeper写入元数据 其他的namenode异步消费同步元数据</p>2021-11-11</li><br/>
</ul>