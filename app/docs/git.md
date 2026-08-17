# 问题拆解
1. `remote origin already exists.`：本地已经绑定过名叫`origin`的远端
2. `Connection closed by 28.0.1.149 port 22` → **SSH 22端口被拦截/代理/防火墙阻断**，这是核心报错，不是权限（先连不上，再谈权限）

## 方案A｜优先：先清理旧origin，再换HTTPS方式绕开22端口（最简单，推荐）
```bash
# 1. 删除旧origin
git remote remove origin

# 2. 改用HTTPS地址（不走22ssh端口）
git remote add origin https://github.com/NEGVS/stock-agent.git

# 3. 推送
git branch -M main
git push -u origin main
```

## 方案B｜坚持用SSH（解决22端口被封）
> 很多公司/WiFi屏蔽ssh 22端口，GitHub支持SSH走443端口
```bash
# 删旧origin
git remote remove origin
# 使用github 443端口ssh地址
git remote add origin ssh://git@ssh.github.com:443/NEGVS/stock-agent.git
git branch -M main
git push -u origin main
```

## 排查小命令（可选）
```bash
# 查看当前远端
git remote -v

# 测试ssh连通性（直接验证是不是端口问题）
ssh -T -p 22 git@github.com
# 测试443ssh
ssh -T -p 443 git@ssh.github.com
```
- 如果`ssh -T -p22`直接报Connection closed → 确认22端口墙了，不要硬用默认ssh

## 补充常见坑确认
- 仓库地址确认：`NEGVS/stock-agent.git` 仓库是否**真实存在**、私有仓库的话当前账号要有权限
- SSH密钥：如果坚持ssh方式，确认本机ssh公钥已经添加到GitHub → Settings → SSH and GPG keys

## 快速建议
优先直接跑【方案A HTTPS】，90%直接解决这个`Connection closed`。
> HTTPS推送时会弹窗/提示输入账号密码，现在GitHub HTTPS不能用账号密码，要用**Personal access token**当密码。
> 如果你需要，我可以直接给你生成token的步骤。

---
### 如果你还是想用SSH长期使用，我可以给你写 `~/.ssh/config` 永久强制github走443端口，以后不用每次改remote地址。


本地 main 分支已经和远端 origin/main 绑定完成，后续直接：

```
git push
git pull
```


# Git 高频常用命令（按场景整理，日常开发直接复制）
> 适配你当前 Mac + GitHub 场景

## 一、初始化 & 远端仓库（刚建项目用，你刚才这套）
```bash
# 初始化git（新项目）
git init

# 查看远端
git remote -v
# 删除远端
git remote remove origin
# 添加远端（两种）
git remote add origin git@github.com:xxx/xxx.git       # SSH
git remote add origin https://github.com/xxx/xxx.git  # HTTPS

# 重命名分支 → main
git branch -M main
# 首次推送并建立追踪关系
git push -u origin main
# 后续直接
git push
git pull
```

## 二、日常提交工作流（最常用）
```bash
# 查看状态
git status

# 添加文件到暂存
git add .                  # 全部变更（慎用，确认status后再用）
git add xxx.py src/        # 指定文件/目录

# 提交（必须加-m备注）
git commit -m "feat: 新增xxx功能"

# 提交后补备注 / 修改最近一次commit信息
git commit --amend
```

## 三、分支操作（开发、feature、hotfix必用）
```bash
# 查看本地分支
git branch
# 查看所有(本地+远端)
git branch -a

# 创建分支
git branch dev
# 创建并直接切换
git checkout -b dev
# 新版推荐（同上面效果）
git switch -c dev

# 切换分支
git checkout main
git switch main

# 删除本地分支（已合并后）
git branch -d dev
# 强制删除（未合并）
git branch -D dev

# 推送新分支到远程
git push -u origin dev
# 删除远程分支
git push origin --delete dev
```

## 四、合并 & 冲突
```bash
# 在main分支合并dev
git checkout main
git merge dev

# 变基（干净线性提交，适合feature分支）
git checkout dev
git rebase main

# 解决完冲突后继续rebase
git add .
git rebase --continue
# 放弃rebase
git rebase --abort
```

## 五、拉取、同步远端
```bash
# 拉取+合并（等价 fetch + merge）
git pull
# 拉取远端信息，不自动合并（安全，推荐先看）
git fetch origin

# 把本地main同步和远端强制对齐（⚠️ 谨慎，会覆盖本地）
git reset --hard origin/main
```

## 六、日志、查看记录
```bash
git log
# 简洁单行
git log --oneline
# 图形化看分支
git log --oneline --graph
# 看最近几条
git log -5
```

## 七、撤销、回滚（高频踩坑区，⚠️ 分清场景）
```bash
# 1. 工作区文件撤销（还没add，丢弃本地修改）
git checkout -- xxx.py
# 新版推荐
git restore xxx.py

# 2. 取消add（暂存→变回工作区，不丢代码）
git reset HEAD xxx.py

# 3. 撤销最近一次commit（代码保留，只是取消提交）
git reset --soft HEAD~1

# 4. 强制回退到某个版本（⚠️ 会丢本地改动）
git reset --hard 【commitHash】

# 5. 已经push到远端的提交要回滚（安全，新增一条reverse commit）
git revert 【commitHash】
```

## 八、储藏（临时切换分支，不想commit半成品）
```bash
# 暂存当前改动
git stash
# 查看储藏列表
git stash list
# 取出最近一次stash（保留stash记录）
git stash apply
# 取出并删除stash
git stash pop
# 删除储藏
git stash drop
```

## 九、Tag（版本打标，v1.0.0）
```bash
# 创建轻量tag
git tag v1.0.0
# 推送tag到远端
git push origin v1.0.0
# 删除本地tag
git tag -d v1.0.0
# 删除远端tag
git push origin --delete v1.0.0
```

## 十、配置（SSH/用户名邮箱）
```bash
# 全局用户名邮箱
git config --global user.name "Andy"
git config --global user.email "xxx@xx.com"
# 查看全局配置
git config --global --list
```

# ✅ 规范小建议（配合你Java/Python项目）
commit 信息规范（约定式提交）
- `feat:` 新功能
- `fix:` bug修复
- `refactor:` 重构，无功能变化
- `docs:` 文档
- `style:` 格式调整
- `chore:` 构建/依赖、脚手架调整

# 📌 最简日常流水线（记住这6条足够80%场景）
```bash
git status
git add .
git commit -m "feat: xxx"
git pull
git push
```




如果你想要，我可以输出一份**可直接存本地的markdown速查表**，或者精简成「极简一页口袋版」。