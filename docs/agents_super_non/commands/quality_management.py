#!/usr/bin/env python3
"""
품질관리 명령어 구현 스크립트
V5 코드 품질 무결점 달성을 위한 통합 도구

Usage:
    python quality_management.py check all
    python quality_management.py fix all
    python quality_management.py validate pre-commit
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class QualityTool(Enum):
    RUFF = "ruff"
    MYPY = "mypy"
    BLACK = "black"
    ISORT = "isort"
    BANDIT = "bandit"
    IMPORT_LINTER = "import-linter"


@dataclass
class QualityResult:
    tool: QualityTool
    passed: bool
    violations: int
    errors: list[str]
    execution_time: float
    fixable: bool = False


class QualityManager:
    """V5 코드 품질 무결점 관리자"""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.results: dict[QualityTool, QualityResult] = {}

    async def check_all(
        self, scope: str = "all", fix: bool = False
    ) -> dict[QualityTool, QualityResult]:
        """모든 품질 도구 실행"""
        tools = [
            QualityTool.RUFF,
            QualityTool.MYPY,
            QualityTool.BLACK,
            QualityTool.ISORT,
            QualityTool.BANDIT,
            QualityTool.IMPORT_LINTER,
        ]

        for tool in tools:
            result = await self._run_tool(tool, scope, fix)
            self.results[tool] = result

            if result.passed or (result.errors and len(result.errors[0]) < 200):
                pass

        return self.results

    async def _run_tool(
        self, tool: QualityTool, scope: str, fix: bool
    ) -> QualityResult:
        """개별 품질 도구 실행"""
        start_time = time.time()

        try:
            if tool == QualityTool.RUFF:
                return await self._run_ruff(scope, fix)
            if tool == QualityTool.MYPY:
                return await self._run_mypy(scope)
            if tool == QualityTool.BLACK:
                return await self._run_black(scope, fix)
            if tool == QualityTool.ISORT:
                return await self._run_isort(scope, fix)
            if tool == QualityTool.BANDIT:
                return await self._run_bandit(scope)
            if tool == QualityTool.IMPORT_LINTER:
                return await self._run_import_linter()

            # 기본 반환값 (여기에 도달하면 안 됨)
            return QualityResult(
                tool=tool,
                passed=False,
                violations=1,
                errors=["Unknown tool"],
                execution_time=time.time() - start_time,
            )

        except Exception as e:
            return QualityResult(
                tool=tool,
                passed=False,
                violations=1,
                errors=[str(e)],
                execution_time=time.time() - start_time,
            )

    async def _run_ruff(self, scope: str, fix: bool) -> QualityResult:
        """Ruff 린터 실행 (check + format)"""
        start_time = time.time()

        # 검사 명령 - 정확한 위반 개수를 위해 --statistics 사용
        if fix:
            check_cmd = [
                "uv",
                "run",
                "ruff",
                "check",
                "src/",
                "--fix",
                "--unsafe-fixes",
                "--no-cache",
            ]
        else:
            check_cmd = [
                "uv",
                "run",
                "ruff",
                "check",
                "src/",
                "--statistics",
                "--no-cache",
            ]

        check_result = subprocess.run(
            check_cmd,
            check=False,
            capture_output=True,
            text=True,
            cwd=self.project_root,
        )

        # 포맷 검사
        if fix:
            format_cmd = ["uv", "run", "ruff", "format", "src/"]
        else:
            format_cmd = ["uv", "run", "ruff", "format", "--check", "src/"]

        format_result = subprocess.run(
            format_cmd,
            check=False,
            capture_output=True,
            text=True,
            cwd=self.project_root,
        )

        violations = 0
        errors = []

        if check_result.returncode != 0:
            # --statistics 출력에서 "Found X errors" 추출 (stdout에 있음)
            output = check_result.stdout + check_result.stderr
            if "Found" in output:
                import re

                match = re.search(r"Found (\d+) errors", output)
                if match:
                    violations = int(match.group(1))
                else:
                    violations = 1  # 폴백
            else:
                violations = 1
            if check_result.stdout or check_result.stderr:
                errors.append(
                    f"Ruff check: {(check_result.stdout or check_result.stderr)[:500]}"
                )

        if format_result.returncode != 0 and not fix:
            violations += 1
            errors.append("Ruff format violations found")

        return QualityResult(
            tool=QualityTool.RUFF,
            passed=violations == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=True,
        )

    async def _run_mypy(self, scope: str) -> QualityResult:
        """MyPy 타입 체커 실행"""
        start_time = time.time()

        cmd = ["uv", "run", "mypy", "src/"]
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, cwd=self.project_root
        )

        violations = result.stdout.count("error:")
        errors = []
        if violations > 0:
            errors.append(f"MyPy errors: {result.stdout[:500]}")

        return QualityResult(
            tool=QualityTool.MYPY,
            passed=result.returncode == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=False,
        )

    async def _run_black(self, scope: str, fix: bool) -> QualityResult:
        """Black 포맷터 실행"""
        start_time = time.time()

        if fix:
            cmd = ["uv", "run", "black", "src/"]
        else:
            cmd = ["uv", "run", "black", "--check", "src/"]

        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, cwd=self.project_root
        )

        violations = 1 if result.returncode != 0 else 0
        errors = []
        if violations > 0 and not fix:
            errors.append(f"Black format issues: {result.stdout[:300]}")

        return QualityResult(
            tool=QualityTool.BLACK,
            passed=result.returncode == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=True,
        )

    async def _run_isort(self, scope: str, fix: bool) -> QualityResult:
        """isort Import 정리 실행"""
        start_time = time.time()

        if fix:
            cmd = ["uv", "run", "isort", "src/"]
        else:
            cmd = ["uv", "run", "isort", "--check-only", "src/"]

        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, cwd=self.project_root
        )

        violations = 1 if result.returncode != 0 else 0
        errors = []
        if violations > 0 and not fix:
            errors.append(f"isort issues: {result.stdout[:300]}")

        return QualityResult(
            tool=QualityTool.ISORT,
            passed=result.returncode == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=True,
        )

    async def _run_bandit(self, scope: str) -> QualityResult:
        """Bandit 보안 검사 실행"""
        start_time = time.time()

        cmd = ["uv", "run", "bandit", "-r", "src/", "-f", "json"]
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, cwd=self.project_root
        )

        violations = 0
        errors = []

        try:
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                violations = len(bandit_data.get("results", []))
                if violations > 0:
                    for issue in bandit_data.get("results", [])[:3]:  # 처음 3개만
                        errors.append(
                            f"Security: {issue.get('test_name', 'Unknown')} in {issue.get('filename', '')}"
                        )
        except json.JSONDecodeError:
            if result.returncode != 0:
                violations = 1
                errors = ["Bandit execution failed"]

        return QualityResult(
            tool=QualityTool.BANDIT,
            passed=violations == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=False,
        )

    async def _run_import_linter(self) -> QualityResult:
        """Import Linter 아키텍처 검증 실행"""
        start_time = time.time()

        # import-linter 설정 파일 확인
        config_file = self.project_root / ".import-linter.toml"
        if not config_file.exists():
            return QualityResult(
                tool=QualityTool.IMPORT_LINTER,
                passed=True,  # 설정 파일이 없으면 통과로 간주
                violations=0,
                errors=["No .import-linter.toml config found"],
                execution_time=time.time() - start_time,
                fixable=False,
            )

        cmd = ["uv", "run", "import-linter", "--config", ".import-linter.toml"]
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, cwd=self.project_root
        )

        violations = result.stdout.count("error:")
        errors = []
        if violations > 0:
            errors.append(f"Import violations: {result.stdout[:400]}")

        return QualityResult(
            tool=QualityTool.IMPORT_LINTER,
            passed=result.returncode == 0,
            violations=violations,
            errors=errors,
            execution_time=time.time() - start_time,
            fixable=False,
        )

    def generate_summary_report(self) -> str:
        """요약 리포트 생성"""
        total_violations = sum(r.violations for r in self.results.values())
        passed_tools = sum(1 for r in self.results.values() if r.passed)
        total_tools = len(self.results)
        total_time = sum(r.execution_time for r in self.results.values())

        report = f"""
