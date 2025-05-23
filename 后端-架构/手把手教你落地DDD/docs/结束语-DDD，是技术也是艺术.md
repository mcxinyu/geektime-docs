你好，我是钟敬。

在不知不觉间，我们的课程已经接近尾声了。几个月来编写这门课的经历，既是对智力的淬炼，也是对体能的挑战。能够坚持至今，少不了你和其他小伙伴的支持。

在课程即将结束的时候，我又想起了开篇词里说过的这句话——“DDD 不仅是一门技术，更是一门艺术”。今天，我们就来聊聊技术和艺术吧。

“技”和“艺”有时不容易严格区分。不过相对而言，技术更偏重逻辑和套路。要么可以通过逻辑推导出来，要么可以通过套路一步一步地做出来；而艺术更侧重于经验、洞察、甚至审美。

不过，软件开发的审美不是与生俱来的，而是要经过后天的训练习得。就好比，一个数学家看到欧拉公式（见下图），会觉得很美，但没有经过数学训练的话，可能就无感了。

$$  
e^{i \\pi}+1=0  
$$

能够把技术和艺术结合起来，是优秀架构师的基本素养，也是学好 DDD 的关键。软件开发作为一门“技术”比较好理解，那么怎么理解其中的“艺术”呢？咱们就说三个方面吧：权衡的艺术、抽象的艺术、抓住本质的艺术。

## 权衡的艺术

我发现有些小伙伴对于软件开发中的不同选择，常常抱有非黑即白的思想。用Java还是PHP？当然是Java。用面向对象还是贫血模型？当然是面向对象。用JPA还是Mybatis?当然是 Mybatis……

然而，一个成熟的架构师却好像开了一双慧眼。他会看到，同样的业务，可以有不同的模型；同样的模型，可以用不同的代码风格实现；同样的技术需求，可以用不同的策略。

事实上，软件开发的全过程，几乎每一步，都可以有不同的做法，每种做法都有各自的优劣，常常没有绝对的对错。架构师总是秉持谦卑的心态，小心翼翼地分析和权衡，才能做出更好的决策。而很多决策，都存在“艺术”的成分。没有人能保证架构师的每一次决策都是正确的，但是更有经验、更擅于学习的架构师，做出正确决策的概率会更大一些。

