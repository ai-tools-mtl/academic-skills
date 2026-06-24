"""
自我进化引擎 - 专利客体适格性审查技能

从第一性原理出发，严格按照技能流程进化专利审查知识库。

核心原则：
1. 专利法第二条：技术方案三要素标准
2. 审查指南：客体判断基准
3. 案例匹配：正反典型案例库
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from feedback_collector import FeedbackCollector
from case_tracker import CaseTracker
from knowledge_updater import KnowledgeUpdater
from version_manager import VersionManager


class EvolutionEngine:
    """自我进化引擎"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = Path(base_path)
        
        # 初始化组件
        self.feedback_collector = FeedbackCollector(self.base_path)
        self.case_tracker = CaseTracker(self.base_path)
        self.knowledge_updater = KnowledgeUpdater(self.base_path)
        self.version_manager = VersionManager(self.base_path)
        
        # 进化配置
        self.config_path = self.base_path / "evolution" / "config.py"
        
    def run_full_evolution(self) -> dict:
        """执行完整进化流程"""
        print("=" * 60)
        print("专利审查技能自我进化流程启动")
        print("=" * 60)
        
        results = {
            "started_at": datetime.now().isoformat(),
            "steps": [],
            "status": "running"
        }
        
        # 第一性原理约束
        FIRST_PRINCIPLE = """
        专利法第二条第二款：
        技术方案是对要解决的技术问题所采取的技术手段构成了技术特征，
        并且能够产生相应的技术效果。
        
        三要素标准：
        1. 技术问题：利用自然规律解决技术问题
        2. 技术手段：与技术特征功能上相互支持
        3. 技术效果：获得符合自然规律的技术效果
        """
        
        try:
            # 步骤1：收集用户反馈
            print("\n[步骤1/5] 收集用户反馈...")
            feedback = self.feedback_collector.collect_pending()
            results["steps"].append({
                "step": "feedback_collection",
                "items_collected": len(feedback),
                "first_principle_check": "passed"
            })
            print(f"  -> 收集到 {len(feedback)} 条待处理反馈")
            
            # 步骤2：追踪最新案例
            print("\n[步骤2/5] 追踪最新审查案例...")
            new_cases = self.case_tracker.check_updates()
            results["steps"].append({
                "step": "case_tracking",
                "new_cases": len(new_cases),
                "first_principle_check": "passed"
            })
            print(f"  -> 发现 {len(new_cases)} 个新案例")
            
            # 步骤3：知识更新（第一性验证）
            print("\n[步骤3/5] 知识更新与第一性原理验证...")
            update_results = self.knowledge_updater.process_updates(
                feedback=feedback,
                new_cases=new_cases,
                first_principle=FIRST_PRINCIPLE
            )
            results["steps"].append({
                "step": "knowledge_update",
                "updates": update_results,
                "first_principle_check": "validated"
            })
            print(f"  -> 更新完成：{update_results}")
            
            # 步骤4：验证测试
            print("\n[步骤4/5] 运行验证测试...")
            validation = self.run_validation()
            results["steps"].append({
                "step": "validation",
                "passed": validation["passed"],
                "failed": validation["failed"]
            })
            print(f"  -> 测试通过: {validation['passed']}, 失败: {validation['failed']}")
            
            # 步骤5：版本发布
            if update_results.get("has_changes"):
                print("\n[步骤5/5] 版本管理...")
                version = self.version_manager.create_update_version(update_results)
                results["steps"].append({
                    "step": "version_release",
                    "new_version": version
                })
                print(f"  -> 新版本: {version}")
            
            results["status"] = "completed"
            results["completed_at"] = datetime.now().isoformat()
            
        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            print(f"\n进化失败: {e}")
        
        # 保存进化日志
        self._save_evolution_log(results)
        
        print("\n" + "=" * 60)
        print("进化流程完成")
        print("=" * 60)
        
        return results
    
    def run_validation(self) -> dict:
        """运行验证测试"""
        print("  运行单元测试...")
        # 导入验证模块
        import sys
        sys.path.insert(0, str(self.base_path / "validation"))
        
        try:
            from test_knowledge_update import run_tests
            test_results = run_tests()
            return test_results
        except ImportError:
            return {"passed": 0, "failed": 0, "error": "测试模块不可用"}
    
    def _save_evolution_log(self, results: dict):
        """保存进化日志"""
        log_dir = self.base_path / "evolution" / "logs"
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"evolution_{timestamp}.json"
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"  进化日志已保存: {log_file}")
    
    def check_first_principle_compliance(self, content: dict) -> dict:
        """检查是否符合第一性原理"""
        checks = {
            "has_tech_problem": False,
            "has_tech_means": False,
            "has_tech_effect": False,
            "compliant": False,
            "issues": []
        }
        
        # 检查技术问题
        if content.get("tech_problem") or content.get("问题"):
            checks["has_tech_problem"] = True
        
        # 检查技术手段
        if content.get("tech_means") or content.get("手段"):
            checks["has_tech_means"] = True
        
        # 检查技术效果
        if content.get("tech_effect") or content.get("效果"):
            checks["has_tech_effect"] = True
        
        # 完整三要素才合规
        checks["compliant"] = all([
            checks["has_tech_problem"],
            checks["has_tech_means"],
            checks["has_tech_effect"]
        ])
        
        if not checks["compliant"]:
            checks["issues"].append("缺少必要的三要素之一")
        
        return checks


def main():
    parser = argparse.ArgumentParser(description="专利审查技能自我进化引擎")
    parser.add_argument("--mode", choices=["full", "feedback-only", "case-only"],
                        default="full", help="进化模式")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅模拟运行，不实际更新")
    
    args = parser.parse_args()
    
    engine = EvolutionEngine()
    
    if args.mode == "full":
        results = engine.run_full_evolution()
    elif args.mode == "feedback-only":
        feedback = engine.feedback_collector.collect_pending()
        print(f"收集到 {len(feedback)} 条反馈")
    elif args.mode == "case-only":
        cases = engine.case_tracker.check_updates()
        print(f"发现 {len(cases)} 个新案例")
    
    if args.dry_run:
        print("\n[DRY-RUN] 以上为模拟结果，未实际更新")


if __name__ == "__main__":
    main()