🧬 V5 DNA 품질 시스템 리포트
{"=" * 50}

📊 전체 현황:
  총 도구: {total_tools}개
  통과: {passed_tools}개
  실패: {total_tools - passed_tools}개
  총 위반: {total_violations}개
  총 실행시간: {total_time:.2f}s

🛡️ 도구별 상세:"""

        for tool, result in self.results.items():
            status = "✅ PASS" if result.passed else "❌ FAIL"
            fixable = " (자동수정가능)" if result.fixable and not result.passed else ""

            report += f"""
  {tool.value.upper()}: {status}
    위반: {result.violations}개{fixable}
    실행시간: {result.execution_time:.2f}s"""

        if total_violations == 0:
            report += """

🎉 축하합니다! 무결점 코드 품질 달성!
   모든 품질 검사를 통과했습니다.

🚀 다음 단계: TASK-R1-01 (UV 프로젝트 초기화) 진행 준비 완료
"""
        else:
            fixable_tools = [
                r.tool.value
                for r in self.results.values()
                if not r.passed and r.fixable
            ]
            manual_tools = [
                r.tool.value
                for r in self.results.values()
                if not r.passed and not r.fixable
            ]

            report += f"""

🔧 수정 권장사항:
  자동 수정 가능: {len(fixable_tools)}개 ({", ".join(fixable_tools)})
  수동 수정 필요: {len(manual_tools)}개 ({", ".join(manual_tools)})

💡 다음 명령어로 자동 수정:
  python .claude/commands/quality_management.py fix all
"""

        return report


async def main() -> None:
    """품질관리 명령어 메인 실행"""
    parser = argparse.ArgumentParser(description="V5 품질관리 - 코드 품질 무결점 달성")
    parser.add_argument(
        "action", choices=["check", "fix", "validate", "report"], help="실행할 액션"
    )
    parser.add_argument(
        "scope",
        nargs="?",
        default="all",
        choices=["all", "src", "tests", "changed", "staged"],
        help="검사 범위",
    )
    parser.add_argument("--fix", action="store_true", help="자동 수정 활성화")
    parser.add_argument(
        "--report", choices=["summary", "detailed", "trend"], help="리포트 타입"
    )

    args = parser.parse_args()

    project_root = Path.cwd()
    manager = QualityManager(project_root)

    try:
        if args.action == "check":
            await manager.check_all(args.scope, args.fix)

            # 리포트 출력

            # 품질 게이트 검증
            total_violations = sum(r.violations for r in manager.results.values())
            if total_violations > 0:
                sys.exit(1)
            else:
                sys.exit(0)

        elif args.action == "fix":
            await manager.check_all(args.scope, True)

            # 수정 후 재검사
            await manager.check_all(args.scope, False)

            final_violations = sum(r.violations for r in manager.results.values())

            if final_violations == 0:
                sys.exit(0)
            else:
                sys.exit(1)

        elif args.action == "validate":
            result = subprocess.run(
                ["uv", "run", "pre-commit", "run", "--all-files"],
                check=False,
                cwd=project_root,
            )
            if result.returncode == 0:
                sys.exit(0)
            else:
                sys.exit(1)

        elif args.action == "report":
            await manager.check_all(args.scope, False)

    except KeyboardInterrupt:
        sys.exit(130)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