怎样才能更清晰地审视自己的决策呢？最好能够把开发过程中每个架构决策的理由都记录下来，以便进一步地优化和演进。一个可以落地的方法是架构决策记录（architectural decision record ），简称ADR。相关信息你可以参考[这个链接](https://github.com/joelparkerhenderson/architecture-decision-record)，也可以通过网络找到更多详细的介绍。

## 抽象的艺术

再说说抽象的艺术。软件开发是个建模过程，而建模过程又是一个抽象过程。没有经过抽象的原始需求只是“形似”，经过抽象的领域模型才能“神似”。这也就是我们要建领域模型的一个重要原因。

同样一个业务，可能有不同的抽象方式，而且都是正确的。如何选择？有时候又是一个艺术问题。

抽象能够更准确地理解业务，也能带来更灵活的软件设计，代价则是理解的难度提高了。例如，在领域建模的过程中，遇到以下情况，抽象程度就会提高。

- 多对多关联
- 指向自身的关联
- 泛化
- 三元关联（ternary association，我们的课程目前只遇到过二元关联）

如果这些因素混合在一起，抽象程度就会进一步增加。

是不是越抽象越好呢？不是。那么抽象到什么程度合适呢？你可能又遇到一个艺术问题了。

## 抓住本质的艺术

我们再来聊聊“抓住本质”的艺术。

所谓“抓住本质”有不同层面的含义。我在这里想说的是，DDD 解决的是软件开发的本质问题。

我们不妨先思考两个有趣的事情。一个是前两年兴起的“低代码”。低代码会让程序员失业吗？

另一个是在这门课程编写过程中，横空出世的 ChatGPT，这是一个会写论文，会编程序的人工智能。可怕的是这一切还刚刚开始。那么，人工智能会让程序员失业吗？

从某个角度来说，软件开发的历史，就是代码越来越“低”的历史。C语言比汇编语言“低”；Java比C语言“低”，现在的“低代码”不过是这个过程的延续。而ChatGPT写程序，是从另一个层面，使软件开发的难度更低。

在这个越来越“低”的过程中，也曾经有若干次宣称取代程序员的技术。60年代的COBOL语言，70年代的 SQL，90年代的“第四代语言”，直到今天的低代码和人工智能。有些程序员在这个过程中真的失业了，有些没有。

没有失业的程序员有两种，一种是不断拥抱新技能的；另一种是学会解决软件开发本质问题的。

我们这里的本质问题不是随便说说，而是来源于大家耳熟能详的“没有银弹”理论。这个思想是图灵奖得主Brooks提出的，怹老人家也是软件工程名著《人月神话》的作者。

![](https://static001.geekbang.org/resource/image/a8/b8/a8162831d566d574ac3c1cd82c7f48b8.jpg?wh=3962x2957)

没有银弹指的是，没有任何一种单一的软件开发技术，能在短期内大幅度提高软件开发效率。理由是什么呢？

Brooks 把软件开发所面临的困难分为本质问题（essence）和非本质问题(accident)。这里说的本质和非本质，又来源于亚里士多德的理论。本质问题，是关于事物中内在不变的属性的。比如一般而言人都有两只手。非本质问题是关于外在变化的属性的，比如人的年龄。

Brooks 认为，软件开发工具的革新，硬件效率的提升，解决的都是软件开发的非本质问题。而由于无法解决本质问题，所以工具的发展对软件开发效率的影响只是渐进的。

那么什么是软件开发的本质问题呢？这包括业务的复杂性、业务的可变性、以及软件的不透明性。

低代码，人工智能编程，目前解决的仍然是软件开发的非本质问题。为什么它们还不能解决本质问题呢？其中一个原因，就是问题中的“艺术”成分。

而你正在学习的 DDD，解决的恰恰是软件开发的本质问题。通过可视化、抽象化、严格化的方法建立领域模型的艺术，仍然无法被人工智能取代。所以你学会了这个本事，暂时应该还没有失业的危险。听到这，是不是觉得开心一些了？

人工智能未来能够掌握这门“艺术”吗？我也不知道。或许将来的某一天，它能掌握。不过那时候，人类面临的就不只是程序员是否失业的问题了。

既然已经到了科幻领域，咱们的讨论还是就此打住吧。

学到现在，你已经站在技术和艺术的十字路口上了。这说明你是一个有追求的程序员。探索的历程虽然艰辛，但是你总能在路途中发现一颗颗“璀璨宝石”。

现在，你已经把 DDD 收入囊中了。追风赶月莫停留，平芜尽处是春山。让我们继续前行，探索前路更多的风景！

我知道有很多同学都在努力学习，默默潜水。在专栏结束的今天，不妨在留言区里聊聊学习这门课的感受和收获。我还准备了一份[毕业问卷](https://jinshuju.net/f/YZJHrI)，希望你能花两三分钟填写一下。

[![](https://static001.geekbang.org/resource/image/9a/8f/9a94cf22a7c9bc58676a03c1b4e6a28f.jpg?wh=1142x801)](https://jinshuju.net/f/YZJHrI)

再次感谢你选择这门课，我们江湖再见！
<div><strong>精选留言（8）</strong></div><ul>
<li><span>扶程星云</span> 👍（2） 💬（1）<p>非常感谢老师的分享，第一次读完，很多地方懵懂，我会不断重复拜读佳作！</p>2023-07-28</li><br/><li><span>Sam_Deep_Thinking</span> 👍（0） 💬（1）<p>非常好的专栏，感谢作者的辛苦付出。</p>2024-11-12</li><br/><li><span>无问</span> 👍（0） 💬（2）<p>钟老师 golang有什么参考的ddd项目吗</p>2023-06-21</li><br/><li><span>Sam Jiang</span> 👍（0） 💬（1）<p>技术也需要洞察力，但是艺术需要想象力。

学这门课让我开了眼界，发现曾经困扰自己的问题，已经有人想出了解决方法。并不是人类一思考，上帝就发笑。感谢钟老师。</p>2023-03-12</li><br/><li><span>quietwater</span> 👍（0） 💬（1）<p>老师能加餐讲讲三元关联吗？
我说说我的猜测：比如一个用户在一个系统里，可以访问两个不同的企业里的数据，在一个企业里的角色是管理员，在另一个企业里的角色客户。这里的业务逻辑就是三元关联，一个用户在不同的企业下，角色不一样。</p>2023-03-11</li><br/><li><span>aoe</span> 👍（0） 💬（2）<p>收获很大，看了钟老师在之前文章中提到的「低配版」DDD，对坚持学习起到了很大帮助。在工作中恰好遇到了「项目管理」的问题，正在使用 DDD 开发一个项目，帮助解决问题。这是一个练习项目，等第一版完成后，分享出来和大家一起讨论。

感谢钟老师带我入门 DDD ！</p>2023-03-10</li><br/><li><span>灵活工作</span> 👍（0） 💬（1）<p>实际项目不会只有一个应用，在自己的项目中实践这门课时遇到的问题是有2个应用，一个是微信小程序，一个是后台管理系统，不知道怎么组织代码目录结构了，2个应用都有自己的restful和repository实现类，2个应用的功能有相同的有不同的，领域模型建模时建了一个包含从两个应用来的所有逻辑，但是repository接口只在domain层，导致两个应用的repository实现类里面的方法有的是空方法，而如果为2个应用在domain层建立自己的repository接口，又会导致领域逻辑不包括来自2个应用的所有逻辑，这样领域逻辑就不完整来，导致不知道怎么建模了？是每个应用单独建模吗？可是它们是一个系统里面的2个应用啊，怎么能单独建模呢？</p>2023-03-10</li><br/><li><span>Geek</span> 👍（1） 💬（0）<p>默默潜水学习，感谢作者分享！</p>2023-03-09</li><br/>
</ul>