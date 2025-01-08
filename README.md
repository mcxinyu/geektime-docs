## 极客时间文档

极客时间 markdown | pdf 文档

----

####  注意⚠️：

####  本地下载播放音视频，推荐部署 [mygeektime](https://github.com/zkep/mygeektime)

### [极客课程 pdf文档] (https://github.com/uaxe/geektime-pdfs)

下载课程pdf：
```shell
git clone https://github.com/uaxe/geektime-pdfs.git
```

### 课程 markdown 文档

```shell
git clone https://github.com/uaxe/geektime-docs.git  --depth 1

pip install mkdocs-material

cd 后端\|架构/说透中台/

mkdocs serve
```

浏览器访问：<http://127.0.0.1:8000/>


### 本地生成pdf文档
```shell
git clone https://github.com/uaxe/geektime-docs.git

cd geektime-docs

pip install -r requirements.txt

# -i 参数是你需要生成pdf课程的目录
python3 main.py pdf -i 后端\|架构/etcd实战课

# 执行完成后，确诊最终的pdf是否正常，尤其关注图片
# 建议对照markdown文档检查，如果有问题，欢迎提交 issue
```
