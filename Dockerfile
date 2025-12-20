FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 默认无头运行，适合容器
ENV HEADLESS=true
ENV PLAYWRIGHT_HEADLESS=true

# 预安装 Playwright 浏览器（基础镜像已包含）
RUN playwright install --with-deps chromium

CMD ["bash", "-lc", "pytest tests -v"]

