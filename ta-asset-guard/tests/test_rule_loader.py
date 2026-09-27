import datetime
import os
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "checks"))

from rule_loader import Rules, RulesError, load_rules, normalize_asset_path  # noqa: E402

D = datetime.date


class RealRulesTest(unittest.TestCase):
    """실제 asset_rules.yaml 과 test_assets_plan.md 정답지 경로로 확인."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules()

    def test_loads_all_rules(self):
        self.assertEqual(len(self.rules.rules), 14)
        self.assertEqual(self.rules.rule("MESH-002")["params"]["min_lod_count"], 3)

    def test_category_by_path(self):
        cases = {
            "/Game/Environment/Props/Chair_01": "props",
            "/Game/Environment/Architecture/T_Wall": "architecture",
            "/Game/Characters/Hero/T_Hero_Armor_D": "character",
            "/Game/VFX/M_Smoke": "vfx",
            "/Game/UI/T_Icon_Sword_D": "ui",
            "/Game/Environment/Foliage/SM_Grass": "default",
            "/Game/Environment/Props/SM_Bench_01.SM_Bench_01": "props",
        }
        for path, expected in cases.items():
            self.assertEqual(self.rules.category_for(path), expected, path)

    def test_outside_game_has_no_category(self):
        self.assertIsNone(self.rules.category_for("/Engine/BasicShapes/Cube"))
        self.assertIsNone(self.rules.category_for("/GameplayPlugin/SM_X"))

    def test_settings_merge_defaults(self):
        props = self.rules.settings_for("/Game/Environment/Props/T_Barrel_D")
        self.assertEqual(props["texture_max_resolution"], 1024)
        self.assertTrue(props["require_power_of_two"])
        self.assertEqual(props["material_max_samplers"], 8)
        ui = self.rules.settings_for("/Game/UI/T_Icon_Sword_D")
        self.assertFalse(ui["require_power_of_two"])
        self.assertFalse(ui["require_mipmaps"])
        self.assertTrue(self.rules.settings_for("/Game/VFX/M_Smoke")["allow_translucent"])
        self.assertFalse(self.rules.settings_for("/Game/Environment/Architecture/M_Glass")["allow_translucent"])

    def test_hero_armor_exception(self):
        path = "/Game/Characters/Hero/T_Hero_Armor_D"
        self.assertIsNotNone(self.rules.exception_for(path, "TEX-002", today=D(2026, 9, 28)))
        self.assertIsNotNone(self.rules.exception_for(path, "TEX-002", today=D(2026, 12, 31)))
        self.assertIsNone(self.rules.exception_for(path, "TEX-002", today=D(2027, 1, 1)))
        self.assertIsNone(self.rules.exception_for(path, "TEX-001", today=D(2026, 9, 28)))
        self.assertIsNone(self.rules.exception_for("/Game/Environment/Props/T_Barrel_D", "TEX-002", today=D(2026, 9, 28)))


def _rules_from(*parts):
    import yaml
    return Rules(yaml.safe_load("".join(textwrap.dedent(p) for p in parts)))


BASE = """
categories:
  props: {paths: ["/Game/Props/"]}
  default: {paths: ["/Game/"]}
rules:
  - {id: TEX-002, target: Texture2D, severity: error, title: t, why: w, fix: f}
"""


class ValidationTest(unittest.TestCase):
    def test_first_matching_category_wins(self):
        rules = _rules_from("""
        categories:
          default: {paths: ["/Game/"]}
          props: {paths: ["/Game/Props/"]}
        rules: []
        """)
        self.assertEqual(rules.category_for("/Game/Props/SM_A"), "default")

    def test_prefix_needs_folder_boundary(self):
        rules = _rules_from(BASE)
        self.assertEqual(rules.category_for("/Game/PropsExtra/SM_A"), "default")

    def test_expired_exception_ignored_and_listed(self):
        rules = _rules_from(BASE, """
        exceptions:
          - {asset: "/Game/Props/T_A_D", rule: TEX-002, reason: r, owner: o, expires: 2026-01-31}
        """)
        self.assertIsNone(rules.exception_for("/Game/Props/T_A_D", "TEX-002", today=D(2026, 9, 27)))
        self.assertEqual(len(rules.expired_exceptions(today=D(2026, 9, 27))), 1)

    def test_exception_without_expiry_rejected(self):
        with self.assertRaises(RulesError):
            _rules_from(BASE, """
            exceptions:
              - {asset: "/Game/Props/T_A_D", rule: TEX-002, reason: r, owner: o}
            """)

    def test_exception_unknown_rule_rejected(self):
        with self.assertRaises(RulesError):
            _rules_from(BASE, """
            exceptions:
              - {asset: "/Game/Props/T_A_D", rule: TEX-999, reason: r, owner: o, expires: "2026-12-31"}
            """)

    def test_bad_severity_rejected(self):
        with self.assertRaises(RulesError):
            _rules_from(BASE.replace("severity: error", "severity: fatal"))

    def test_duplicate_rule_id_rejected(self):
        with self.assertRaises(RulesError):
            _rules_from(BASE + "  - {id: TEX-002, target: Texture2D, severity: error, title: t, why: w, fix: f}\n")

    def test_load_from_env_path(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write(textwrap.dedent(BASE))
        os.environ["ASSET_RULES_PATH"] = f.name
        try:
            self.assertEqual(list(load_rules().categories), ["props", "default"])
        finally:
            del os.environ["ASSET_RULES_PATH"]
            os.unlink(f.name)

    def test_normalize_asset_path(self):
        self.assertEqual(normalize_asset_path("/Game/A/B.B"), "/Game/A/B")
        self.assertEqual(normalize_asset_path("/Game/A/B"), "/Game/A/B")


if __name__ == "__main__":
    unittest.main()
