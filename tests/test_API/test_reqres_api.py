"""
接口测试示例：基于 https://reqres.in 提供的公开接口
"""
import pytest
import requests
import config.settings as settings

API_BASE = settings.API_BASE_URL.rstrip("/")


@pytest.mark.api
@pytest.mark.parametrize(
    "page,expected_first_id",
    [
        (1, 1),
        (2, 7),
    ],
)
def test_list_users(page, expected_first_id):
    """分页获取用户列表"""
    resp = requests.get(f"{API_BASE}/users", params={"page": page}, timeout=10)
    assert resp.status_code == 200
    data = resp.json()
    assert data["page"] == page
    assert data["data"], "返回数据为空"
    assert data["data"][0]["id"] == expected_first_id


@pytest.mark.api
@pytest.mark.parametrize(
    "name,job",
    [
        ("morpheus", "leader"),
        ("neo", "the one"),
    ],
)
def test_create_user(name, job):
    """创建用户"""
    resp = requests.post(f"{API_BASE}/users", json={"name": name, "job": job}, timeout=10)
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == name
    assert body["job"] == job
    assert "id" in body


@pytest.mark.api
@pytest.mark.parametrize(
    "email,should_pass",
    [
        ("eve.holt@reqres.in", True),
        ("invalid@example.com", False),
    ],
)
def test_login(email, should_pass):
    """登录接口（校验成功/失败场景）"""
    payload = {"email": email, "password": "cityslicka"}
    resp = requests.post(f"{API_BASE}/login", json=payload, timeout=10)
    if should_pass:
        assert resp.status_code == 200
        assert "token" in resp.json()
    else:
        assert resp.status_code == 400
        assert "error" in resp.json()

