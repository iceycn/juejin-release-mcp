# Git 仓库设置与推送指南

## 1. GitHub 仓库设置

### 创建仓库
1. 访问 https://github.com/new
2. 仓库名称: `user-juejin-mcp`
3. 设置为 Public 或 Private
4. 不要勾选 "Initialize this repository with a README"

### 推送代码
```bash
# 添加 GitHub 远程仓库
git remote add origin https://github.com/yourname/user-juejin-mcp.git

# 推送代码
git push -u origin main
```

## 2. Gitee 仓库设置

### 创建仓库
1. 访问 https://gitee.com/projects/new
2. 仓库名称: `user-juejin-mcp`
3. 设置为开源或私有
4. 不要初始化仓库

### 推送代码
```bash
# 添加 Gitee 远程仓库
git remote add gitee https://gitee.com/yourname/user-juejin-mcp.git

# 推送代码
git push -u gitee main
```

## 3. 同时推送到两个平台

```bash
# 添加两个远程仓库
git remote add origin https://github.com/yourname/user-juejin-mcp.git
git remote add gitee https://gitee.com/yourname/user-juejin-mcp.git

# 推送到 GitHub
git push -u origin main

# 推送到 Gitee
git push -u gitee main

# 后续同时推送
git push origin main && git push gitee main
```

## 4. 更新 pyproject.toml 中的仓库地址

推送完成后，更新 `pyproject.toml` 中的项目 URL：

```toml
[project.urls]
Homepage = "https://github.com/yourname/user-juejin-mcp"
Repository = "https://github.com/yourname/user-juejin-mcp"
Documentation = "https://github.com/yourname/user-juejin-mcp#readme"
Issues = "https://github.com/yourname/user-juejin-mcp/issues"
```

然后提交更新：
```bash
git add pyproject.toml
git commit -m "更新项目仓库地址"
git push origin main && git push gitee main
```
