你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

前面两节课我们学习了团队视角下无法根本消除的认知分歧，以及如何围绕测试工序拉齐认知分歧。今天我们就来看看大语言模型（Large Language Model，LLM）在这个过程中能发挥什么作用。

之前课程群里就有同学提出能否从需求开始，用LLM来构造“一条龙的服务”，我们先来讨论一下这个想法在当前（2024年5月）是否可行。

## 无法通过LLM构成工作流

我们在前面的章节中讲述了大量LLM技巧，包含建模、模型验证、任务拆分、测试构造、代码编写等等。几乎覆盖了软件生命周期的全部环节。这时候，我们不禁有一个疑问，我们能否使用LLM拉通所有的环节，构建一个完全基于LLM的工作流？毕竟围绕测试工序，我们还是给过一个类似Devin的方案的。

那么能不能利用多Agents架构，把范围进一步扩展到软件开发的全流程呢？

简单来说，还不能。而且我也不太看好这个方向。想要理解其中的原因，还是要回到认知行为模式上。

当我们和LLM一起完成任务时，**基本上是LLM负责干活人负责喊停**。**那么何时喊停，取决于人对于LLM产生内容质量的判断**。也就是说，人对于问题的认知，和对于质量的理解，决定了最终人与LLM合作结果的质量与效率。那么这就又回到了认知行为模式上。

正如我们在前面课程中讲过的，当我们处在复杂认知模式时（Complex），我们对于问题缺乏深入的理解，以至于无法判断LLM产生结果的有效性；当我们处于庞杂认知模式时（Complicated），我们又需要依赖深入分析才能理解LLM的结果，这必然会降低与LLM合作的效率；而当我们处于清晰模式时（Clear/Obvious），人不再是瓶颈，但是LLM又很难准确生产我们所需要的结果。

最终的结果就是，哪怕我们将整个流程串接成一个完整的流程。我们对于不同节点（建模、模型验证、任务拆分、测试、代码编写）的不同认知，也会极大地降低这个流程的效率。

截止到目前为止（2024年5月），面向全流程的工具，自主成功率大概也只有20-30%左右。

那我们能不能把喊停的工作也交给LLM？也是不太行的。首先，LLM本身不善于定义问题。然后很多情况下，喊停需要的是不可言说知识。比如，是否遵循了某种架构模式，再比如是否处在投资回报率（ROI）最高的需求范围等等。这些本身就很难传递给LLM。

消除掉所有不可能的选项，最后剩下的唯一可能性就是如何通过LLM提高人的认知水平了。

可能与大家构想的不同，**LLM并不能直接提升认知水平**。人的认知水平在某一时刻是一个客观的水准，并不随使用的工具而改变。

比如我们前面课程里的例子，某位架构设计师，将架构模式转化为思维链（Chain of Thought, CoT），拿到这个CoT的团队其他成员，并不会直接提升到和架构师一样的水平。

**他们只是多了一个参考答案而已**。至于CoT返回的任务列表质量如何，还是要依赖于他们自己的判断。他们可能仍然需要通过后续流程，在LLM指引下完成整个开发的过程，然后再根据结果，反思任务划分的是否合理。

也就是说，虽然架构师的目的是以庞杂模式记录下测试工序的不可言说知识，但是初次接触到这个CoT的人，仍然要走过复杂模式，以完成对于这些知识的学习。

所以，我们这门课所讲的很多技巧，**从某种程度上来说，是提供了贴近某个不可言说知识的训练法而已**。当然，可能这也是我们能获得的最佳结构，毕竟我们在讨论的是不可言说知识。

记得我们在第一课里的这一段吗？

> 我经常会用这样一个比喻，比如你看上了某个健身教练的肌肉，那么无论你想花多少钱，他都没办法把肌肉卖给你。他能带给你的是一套训练法。然而通过这套训练法，你增长的是自己的肌肉。**对于不可言说的知识，很多时候我们能从别人那里获得的最好的东西，也就是一套训练法**。而我们能给予别人最好的东西，也是**提供对应的训练法**。

很多时候我们能做的就是提供一套有效的训练法，而基于LLM构造训练法，无论从教还是从学的角度上来讲，恰恰是非常有效的。**所以今天（2024年5月），我们应用LLM最有效的方法，是构造一组辅助工具，以贴近项目的方式，快速培养人员能力**。

## 通过LLM构造团队知识门户

为了实现这个目的，我们可以利用LLM构造团队知识门户。按照分层架构表示的知识门户的架构如下图所示：

