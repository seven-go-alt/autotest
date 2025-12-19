# CI/CD 配置与通知说明

本说明覆盖 GitHub Actions 与 Jenkins 的报告收集与通知配置。

## GitHub Actions

工作流位于 `.github/workflows/ci.yml`。已包含如下步骤：

- 安装依赖 (`requirements.txt`) 与 Playwright 浏览器
- 运行 `pytest` 并生成 HTML 报告到 `reports/pytest_report.html`
- 运行 Robot Framework 并输出到 `reports/robotframework/`
- 上传 `reports/` 为 artifact

可选通知（需要在 GitHub 仓库中配置 Secrets）：

- `SLACK_WEBHOOK`：Slack Incoming Webhook URL。工作流会在构建完成时向该 webhook 发送一条简短通知。
- `NOTIFY_EMAIL`：接收构建报告的邮箱地址。现已改用 Python SMTP（更可靠）。需要配置以下 Secrets：
  - `SMTP_HOST`：SMTP 服务器地址，例如 `smtp.gmail.com`
  - `SMTP_PORT`：SMTP 端口，通常 `587`（StartTLS）或 `465`（SSL），默认 `587`
  - `SMTP_USER`：SMTP 用户名/邮箱地址
  - `SMTP_PASSWORD`：SMTP 密码或应用密码（建议用应用密码而非账户密码）
  - `SMTP_RECIPIENT`：接收邮件的地址

在 GitHub 仓库中设置 Secrets：

1. 打开仓库页面 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`。
2. 添加 `SLACK_WEBHOOK` 或 `NOTIFY_EMAIL`。

示例：
- 名称：`SLACK_WEBHOOK`
- 值：`https://hooks.slack.com/services/TXXXX/BXXXX/XXXXXX`

注意：Slack 通知示例使用 `jq` 与 `curl`；如果 runner 没有 jq，可改用纯字符串构造或使用 marketplace action。

## Jenkins

Jenkinsfile 已改为参数化 pipeline，Job 可通过以下参数控制执行行为：

- `PYTHON_VERSION`：Python 版本（默认 3.9）
- `ENABLE_SLACK`：启用 Slack 通知（bool）
- `ENABLE_EMAIL`：启用邮件通知（bool）
- `SLACK_CREDENTIAL_ID`：Jenkins 凭证 ID（默认 `slack-webhook`）
- `NOTIFY_EMAIL`：邮件地址

在 Jenkins 中创建或编辑 Job：

1. 勾选 **This project is parameterized**
2. 添加以下参数：
   - String parameter：`PYTHON_VERSION` = `3.9`
   - Boolean parameter：`ENABLE_SLACK` = false
   - Boolean parameter：`ENABLE_EMAIL` = false
   - String parameter：`SLACK_CREDENTIAL_ID` = `slack-webhook`
   - String parameter：`NOTIFY_EMAIL` = （默认空）

3. 在 **Pipeline** 部分选择 **Pipeline script from SCM**，指向本仓库的 `Jenkinsfile`
4. 保存并运行 Job，可在 **Build with Parameters** 中设置通知选项

### 凭证设置

- Slack：在 Jenkins 管理 → 凭证 → System → Global → 添加凭证，选择 `Secret text`，输入 Slack webhook，ID 设置为 `slack-webhook`。
- Email：需在 Jenkins 管理 → 系统配置中配置 SMTP 并安装 `email-ext` 插件。

## 报告收集

仓库包含两个辅助脚本：

- `scripts/ci_run.sh`：在 CI 节点上安装依赖并运行测试，最后打包 reports。
- `scripts/collect_reports.py`：将 `reports/` 打包为 zip 并列出内容。

## 建议

- 在 CI 上使用 `python -m playwright install` 来下载浏览器二进制。
- 在 GitHub Actions 中使用 Python SMTP 发送邮件更可靠（已实现）；在 Jenkins 中使用 `email-ext` 插件。
- 把敏感信息（webhook、SMTP 凭证）放在 GitHub Secrets 或 Jenkins Credentials 中，切勿把凭证写入仓库。
- 参考 `CONTRIBUTING.md` 了解如何配置 GitHub Secrets 与 Jenkins Credentials。

## 快速参考

### GitHub Actions Secrets 列表

| Secret | 用途 | 示例 |
|--------|------|------|
| `SLACK_WEBHOOK` | Slack 通知 | `https://hooks.slack.com/services/...` |
| `SMTP_HOST` | 邮件 SMTP 服务器 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SMTP_USER` | SMTP 用户 | `your-email@gmail.com` |
| `SMTP_PASSWORD` | SMTP 密码/应用密码 | （密码） |
| `SMTP_RECIPIENT` | 邮件收件人 | `recipient@example.com` |

### Jenkins Job 参数列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `PYTHON_VERSION` | String | `3.9` | Python 版本 |
| `ENABLE_SLACK` | Boolean | false | 启用 Slack 通知 |
| `ENABLE_EMAIL` | Boolean | false | 启用邮件通知 |
| `SLACK_CREDENTIAL_ID` | String | `slack-webhook` | Jenkins Slack 凭证 ID |
| `NOTIFY_EMAIL` | String | （空） | 邮件收件人地址 |
