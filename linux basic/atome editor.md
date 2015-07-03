#atom 编辑器使用配置

[TOC]

##常用连接
1.  [atom](https://atom.io/)

##安装atom
debain 和 centos系列的可以从官网下载安装包，直接安装。

##中文支持
在setting的style.less文件中，复制如下一段:
```
/* 等宽字体 */
@mono-font-family: "ubuntu mono", "Hiragino Sans GB", "Microsoft YaHei","WenQuanYi Micro Hei", sans-serif;
/* 非等宽字体 */
@font-family: "ubuntu", "Hiragino Sans GB", "Microsoft YaHei","WenQuanYi Micro Hei", sans-serif;
html,
body,
ol,
ul,
li,
h1,
h2,
h3,
h4,
h5,
h6,
div,
p,
span,
pre,
section,
input,
textarea,
.atom-panel,
.status-bar,
.tree-view,
.title,
.current-path,
.tooltip {
    font-family: @font-family;
}
.autocomplete-plus span,
code,
.-tree-view-,
.symbols-view,
.editor {
    font-family: @mono-font-family;
}
.editor {
    font-size: 14px;
}
```