![](https://static001.geekbang.org/resource/image/67/30/67ef0b7c71e2602a81c1abf91baffc30.jpg?wh=1719x783)

最基础也是最核心的内容就是知识层，也就是我们在知识过程中提取的所有知识。这里的知识既包含不可言说知识，比如，业务上下文、架构、测试策略等，也可以包含各种显式或隐式知识，比如文档、代码等等。

然后中间的交互层，这里是指与LLM的交互模式，也是知识的主要消费形式。我们前面讲到以任务为核心的各种提示词模版，略有提及的Agent都是与知识交互的主要形式。我们前面针对每种不同的知识，讲解了潜在的不同交互模式，这里就不再重复了。

现在，我们要讲一下两个与显式/隐式知识交互的模式，即RAG和知识图谱。

检索增强生成（Retrieval-Augmented Generation，RAG）是对LLM的输出进行优化的过程。RAG在LLM生成响应之前会参考训练数据源之外的权威知识库。RAG 可以将 LLM 本已强大的功能扩展到特定领域或组织的内部知识库，而且无需重新训练模型。

这是一种改进 LLM 输出的有效方法，可使其在各种情况下保持相关性、准确性和实用性。非常适合用以检索超过LLM上下文限制的信息和内容。

本来我们在课程中也计划了一些构造RAG方面的内容，但是现在的几个改变，使得RAG变得非常容易实现了。第一个改变是，头部大语言模型都极大地增加了上下文窗口（Context Window）的大小，对于中小团队在开发过程中产生的文档和代码，我们只需要将所有内容拼接成一个文件，引入到上下文中即可。对于大型团队，在合理划分模块边界之后，每个模块的认知边界内产生的文档与代码，也不太会超过上下文限制。

第二是头部大语言模型或多或少都对RAG提供了内建的支持，比如ChatGPT的Assistant API，或MyGPTs，都有内建的RAG机制，用起来已经非常方便了。我们就不做过多介绍了。

现在（2024年5月）更新的一个方向是GraphRAG，也就是结合了知识图谱的RAG架构。首先通过LLM提取知识图谱，然后再通过技术图谱的机器学习算法，生产查询时的提示词模板。相当于是结合使用了知识图谱和知识生成，只不过这里生产的是中间环节的提示词模板。这是非常有意思的方向，希望大家可以多多关注。

交互层之上就是知识门户的UI层了，我们在前面讲过，LLM无法构成端到端的流程，那么门户只能以工具集的形式组织，比如下图所示，就是我司AI门户Team AI的样子：

![](https://static001.geekbang.org/resource/image/d3/57/d368441dd8b9a0f46ea87d9be3a65c57.jpg?wh=2752x2153)

除了分层架构之外，我们也可以按照知识产品（Knowledge Product）的形式来构建门户：  
![](https://static001.geekbang.org/resource/image/c0/f5/c06087c56948e6675c443af95350b9f5.jpg?wh=1702x863)

这样我们就可以把LLM封装为一个个独立的产品，正如我们将单体应用拆分为微服务一样。

## 结束语

正如开篇词里我提到的，这门课的初衷是让你更好地利用 LLM 提高效率，以及站在一个更全面的立场上，了解如何将 LLM 引入团队或是组织。感谢你的一路支持陪伴，到此我们的全部课程就结束了，我想你们应该松了一口气，从AI来临的恐慌中彻底解放出来了。

学到现在你应该清楚了，AI展现的逆天的能力，实际上不过是利用了认知差，以及海量的知识积累，在我们的不擅长的领域中，打了我们一个措手不及。而真正来到实际工作里，在我们处于高认知的领域，AI并不一定比我们更有效率。所以我们不要夸大AI解决实际问题的能力，也不要忽略AI在学习和传递知识方面带来的革命性改变。

如果让我现在（2024年5月）总结AI会给软件开发带来什么影响。第一点我会讲，**AI可能让很多从业人士第一次认识到，软件开发是团体赛而不是个人赛**。

可能从大学接触软件开发开始，我们就忽略了这一点。编程作业是自己一个人做的，项目练习可能也是自己一个人做的。我们关注自己的产出，远远大于关注我们对别人的影响。如何有效地影响他人，如何在团队中最大化自己的效率，这些重要的技能，在很多从业人员的职业生涯中，始终都是被忽略的，把篮球打成了乒乓球。

而进入AI时代，我们终于发现，传递知识比产生知识更重要了。毕竟AI不会算命，也不知道你想要什么。我们需要陈述清楚，它才能发挥作用。一个被忽略已久的技能，变成每日必备技能了。这个影响必将是深刻且深远的。

第二点，AI让我们把重点再次放回到对人的关注上，把人看作资产而非成本。资产是需要增值的，而成本需要降低。我们打造更好的人，让更好的人做更好的软件。我们前面讲认知分歧，讲人在AI使用中，是负责喊停的。这都在强调，我们无法通过AI直接抹平认知分歧，只能通过AI辅助学习，来抹平认知分歧。**这都不是什么新观点，但是AI让差距凸显了出来**。

大家可以去一些采纳了AI辅助编程的团队看一看，你会发现在使用AI一段时间之后，团队会觉得AI工具的效率越来越低。**那其实是因为人的认知水平越来越高。逐渐摆脱了复杂认知模式**，也就摆脱了AI工具的甜点位（Sweet spot），去除了一些水分而已。这个时候，再想进一步提升，就要更仔细地关注认知分歧，以及人员的培养了。

总之，无论我们喜欢或是不喜欢，随着AI的逐步普及，软件开发正在回到它应该有的样子，也是我期待了三十年的样子。

最后，我为你准备了一份[调查问卷](https://jinshuju.net/f/KzVpBV)，题目不多，希望你可以几分钟填写一下。很期待能听到你的反馈，说说你对这门课程的想法和建议。
<div><strong>精选留言（6）</strong></div><ul>
<li><span>范飞扬</span> 👍（2） 💬（0）<p>感谢老师！把不变的规律和模式（认知行为模式、知识工程、业务建模、TDD等）掌握好，就能以不变应万变～</p>2024-05-10</li><br/><li><span>听水的湖</span> 👍（1） 💬（0）<p>课外拓展资料（来自徐昊老师）：https:&#47;&#47;www.cio.com&#47;video&#47;2114740&#47;thoughtworks-haiven-goes-beyond-coding-by-integrating-ai-into-software-development-lifecycle.html</p>2024-05-23</li><br/><li><span>aoe</span> 👍（1） 💬（0）<p>感谢老师带来的精彩内容！

意识到「知识管理」是一项核心技能，掌握后不仅能更好的利用 AI，还能增强解决问题的能力。

原来 AI 是这样降维打击的：AI 展现的逆天的能力，实际上不过是利用了认知差，以及海量的知识积累，在我们的不擅长的领域中，打了我们一个措手不及。</p>2024-05-10</li><br/><li><span>文经</span> 👍（0） 💬（0）<p>感谢徐昊老师！这门课就是AI时代下的软件工程师指南！
花了3天看完了一遍，对AI的理解，从原来的混沌状态，变成了复杂甚至庞杂的状态，需要过一段时间再学习一遍。
这门课对AI祛魅，也让我真正重视AI。
就像课程里说的：“所以我们不要夸大 AI 解决实际问题的能力，也不要忽略 AI 在学习和传递知识方面带来的革命性改变。”</p>2024-11-27</li><br/><li><span>Roway</span> 👍（0） 💬（0）<p>总之，无论我们喜欢或是不喜欢，随着 AI 的逐步普及，软件开发正在回到它应该有的样子，也是我期待了三十年的样子。
具体指的什么？意思越来越好了？</p>2024-06-06</li><br/><li><span>术子米德</span> 👍（0） 💬（0）<p>🤔☕️🤔☕️🤔
【R】全流程LLM：还不能，不看好，根因看在认知模型的面上，LLM负责干活，人来负责喊停，并对内容质量进行判定。
本课程的技巧，更多是贴近不可言说知识的【训练法】。构造辅助工具，贴着项目培养人员能力，目前认知下的LLM有效解。
软件开发是团体赛，陈述清楚要每日必备，打造更好的人做更好的软件。
【.I.】Copilot或Co-Pilot，副驾 or 助手，他们能干事情的任何部分、他们会跟我探讨、思考和评估，他们能跟我一起想定义、画设计、敲代码、做测试、写文档。不过，他们对结果不负一点责任。
我，要对结果负责。我，要对定义、设计、代码、测试、文档的任何部分负责。我，要能对这些产物做出质量判定。我，要比以前的我更加能力完备、经验丰富、思路清晰，才能驾驭住这些产物，才能让副驾干好副驾的活，而我来把握质量和担负职责。
忽然想到句话：人有人的好处，大模型有大模型的用处。不见得会成为别人的金句，但已经是我自己的金句。
【Q】是否可以提供些参考资料，接触到更多基于LLM的软件工程方面的思考和探索？还有期待三十年的样子，能否加餐来多给点启发和指引？
— by 术子米德@2024年5月10日</p>2024-05-10</li><br/>
</ul>