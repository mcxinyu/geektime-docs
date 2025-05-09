你好，我是赵成，不知不觉我们已经来到了结束语，非常感谢你的一路陪伴。

学完咱们的专栏，我想对于SRE到底是怎么一回事儿这个问题，你应该有一个大致的了解了。就像我们在开篇词中提到的，**SRE真的没有那么神秘**，你平时在做的很多事情本身就属于SRE的范畴，学到这里，你应该对此深有体会了。

其实这个感受我也是在不断实践的过程中总结出来的。刚接触这个概念的时候立马被它吸引，但同时也觉得这东西有点儿高大上，自己有种心有余而力不足的感觉。幸好和团队一起，就是一点一点死磕，解决一个又一个具体的问题，然后因为一直有这样一个大的框架和目标在那里，最后慢慢发现，这个框架居然已经落地得差不多了。如果总结下我自己实践SRE的心路历程，我觉得王阳明《传习录》里的“**知者行之始，行者知之成**”就特别恰当、准确。

你是不是在想，这不就是知行合一嘛，也没啥特殊啊！嗯，确实是，听起来、说起来都挺简单的，但是很多时候我们想要做到还真不容易。

其实，在学习这个课程的过程里，我们也需要知行合一，从知出发，到行完成一个闭环，然后积累新的知，把这个知行的循环一直继续下去。

这么说，有点抽象，这里我特别举咱专栏里一位同学的例子。这位同学名字叫胡凯，他一边学习课程，一边和我探讨一些SRE问题。每次提问，他总是可以带着具体场景和具体问题，非常有针对性，而且针对不同的场景，他又会有自己的一些见解和解决方案，然后在与我讨论的过程中，不断迭代优化他的思路和方案，特别是在SLO设定这一块，因为很多监控指标都是现成的，他马上就根据我们课程里给出的VALET方法，整理出了一个新的表格，这种从更多SLO维度分析稳定性的方法，一下子就解答了他之前一直以单一维度判断稳定性的很多疑惑和问题。

像胡凯这样的同学，我们专栏里还有很多，大家都提出了非常好的问题，也分享了自己的思考和总结。这个我们一起交流探讨的过程，对于我来讲也是一次难得的学习机会，我想这就是“教学相长”的意义吧。

那么，接着这个话题，我再唠叨几句我的期待吧。这个课程基础篇的几讲是我花费心思最大的内容，因为我想从基础上就讲明白SRE的一些概念和理论。说实话，这部分内容也是需要你花费很大的精力和实践去消化的。如果你之前有过一些实践，再结合我们的课程去看的时候，你会发现理解起来就会轻松很多，也会有更多的收获；如果你现在还没有那么多的实践，这些内容你理解起来还没那么直观，那接下来就要抓住工作中的具体场景和问题，先去实践下，再回过头来看这几讲，到时候你肯定会有不一样的理解，我也会在这里，继续等你提出更好的问题来。

所以你看，对于我们从书本、课程中学习到的知识，要想把它们真正地转化为自己的能力，唯一的方法就是实践、思考、优化实践，并且不断重复这个过程。

对于我们要学习的SRE来说，也是这样。我认为很多人之所以没能好好落地SRE，一个最大的障碍不是技术难度、甚至不是组织架构和文化等问题，而是大家先把自己局限在了概念上，很多人深深地沉浸在SRE到底是什么，它跟现在非常流行的DevOps、AIOps、混沌工程以及各类中台的概念到底是怎样的一个关系？我们该怎么选？……**纠结在这样那样的问题中，结果就是在问题漩涡中停滞不前，迈不出第一步，那就永远都走不前去**。

这时候应该怎么做呢？我的建议就是，从你遇到的实际问题出发，从你所在的实际场景出发，解决问题，满足场景需求，先做起来再说，然后参考优秀的实践案例和分享，再做优化和调整。

其实，在蘑菇街实践SRE的时候，我们也不是天天把SRE挂在嘴边，也不是动不动就提DevOps、AIOps这些名词的，相反，我们提到的更多是面对某个场景，我们的容量评估应该怎么做？细化到每个应用、每个接口上限流阈值是多少，降级和熔断的具体判断策略是怎么样的？发生故障时，我们Step by Step的响应过程应该是怎么样的？需要哪些人参与？大家应该怎么协作？对于监控，怎么才能更准确？需要用到什么具体算法，参数应该怎么设定？……

你看，这些问题基本都是针对具体问题和具体场景的，而且针对这些问题和场景业界都已经有非常多的经验和案例供我们参考了，也就是我们大有可为的地方太多了。你可以设想一下，如果这些问题都能够解决得很好，我们是不是就已经达到了SRE的标准了呢？我们是不是就已经是SRE了呢？

我想答案是肯定的。

好了，到这里，我们专栏的内容就全部结束了。Google给我们呈现的SRE是理论性的、指导性的，业内在这方面的实践还是相对稀缺。想要更好地落地SRE，那就需要我们每一个团队和每一个热爱SRE的同行一起实践、一起总结、一起分享。

那还等什么，SRE并不神秘，让我们一起探索出一条适合我们自己的SRE实践之路。

