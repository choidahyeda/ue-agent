"""asset_rules.yaml 로더.

규칙 값은 이 모듈에서 하드코딩하지 않는다. 모든 기준은 YAML에서 읽는다.
UE 에디터 내장 Python에서도 동작하도록 PyYAML 외에는 표준 라이브러리만 쓴다.
"""
import datetime
import os

import yaml

DEFAULT_RULES_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "harness", "specs", "asset_rules.yaml")
)

REQUIRED_RULE_KEYS = ("id", "target", "severity", "title", "why", "fix")
REQUIRED_EXCEPTION_KEYS = ("asset", "rule", "reason", "owner", "expires")
SEVERITIES = ("error", "warning")


class RulesError(ValueError):
    """규칙 파일 형식 오류."""


def normalize_asset_path(asset_path):
    """'/Game/A/B.B' 같은 오브젝트 경로를 '/Game/A/B' 패키지 경로로 바꾼다."""
    package, _, _ = asset_path.partition(".")
    return package.rstrip("/")


def _to_date(value):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        raise RulesError("expires 형식은 YYYY-MM-DD 여야 합니다: {!r}".format(value))


class Rules(object):
    def __init__(self, data):
        self.data = data
        self.version = data.get("version")
        self.categories = data.get("categories") or {}
        self.defaults = data.get("defaults") or {}
        self.naming = data.get("naming") or {}
        self.rules = {}
        for rule in data.get("rules") or []:
            self.rules[rule["id"]] = rule
        self.exceptions = data.get("exceptions") or []
        self._validate()

    def _validate(self):
        if not self.categories:
            raise RulesError("categories 가 비어 있습니다")
        for name, cat in self.categories.items():
            if not cat.get("paths"):
                raise RulesError("카테고리 {} 에 paths 가 없습니다".format(name))
        for rule in self.data.get("rules") or []:
            missing = [k for k in REQUIRED_RULE_KEYS if k not in rule]
            if missing:
                raise RulesError("규칙 {} 에 {} 가 없습니다".format(rule.get("id"), missing))
            if rule["severity"] not in SEVERITIES:
                raise RulesError("규칙 {} severity 값 오류: {}".format(rule["id"], rule["severity"]))
        if len(self.rules) != len(self.data.get("rules") or []):
            raise RulesError("규칙 id 가 중복됩니다")
        for exc in self.exceptions:
            missing = [k for k in REQUIRED_EXCEPTION_KEYS if not exc.get(k)]
            if missing:
                # 무기한 예외 금지: 사유, 담당자, 만료일 모두 필수
                raise RulesError("예외 {} 에 {} 가 없습니다".format(exc.get("asset"), missing))
            if exc["rule"] not in self.rules:
                raise RulesError("예외 {} 가 없는 규칙 {} 를 가리킵니다".format(exc["asset"], exc["rule"]))
            exc["expires"] = _to_date(exc["expires"])

    def category_for(self, asset_path):
        """경로 접두사로 카테고리 이름을 찾는다. YAML에 적힌 순서대로 먼저 매칭되는 것을 쓴다."""
        path = normalize_asset_path(asset_path) + "/"
        for name, cat in self.categories.items():
            for prefix in cat["paths"]:
                if path.startswith(prefix):
                    return name
        return None

    def settings_for(self, asset_path):
        """카테고리 설정에 defaults 를 합친 값. 카테고리가 없으면 None."""
        name = self.category_for(asset_path)
        if name is None:
            return None
        merged = dict(self.defaults)
        merged.update({k: v for k, v in self.categories[name].items() if k != "paths"})
        merged["category"] = name
        return merged

    def rule(self, rule_id):
        return self.rules[rule_id]

    def exception_for(self, asset_path, rule_id, today=None):
        """경로와 규칙 ID가 모두 일치하고 만료되지 않은 예외를 돌려준다. 만료일 당일까지 유효."""
        today = today or datetime.date.today()
        path = normalize_asset_path(asset_path)
        for exc in self.exceptions:
            if normalize_asset_path(exc["asset"]) == path and exc["rule"] == rule_id:
                if exc["expires"] >= today:
                    return exc
        return None

    def expired_exceptions(self, today=None):
        """만료된 예외 목록. 리포트에서 정리 대상으로 알려주는 용도."""
        today = today or datetime.date.today()
        return [exc for exc in self.exceptions if exc["expires"] < today]


def load_rules(path=None):
    path = path or os.environ.get("ASSET_RULES_PATH") or DEFAULT_RULES_PATH
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise RulesError("규칙 파일 최상위가 매핑이 아닙니다: {}".format(path))
    return Rules(data)
