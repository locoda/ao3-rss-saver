# ao3-rss-saver
[![AO3 RSS Downloader](https://github.com/locoda/ao3-rss-saver/actions/workflows/action.yaml/badge.svg)](https://github.com/locoda/ao3-rss-saver/actions/workflows/action.yaml) 

[![Preview](https://img.shields.io/badge/Preview-ao3--rss--saver.pages.dev-brightgreen?style=plastic)](https://ao3-rss-saver.pages.dev/)
![Repo Size](https://img.shields.io/github/repo-size/locoda/ao3-rss-saver?style=plastic)

由于有一些太太从AO3删文跑路所以尝试从RSS抓取所有我关心的tag的文章……

---

### 一些杂记：

~23/01/20: 呃呃呃呃呃……AO3 RSS的工作方式和想象中不一样，打算重写一下直接从网页抓了……~ 已重写

AO3 RSS 定义在 config.toml内

由于“/”不能作为文件名，在文章名中用“_”替代，在CP名中一般用“:”替代\，并且生成的文件可能会有Windows系统有文件名兼容问题

没有跨文件夹去重
