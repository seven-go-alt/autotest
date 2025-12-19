# 贡献指南

欢迎为本项目做出贡献！本文档说明如何设置开发环境、运行测试，以及在 CI/CD 中配置通知。

## 开发环境设置

### 前置条件

- Python 3.9+
- Git

### 本地设置

1. **克隆仓库**

```bash
git clone https://github.com/your-org/autotest.git
cd autotest
```

2. **创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
python -m playwright install
```

4. **（可选）运行测试**

```bash
python run_test.py
```

## 提交工作流

1. 创建 feature 分支: `git checkout -b feature/your-feature`
2. 编写/修改测试用例
3. 运行本地测试通过
4. 提交 commit 与 push: `git push origin feature/your-feature`
5. 在 GitHub 上创建 Pull Request

## CI / CD 配置

本项目使用 GitHub Actions 与 Jenkins（可选）运行自动化测试。为启用通知功能，请按以下步骤配置 Secrets：

### GitHub Actions Secrets

1. 打开仓库页面 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret** 并添加以下内容：

#### Slack 通知（可选）

- **Name**: `SLACK_WEBHOOK`
- **Value**: 你的 Slack Incoming Webhook URL（格式：`https://hooks.slack.com/services/TXXXX/BXXXX/XXXXXX`）

获取方式：
- 打开 Slack workspace → **Apps** → **App Manifests** 或搜索 **Incoming Webhooks**
- 创建新的 Incoming Webhook，复制 webhook URL

#### 邮件通知（可选，推荐用 SMTP）

- **Name**: `SMTP_HOST` | **Value**: `smtp.gmail.com` （或你的 SMTP 服务器）
- **Name**: `SMTP_PORT` | **Value**: `587` （通常 SMTP 端口）
- **Name**: `SMTP_USER` | **Value**: 你的 SMTP 用户名/邮箱
- **Name**: `SMTP_PASSWORD` | **Value**: 你的 SMTP 密码（建议使用应用密码而非账户密码）
- **Name**: `SMTP_RECIPIENT` | **Value**: 接收报告的邮箱地址

示例（Gmail）：
- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USER`: `your-email@gmail.com`
- `SMTP_PASSWORD`: 从 [Google Account](https://myaccount.google.com/apppasswords) 生成的应用密码
- `SMTP_RECIPIENT`: 接收邮箱地址

### Jenkins Credentials（如使用 Jenkins）

1. 打开 Jenkins 首页 → **Manage Jenkins** → **Credentials**
2. 在 **System** → **Global** 下创建新凭证
3. 选择类型 **Secret text**，输入 Slack webhook 地址，ID 设置为 `slack-webhook`
4. 在 Job 配置中设置环境变量 `SLACK_CREDENTIAL_ID=slack-webhook`

具体参考 `Jenkinsfile` 与 `docs/CI.md`。

## 代码风格

- Python: 遵循 PEP 8，使用 4 空格缩进
- Robot Framework: 使用 2 空格缩进，关键字首字母大写
- 自定义库：在 `utils/` 下编写，遵循类与方法命名规范

## 测试规范

### pytest 测试

- 位置：`tests/test_*.py`
- 使用 marker：`@pytest.mark.selenium`, `@pytest.mark.playwright`, `@pytest.mark.smoke`
- 命令：`pytest tests/ -v`

### Robot Framework 测试

- 位置：`tests/robotframework/`
- 使用自定义库（`utils/robot_custom_library.py`）和通用关键字（`tests/resources/common.robot`）
- 命令：`python -m robot --outputdir reports/robotframework tests/robotframework/`

## 提交规范

提交信息应清晰简洁，例如：

```
feat: add new Playwright keyword for waiting
fix: correct timeout handling in SeleniumHelper
docs: update QUICKSTART.md with CI guide
```

## 问题与建议

有 Bug 或功能建议？欢迎提交 Issue 或 PR。请附上：
- 问题描述
- 复现步骤（如适用）
- 预期行为 vs 实际行为
- 环境信息（OS、Python 版本、浏览器等）

## 许可证

本项目使用 MIT 许可证。详见 LICENSE 文件。
