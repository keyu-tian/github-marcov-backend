# gitee-marcov-backend

[![Keyu Tian/gitee-marcov-backend](https://gitee.com/keyu_tian/gitee-marcov-backend/widgets/widget_card.svg?colors=ffffff,1e252b,323d47,455059,d7deea,99a0ae)](https://gitee.com/keyu_tian/gitee-marcov-backend)

#### 介绍
the backend of MarCov

#### 脚本使用

- 下面三个脚本在 gitbash 中使用 `sh ./xxxx.sh` 运行
    1.  `drop.sh`：进行三个操作：修改时区为 utc+8、删库、新建库。
    2.  `install.sh`：安装 `requirements.txt` 里的 python 库。
    3.  `make_migs.sh`：修改 django 的模型定义后，自动迁移更新数据库

- 下面这个脚本可以 `sh ./search` 运行，也可以直接 `search` 运行
    4.  `search`：搜索某个


#### 提交信息（Commit Message）编写规范

1.  格式为：`[tag] comments`
2.  `[tag]` 只能是其中之一：
    - `[new]`：新功能开发。
    - `[upd]`：正常更新现有功能（**注意**：debug 过程中的更新不是正常更新，所以不是 [upd]，而是下面的 [dbg]）。
    - `[del]`：删除某个代码功能（**注意**：debug 后的删除无用代码不是 [del]，而是下面的 [fix]）。
    - `[dbg]`：debug 过程中的提交，比如暂时修改一些代码，或者添加 debug 代码。
    - `[fix]`：debug 结束，是 fix 一个 bug 的提交，包括删除无用的、用来 debug 的代码。
    - `[ref]`：重构，不改变功能。
    - `[merge]`：仅仅只是 merge 分支。**只有这个 [tag] 不是三个字母，便于记忆。**
3.  `comments` 可以使用中文，简要描述一下这次提交是做了什么。如果只修改了一两个文件，请详细指出是哪个文件；如果修改了多个文件，请简要描述本次修改的大概目的。
4.  请不要在短时间内连续提交；多个提交可以在本地积累之后一次性提交（如果是使用 PyCharm，可以把本地的多个 commit 合并之后，得到一个总的 commit，再一次性提交。这个合并的教程请见最下方）。


#### 风格规范
1.  务必确保代码的可读性，命名不要过短。
2.  使用 4 空格而不是 `\t`（PyCharm 的右下角选择 `4 spaces` 即可）。
3.  如无特别要求，所有的**函数**使用下划线命名法，而不是驼峰（比如 `foo_bar` 而不是 `fooBar`）。
4.  如无特别要求，所有的**类名**使用驼峰命名法，而不是下划线（比如 `fooBar` 而不是 `foo_bar`）。
5.  其他的比较自由。请注意可读性。
6.  后续可能会使用自动检查或者格式化插件。


#### 开发规范

1.  每个开发者独立分支开发
2.  开发完毕、**本地**简单测试完毕后，可以 push 到自己分支。
3.  代码自动审查完毕后可以 merge 到 test 分支，待在**服务器上**测试。
4.  测试完毕的 dev 分支可以被管理员 merge 到 main 分支。
5.  重大版本发布后，在 main 分支上会打上被保护的 tag，并发布 release 版本。


#### 注意事项

1.  杂七杂八的文件（不想同步到 git 上）请列在 .gitignore 里，比如 .idea 这个文件夹。




#### 如何通过 PyCharm 合并多个本地的未 push 上去的 commits：

1.  点击左下角的 git.
2.  点击 `log` 选项卡。
3.  可以在中间看见多个本地的未 push 上去的 commits.
4.  找到这些 commits 里面最早的一个。
5.  右键这一个 commit，点 Interactively Rebase from Here...
6.  `ctrl+a` 全选，点上面的 Squash，在弹出的框里写 Commit Message（最终的一个 message）。
7.  写完之后点一下下面的空白区域，然后可以看到上面所有的 commits 都指向了一个最终的 commit。
8.  点 start rebasing，然后结束。
9.  这个时候再提交，就只有一个 commit 了。

