# 部署指南

本文档说明如何将翼术师世界网站部署到 GitHub Pages。

## 前置要求

- GitHub 账户
- Git 已安装
- （可选）配置好的 OpenAI 或 Anthropic API Key，用于 AI 冲突检查

## 部署步骤

### 1. 创建 GitHub 仓库

在 GitHub 上创建一个新仓库，例如命名为 `doc`。

### 2. 初始化本地仓库

```bash
cd /path/to/翼术师
git init
git add .
git commit -m "初始提交：翼术师世界网站"
```

### 3. 连接远程仓库

```bash
git remote add origin https://github.com/wingician/doc.git
git branch -M main
git push -u origin main
```

### 4. 启用 GitHub Pages

1. 进入仓库的 Settings
2. 在左侧菜单找到 "Pages"
3. 在 "Build and deployment" 部分：
   - Source: 选择 "GitHub Actions"
4. 保存设置

### 5. 配置 Actions 权限

1. 在 Settings → Actions → General
2. 找到 "Workflow permissions"
3. 选择 "Read and write permissions"
4. 勾选 "Allow GitHub Actions to create and approve pull requests"
5. 保存

### 6. （可选）配置 AI 检查

如果要启用自动冲突检查功能：

1. 在 Settings → Secrets and variables → Actions
2. 添加以下 Secret：
   - `OPENAI_API_KEY`: 你的 OpenAI API Key
   - 或 `ANTHROPIC_API_KEY`: 你的 Anthropic API Key
3. 保存

### 7. 触发部署

推送代码到 main 分支会自动触发部署：

```bash
git push origin main
```

或者在 Actions 标签页手动运行 "部署 GitHub Pages" 工作流。

## 访问网站

部署完成后，你的网站将在以下地址可用：

```
https://wingician.github.io/doc/
```

（将 `wingician` 替换为你的 GitHub 用户名）

## 自定义域名（可选）

如果你有自己的域名：

1. 在仓库根目录创建 `CNAME` 文件
2. 在文件中写入你的域名，例如：
   ```
   wingmaster.example.com
   ```
3. 在你的域名提供商处配置 DNS：
   - 添加 CNAME 记录指向 `<username>.github.io`
   - 或添加 A 记录指向 GitHub Pages 的 IP 地址

## 更新网站

每次推送到 main 分支都会自动重新部署：

```bash
git add .
git commit -m "更新描述"
git push origin main
```

## 分支管理

### 主分支（main）
正式的世界设定，严格审核。

### 创建平行宇宙分支

```bash
# 创建并切换到新分支
git checkout -b branch-steampunk

# 进行修改后推送
git push origin branch-steampunk
```

### 合并分支

通过 Pull Request 进行：
1. 在 GitHub 上创建 PR
2. 等待 AI 自动检查
3. 审核通过后合并

## 故障排除

### 网站无法访问

1. 检查 Actions 标签页，确认部署成功
2. 等待几分钟让 CDN 更新
3. 检查 Settings → Pages 确认已启用

### AI 检查失败

1. 确认已添加 API Key 到 Secrets
2. 检查 API Key 是否有效且有余额
3. 查看 Actions 日志了解具体错误

### 样式未加载

1. 检查 `_config.yml` 中的 `baseurl` 设置
2. 确保 CSS/JS 文件路径正确
3. 清除浏览器缓存

## 本地开发

在本地预览网站：

```bash
# 使用 Python 的简单 HTTP 服务器
cd /path/to/翼术师
python3 -m http.server 8000

# 或使用 Node.js 的 http-server
npx http-server -p 8000
```

然后访问 `http://localhost:8000`

## 维护建议

1. **定期备份**：虽然 Git 提供版本控制，但建议定期备份整个仓库
2. **监控 Issues**：及时回应社区的问题和建议
3. **审核 PR**：认真审核每个 Pull Request，保持世界观一致性
4. **更新依赖**：定期更新 GitHub Actions 版本
5. **文档维护**：保持文档与实际代码同步

## 安全性

- 不要在仓库中提交敏感信息（API Keys 等）
- 使用 GitHub Secrets 存储机密信息
- 定期检查依赖的安全性

## 性能优化

- 压缩图片资源
- 使用 CDN 加载外部库（如 Font Awesome）
- 启用浏览器缓存
- 考虑使用图片懒加载

## 许可证

本项目采用 CC BY-SA 4.0 协议，确保所有贡献者了解并同意此协议。

---

如有问题，请在 GitHub Issues 中提出。
