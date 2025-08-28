import yaml
from orchestrator.policy.engine import PolicyEngine
from orchestrator.util.settings import settings


def load_policy():
    with settings.policy_file.open() as f:
        return yaml.safe_load(f)


def test_rbac_deny_outlook():
    engine = PolicyEngine(load_policy())
    try:
        engine.pre_check("viewer", "outlook.send_mail", {})
    except PermissionError:
        pass
    else:
        assert False, "viewer should not access outlook.send_mail"


def test_jira_allowed_with_required_arg():
    engine = PolicyEngine(load_policy())
    engine.pre_check("viewer", "jira.search_issues", {"jql": "project=TEST"})
