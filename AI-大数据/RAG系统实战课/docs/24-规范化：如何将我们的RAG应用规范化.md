你好，我是叶伟民。

到今天为止，我们整个课程的实战案例代码都已经编写完毕。

不过之前的代码是为了让同学们学习起来更轻松更专注，并不符合实际工作的代码规范。比如我们的函数和变量都尽量使用了中文，也基本上没有使用类，更没有添加单元测试，没有应用设计模式等等。

因此，我们需要将这些函数名、变量名从中文改成英文、把代码封装成类，还要添加边界验证条件、添加单元测试用例，应用设计模式等等。我们将使用AI编程助手去完成这一切。

需要注意的是，目前我们还无法一步到位，让AI一次性完成代码规范化任务。不知道同学们有没有听过一个笑话，给AI输入指令：您是一位编程高手，请生成抖音APP的全部代码。显然AI目前是做不到这点的，所以我们还是需要按照今天这节课一步一步地进行规范化。

## 安装AI编程助手

我们第一步是安装AI编程助手。

目前市面上的AI编程助手也有很多款，这节课里我们将使用我日常使用的通义灵码。我们首先打开通义灵码的[官网](https://tongyi.aliyun.com/lingma/download)，按照官网指引下载VSCode的插件。

安装完之后，你将会在VSCode左侧看到以下图标。

![](https://static001.geekbang.org/resource/image/c0/09/c0f7f865f8517da0e288ae3b1665e009.jpg?wh=6904x8808)

点击该图标之后，你将进入以下界面。

![](https://static001.geekbang.org/resource/image/ef/17/efb3a5cce026d5b4d34b35ec543ceb17.jpg?wh=3030x1910)

进行到这里，就说明我们已经成功安装了通义灵码。

## 用AI将函数名变量名从中文改成英文

接下来我们使用通义灵码将函数名变量名从中文改成英文。

我们打开一个.py文件，这里以实战案例2里面的 `feed.py` 为例。打开了 `feed.py` 文件之后，我们选中一个函数，例如`根据元数据过滤新闻`。然后鼠标右键选择`通义灵码`-&gt; `生成优化建议`。

![](https://static001.geekbang.org/resource/image/a6/e7/a69dd106ed20851af81f7dac2f422ee7.jpg?wh=2290x467)

然后我们将会在通义灵码插件界面看到后面的生成结果。

![](https://static001.geekbang.org/resource/image/af/9f/afc0d4d3f30b19fbc947263cf554ef9f.jpg?wh=3352x4894)

我们可以看到，AI给出了这样几条优化建议：

1. 类型转换不一致
2. 异常处理缺失
3. 代码可读性
4. 性能考虑

这里我们先看看代码可读性部分。我们可以看到，函数名、函数的参数名、变量名全部都从中文改成了英文，除此之外，AI还帮我们添加了中文注释。  
![](https://static001.geekbang.org/resource/image/35/1a/35df276a526ebf1fbcd09d1bc3eebf1a.jpg?wh=2961x4333)

然后我们可以点击代码右上方的复制按钮，把代码复制到 `feed.py`。

注意，目前的AI编程助手并不能做到100%准确，只能起到辅助参考的作用。所以你还需要复核一遍，在这个基础上修改。

另外，很有可能在这次优化建议中，AI并没有提出要将函数名变量名从中文改成英文。这时候又该怎么办呢？

很简单，直接给AI追加要求就好了。这时候我们可以在底部的文本输入框输入：请将函数名和变量名改为规范化的英文。

![](https://static001.geekbang.org/resource/image/da/dc/da0ba78ba0846d99ea67f4244bf9f7dc.jpg?wh=2579x1109)

这样就能解决这个问题。这时AI编程助手将会把函数名变量名从中文改成英文。

现在我们搞定了中英文名称转换的问题。除此之外，我们还可以参考其他优化建议进行优化，包括前面提到的类型转换不一致、异常处理缺失、性能考虑等等。

## 用AI添加单元测试用例

除了提供优化建议之外，我们还可以使用AI添加单元测试用例。

我们还是选中刚才的函数`根据元数据过滤新闻`。然后点击鼠标右键选择`通义灵码`-&gt; `生成单元测试`。

![](https://static001.geekbang.org/resource/image/bd/24/bd49aaa9611356f5257a5yy6034f5f24.jpg?wh=2963x582)

然后通义灵码插件界面就会生成后面这样的结果。

![](https://static001.geekbang.org/resource/image/2b/1a/2b695c327ddd772f33fec8e3228dff1a.jpg?wh=2954x2864)

我们可以看到，这里和刚才不一样了，AI并没有生成单元测试用例，而是提示我们用哪个单元测试框架。我的习惯是使用 `pytest`，你也可以根据你的习惯来选择相应的单元测试框架。

点击`使用pytest库`按钮之后，AI将会生成单元测试建议。

![](https://static001.geekbang.org/resource/image/11/2d/11bd165093f92c44ecb340a15a35a02d.jpg?wh=3328x5187)

不过这次我们将要点击代码右上方的`新建文件`按钮，而不是前面提到的`复制`按钮，因为Python单元测试代码一般会放在单独的、文件名包含test字眼的py文件，而不是放在原来的py文件。

然后我们就可以在新建文件的基础上复核和修改单元测试代码了。

## 用AI应用设计模式

接下来我们来点更高级的，尝试用AI应用设计模式。

与前面生成优化建议和生成单元测试不同，目前通义灵码还没有直接应用设计模式的右键菜单。因此需要在通义灵码的输入文本框里输入我们的需求，才能应用设计模式。

我们直接在输入文本框输入：可以对这个函数使用什么设计模式？

这次AI的回答是这样的。

```xml
当然可以！为了更好地组织和扩展代码，我们可以使用一些设计模式来改进 根据元数据过滤新闻 函数。这里有几个常见的设计模式，可以帮助我们更好地管理和扩展这个功能：
1. 策略模式
策略模式允许我们在运行时选择不同的算法或策略。这非常适合处理多种过滤逻辑的情况。
```

它还提供了使用了策略模式之后的示例代码，以及单例模式。

```python
from datetime import date, datetime
import time

class 元数据过滤器:
    def 过滤(self, 元数据列表):
        raise NotImplementedError("子类必须实现此方法")

class 按日期过滤(元数据过滤器):
    def 过滤(self, 元数据列表):
        今天 = date.today()
        今天struct_time格式 = time.struct_time(今天.timetuple())
        return [元数据 for 元数据 in 元数据列表 if 元数据.创建日期 > 今天struct_time格式]

class 按关键词过滤(元数据过滤器):
    def __init__(self, 关键词):
        self.关键词 = 关键词

    def 过滤(self, 元数据列表):
        return [元数据 for 元数据 in 元数据列表 if self.关键词 in 元数据.标题]

class 过滤器管理器:
    def __init__(self):
        self.过滤器 = []

    def 添加过滤器(self, 过滤器):
        self.过滤器.append(过滤器)

    def 应用过滤器(self, 元数据列表):
        结果 = 元数据列表
        for 过滤器 in self.过滤器:
            结果 = 过滤器.过滤(结果)
        return 结果

if __name__ == "__main__":
    # 假设有一个元数据列表
    元数据列表 = [
        {"标题": "新闻1", "创建日期": time.strptime("2023-10-01", "%Y-%m-%d")},
        {"标题": "新闻2", "创建日期": time.strptime("2023-10-02", "%Y-%m-%d")},
        {"标题": "新闻3", "创建日期": time.strptime("2023-09-30", "%Y-%m-%d")},
    ]

    管理器 = 过滤器管理器()
    管理器.添加过滤器(按日期过滤())
    管理器.添加过滤器(按关键词过滤("新闻2"))

    过滤后的元数据 = 管理器.应用过滤器(元数据列表)
    print(过滤后的元数据)
```

```xml
2. 单例模式
单例模式确保一个类只有一个实例，并提供一个全局访问点。这对于全局性的配置或者单例服务非常有用。
```

另外还给出使用了单例模式之后的示例代码。

```python
from datetime import date, datetime
import time

class 元数据过滤器(单例):
    def __init__(self):
        self.过滤器列表 = []

    def 添加过滤器(self, 过滤器):
        self.过滤器列表.append(过滤器)

    def 应用过滤器(self, 元数据列表):
        结果 = 元数据列表
        for 过滤器 in self.过滤器列表:
            结果 = 过滤器.过滤(结果)
        return 结果

class 按日期过滤:
    def 过滤(self, 元数据列表):
        今天 = date.today()
        今天struct_time格式 = time.struct_time(今天.timetuple())
        return [元数据 for 元数据 in 元数据列表 if 元数据.创建日期 > 今天struct_time格式]

class 按关键词过滤:
    def __init__(self, 关键词):
        self.关键词 = 关键词

    def 过滤(self, 元数据列表):
        return [元数据 for 元数据 in 元数据列表 if self.关键词 in 元数据.标题]

if __name__ == "__main__":
    元数据列表 = [
        {"标题": "新闻1", "创建日期": time.strptime("2023-10-01", "%Y-%m-%d")},
        {"标题": "新闻2", "创建日期": time.strptime("2023-10-02", "%Y-%m-%d")},
        {"标题": "新闻3", "创建日期": time.strptime("2023-09-30", "%Y-%m-%d")},
    ]

    过滤器 = 元数据过滤器()
    过滤器.添加过滤器(按日期过滤())
    过滤器.添加过滤器(按关键词过滤("新闻2"))

    过滤后的元数据 = 过滤器.应用过滤器(元数据列表)
    print(过滤后的元数据)
```

通过这些设计模式，你可以更好地组织和扩展代码，使得代码变得更加灵活和可维护。

同学们可能会问，为什么这次AI推荐的设计模式代码还是包含中文？

那是因为我想让同学们更专注更容易理解AI给出的参考代码。同学们完全可以先将代码改成全英文，然后再选中全英文代码之后询问AI：可以对这个函数使用什么设计模式？

课程里主要是为你提供解决方案和思路，除此之外，你还可以输入更多代码规范化指令让AI规范化我们的代码。

## 小结

好了，今天这一讲到这里就结束了，最后我们来回顾一下。这一讲我们学会了四件事情。

第一件事情是安装AI编程助手。这一步是后面所有操作的基础，我们按照通义灵码官网的教程在VSCode安装了AI编程助手插件。

第二件事情是用AI将函数名变量名从中文改成英文。我们可以通过通义灵码的“生成优化建议”右键菜单让AI将函数名变量名从中文改成英文，除此之外，AI还会给出其他优化建议。

第三件事情是用AI添加单元测试用例。我们可以通过通义灵码的“生成单元测试”右键菜单让AI生成单元测试。

第四件事情是用AI应用设计模式。通义灵码右键菜单里目前不支持应用设计模式，因此我们需要在输入文本框输入指令来实现这点，依此类推，我们可以输入其他代码规范化指令让AI帮我们生成更多规范化建议。

## 练习题

请根据这节课所讲的内容把三个实战案例的代码规范化。

欢迎你在留言区和我交流互动，如果这节课对你有启发，也推荐分享给身边更多朋友。
<div><strong>精选留言（1）</strong></div><ul>
<li><span>kevin</span> 👍（1） 💬（1）<p>想什么呢？请问完整的代码在哪里下载？之前的有些代码是缺失的</p>2024-10-28</li><br/>
</ul>