[![](https://static001.geekbang.org/resource/image/0f/77/0ff24b3805b9494193071ab274498777.jpg?wh=1142%2A801)](https://jinshuju.net/f/LpoFKG)
<div><strong>精选留言（15）</strong></div><ul>
<li><span>艾比利夫</span> 👍（11） 💬（1）<p>谢谢老师一个月的分析，一章不差的看完了，收获颇深。

我和大家不太一样，我在一个小公司就职。所以在学习各种大厂体系的过程中，总有一个困惑，就是体系很牛，但我没法用，因为小公司无论人力资源、技术能力、硬件能力等都太小了，即使理论上学了，但根本无法耗时耗力搭建这么一套东西。

但这次我学习咱们的SRE体会就不太一样，我先了解了MTBF、MTTR(更细的说是MTTR里的四个阶段)，然后对照我们公司的自身的情况对照着表格看，看看是哪个环节是目前的薄弱环节。这样即使我无法向您一样搭建整个体系，我也能针对性的解决最薄弱的环节。

但老师您在课程中也有说：SRE是一套体系，多部门合作出来的，并不是某一个点或某一个技术，那请问老师，对于我们这些中小型公司，资源有限，那怎么做才能让系统全方位的稳定起来呢？</p>2020-04-10</li><br/><li><span>天草二十六</span> 👍（6） 💬（1）<p>大清早看到更新了，第一时间转发了这段到朋友圈：其实，在蘑菇街实践 SRE 的时候，我们也不是天天把 SRE 挂在嘴边，也不是动不动就提 DevOps、AIOps 这些名词的，相反，我们提到的更多是面对某个场景，我们的容量评估应该怎么做？细化到每个应用、每个接口上限流阈值是多少，降级和熔断的具体判断策略是怎么样的？发生故障时，我们 Step by Step 的响应过程应该是怎么样的？需要哪些人参与？大家应该怎么协作？对于监控，怎么才能更准确？需要用到什么具体算法，参数应该怎么设定？……

我想，这才是我要去实践的，不是跟领导或同事灌输思想</p>2020-04-10</li><br/><li><span>李杨</span> 👍（4） 💬（1）<p>谢谢赵老师分享！感觉 DevOps 和 SRE 相辅相成，没有 DevOps 的CI、CD、监控就没有SRE的SLI, SLO。返过来，没有SRE的指标，DevOps也不知道往哪个方向发展。</p>2020-04-25</li><br/><li><span>leslie</span> 👍（4） 💬（1）<p>SER&#47;DevOps与另外一个现在提出很多的概念“中台”类似，落地的过程其实就是循序渐进中梳理出自己的东西；然后不断反复。
概念是浮在面上的东西：如何合理去体现在实践中去摸索相关实践修正这其实是大家需要探索的一条路。概念无处不在如何合理组合然后落地这个是一条漫长的路。
谢谢老师一路的分享，希望将来还有机会交流学习；愿老师未来的路越来越好。</p>2020-04-10</li><br/><li><span>wholly</span> 👍（3） 💬（1）<p>跟着老师把课程学完了，谢谢老师，老师辛苦了！就像老师说的，学习课程还只是一个理论的开始，后面更关键的是结合理论不断实践不断思考，把实际遇到的场景和问题一个个解决闭环，才能真正成为一个优秀的SRE。</p>2020-04-10</li><br/><li><span>Mander</span> 👍（2） 💬（1）<p>感谢老师分享</p>2020-04-10</li><br/><li><span>大尾巴老猫</span> 👍（1） 💬（1）<p>这么快就结束语了？还意犹未尽...</p>2020-04-10</li><br/><li><span>台风骆骆</span> 👍（1） 💬（1）<p>知行合一，从具体场景，业务出发。把学到的知识真正融入到业务中，然后反哺知识，形成闭环</p>2020-04-10</li><br/><li><span>小广</span> 👍（0） 💬（1）<p>感谢赵老师提供了那么优质的课程，特别是课程前面部分的内容，基础性知识讲解得非常细致，这部分内容可移植性和可适配性非常好，对指导改变现实中的问题帮助非常大😄后面我会尝试使用这些指导思想定义我司的稳定性指标，希望能有个好的开始(^_^)v祝老师🐯年顺利</p>2022-02-24</li><br/><li><span>Browser</span> 👍（0） 💬（1）<p>很有收获，目前公司内部也老是遇到各种问题，每次都充当救火队员，根据老师的这份资料，决定实践一下</p>2020-10-24</li><br/><li><span>三毛</span> 👍（0） 💬（1）<p>成哥的课反复看了好几遍，每次都有新的收获，谢谢成哥！</p>2020-09-06</li><br/><li><span>li3huo</span> 👍（0） 💬（1）<p>之前做2C业务时的线上故障大致能分成两类：1种是由软件质量缺陷导致；另外1种就是上章这种大促场景由于扩容不足、预案不充分时错误应对忙中出错。虽然也有事后复盘，但之前的总结没有这么系统，赵老师讲得真的很好！</p>2020-04-22</li><br/><li><span>开心哥</span> 👍（1） 💬（0）<p>知易行难啊。一点点来吧</p>2021-06-02</li><br/><li><span>Tyrone.Zhao</span> 👍（1） 💬（0）<p>限流阈（yu）值</p>2021-04-21</li><br/><li><span>橙汁</span> 👍（0） 💬（0）<p>牛逼 老师什么时候开直播 我去刷点礼物</p>2025-01-20</li><br/>
</ul>