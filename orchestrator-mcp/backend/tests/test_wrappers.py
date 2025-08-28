from fastapi.testclient import TestClient
from orchestrator.bridge.api import app

client = TestClient(app)


def test_tool_list_namespaced():
    resp = client.get("/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert "jira.search_issues" in data


def test_invoke_jira_requires_arg():
    resp = client.post("/invoke", json={"tool": "jira.search_issues", "args": {}})
    assert resp.status_code == 400
    resp = client.post(
        "/invoke",
        headers={"X-User": "alice", "X-Role": "viewer"},
        json={"tool": "jira.search_issues", "args": {"jql": "project=TEST"}},
    )
    assert resp.status_code == 200
    assert "issues" in resp.json()["result"]


def test_rbac_blocks_outlook():
    resp = client.post(
        "/invoke",
        headers={"X-User": "bob", "X-Role": "viewer"},
        json={"tool": "outlook.send_mail", "args": {"to": "a@b.com", "body": "hi", "password": "s"}},
    )
    assert resp.status_code == 403
