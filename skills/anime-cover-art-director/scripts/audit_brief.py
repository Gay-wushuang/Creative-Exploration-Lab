#!/usr/bin/env python3
"""Offline copy audit for JSON briefs; does not generate images or OCR.
Usage: python scripts/audit_brief.py brief.json [rendered_text.txt]
JSON schema: {"required_text":["标题", "cover 某某"], "ratio":"4:3", "roles":{"A":"白发"}}
If rendered_text.txt is supplied, exact substring presence is checked.
"""
import json
import pathlib
import re
import sys


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip())
        return 2
    path = pathlib.Path(sys.argv[1])
    brief = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    required = brief.get("required_text", [])
    if not isinstance(required, list) or not all(isinstance(s, str) and s.strip() for s in required):
        problems.append("required_text 必须为非空字符串数组")
    elif len(required) != len(set(required)):
        problems.append("required_text 存在重复条目")
    ratio = brief.get("ratio", "")
    if not re.fullmatch(r"[1-9]\d*:[1-9]\d*", str(ratio)):
        problems.append("ratio 应为 4:3 等比例格式")
    roles = brief.get("roles", {})
    if roles and not isinstance(roles, dict):
        problems.append("roles 应为对象，明确角色绑定")
    if len(sys.argv) == 3:
        final_text = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
        for t in required if isinstance(required, list) else []:
            if t not in final_text:
                problems.append(f"未找到要求文字：{t}")
    if problems:
        for p in problems:
            print("FAIL:", p)
        return 1
    print(f"PASS: 已检查 {len(required)} 条文字，比例 {ratio}，角色数 {len(roles)}")
    if len(sys.argv) == 2:
        print("NOTE: 未提供成品文字稿；只验证简报本身，无法证明生成图中文字正确")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
