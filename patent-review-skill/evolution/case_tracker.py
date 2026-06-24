"""
案例追踪器 - 专利客体适格性审查技能

定期追踪最新审查案例，更新案例数据库。
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional


class CaseTracker:
    """案例追踪器"""
    
    # 案例来源配置
    CASE_SOURCES = {
        "cnipa_cases": {
            "name": "国家知识产权局审查案例",
            "url_pattern": "https://www.cnipa.gov.cn/...",
            "check_interval": "weekly"
        },
        "court_cases": {
            "name": "最高人民法院知识产权法庭判例",
            "url_pattern": "https://ipc.court.gov.cn/...",
            "check_interval": "weekly"
        },
        "review_guide": {
            "name": "专利审查指南官方示例",
            "url_pattern": "https://www.cnipa.gov.cn/...",
            "check_interval": "quarterly"
        }
    }
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        
        # 案例数据库
        self.case_db_path = self.base_path / "workflow" / "knowledge" / "case-database.md"
        self.last_check_file = self.base_path / "evolution" / ".last_check"
        
    def check_updates(self) -> List[Dict]:
        """
        检查最新案例更新
        
        Returns:
            新发现的案例列表
        """
        print("开始检查最新审查案例...")
        
        new_cases = []
        
        # 读取上次检查时间
        last_check = self._get_last_check_time()
        
        # 模拟获取最新案例（实际应调用API）
        # 在实际使用中，这里应该：
        # 1. 调用国家知识产权局API
        # 2. 爬取最高人民法院网站
        # 3. 监控审查指南更新
        
        simulated_cases = self._simulate_case_updates()
        
        for case in simulated_cases:
            if self._is_new_case(case, last_check):
                # 第一性原理验证
                if self._validate_first_principle(case):
                    new_cases.append(case)
        
        # 更新检查时间
        self._update_last_check_time()
        
        # 保存新案例
        if new_cases:
            self._save_new_cases(new_cases)
        
        return new_cases
    
    def _validate_first_principle(self, case: Dict) -> bool:
        """
        第一性原理验证
        
        专利法第二条第二款：技术方案是对要解决的技术问题
        所采取的技术手段构成了技术特征，并且能够产生相应的技术效果。
        """
        # 必须包含三要素之一
        has_tech_element = (
            "tech_problem" in case or
            "tech_means" in case or
            "tech_effect" in case or
            "judgment" in case  # 审查结论
        )
        
        # 不符合第一性的案例类型
        non_tech_patterns = [
            "智力活动的规则和方法",
            "商业模式",
            "游戏规则本身",
            "纯粹的算法",
            "数学公式"
        ]
        
        description = case.get("description", "") + case.get("judgment", "")
        
        for pattern in non_tech_patterns:
            if pattern in description:
                # 如果是明确不授权案例，可以保留
                if "不授权" in description or "驳回" in description:
                    return True
                return False
        
        return has_tech_element
    
    def _simulate_case_updates(self) -> List[Dict]:
        """
        模拟案例更新
        
        实际使用时应替换为真实的数据源
        """
        # 这里模拟一些最新案例
        return [
            {
                "id": f"case-{datetime.now().strftime('%Y%m%d')}-001",
                "source": "审查指南2024示例",
                "title": "涉及大语言模型推理优化方法",
                "description": "通过优化模型推理过程中的内存分配策略，提升推理速度。",
                "tech_problem": "模型推理速度慢",
                "tech_means": "动态内存分配策略",
                "tech_effect": "推理速度提升30%",
                "judgment": "授权 - 涉及计算机系统内部性能改进",
                "tags": ["大模型", "推理优化", "内存管理"],
                "authority": "审查指南"
            },
            {
                "id": f"case-{datetime.now().strftime('%Y%m%d')}-002",
                "source": "最高法知产法庭",
                "title": "基于深度学习的推荐算法",
                "description": "使用神经网络模型进行用户商品推荐。",
                "tech_problem": "推荐精度不高",
                "tech_means": "深度神经网络",
                "tech_effect": "推荐准确率提升",
                "judgment": "不授权 - 商业推荐方法，不构成技术方案",
                "tags": ["推荐算法", "神经网络", "商业方法"],
                "authority": "最高法"
            }
        ]
    
    def _is_new_case(self, case: Dict, last_check: datetime) -> bool:
        """判断是否为新案例"""
        # 简化判断：所有模拟案例都视为新案例
        return True
    
    def _get_last_check_time(self) -> datetime:
        """获取上次检查时间"""
        if self.last_check_file.exists():
            with open(self.last_check_file, "r") as f:
                return datetime.fromisoformat(f.read().strip())
        return datetime.now() - timedelta(days=7)
    
    def _update_last_check_time(self):
        """更新检查时间"""
        with open(self.last_check_file, "w") as f:
            f.write(datetime.now().isoformat())
    
    def _save_new_cases(self, cases: List[Dict]):
        """保存新案例"""
        new_cases_file = self.base_path / "evolution" / "new_cases_pending.json"
        
        existing = []
        if new_cases_file.exists():
            with open(new_cases_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        
        existing.extend(cases)
        
        with open(new_cases_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        print(f"  已保存 {len(cases)} 个新案例到待处理队列")
    
    def generate_case_entry(self, case: Dict) -> str:
        """生成案例条目（Markdown格式）"""
        entry = f"""
### {case.get('title', '未命名案例')}

**来源**: {case.get('source', '未知')}
**编号**: {case.get('id', 'N/A')}

**案情摘要**:
{case.get('description', '')}

**技术要素分析**:
- 技术问题: {case.get('tech_problem', '未明确')}
- 技术手段: {case.get('tech_means', '未明确')}
- 技术效果: {case.get('tech_effect', '未明确')}

**审查结论**: {case.get('judgment', '未明确')}

**关键词**: {', '.join(case.get('tags', []))}

**第一性原理验证**: {"通过" if self._validate_first_principle(case) else "未通过"}
"""
        return entry
    
    def get_tracking_status(self) -> Dict:
        """获取追踪状态"""
        last_check = self._get_last_check_time()
        new_cases_file = self.base_path / "evolution" / "new_cases_pending.json"
        
        pending_count = 0
        if new_cases_file.exists():
            with open(new_cases_file, "r", encoding="utf-8") as f:
                pending_count = len(json.load(f))
        
        return {
            "last_check": last_check.isoformat(),
            "pending_cases": pending_count,
            "sources": list(self.CASE_SOURCES.keys())
        }


def main():
    parser = argparse.ArgumentParser(description="案例追踪器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # update子命令
    update_parser = subparsers.add_parser("update", help="检查更新")
    
    # status子命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    
    args = parser.parse_args()
    
    tracker = CaseTracker()
    
    if args.command == "update":
        cases = tracker.check_updates()
        print(f"\n发现 {len(cases)} 个新案例")
        
    elif args.command == "status":
        status = tracker.get_tracking_status()
        print("\n案例追踪状态:")
        print(f"  上次检查: {status['last_check']}")
        print(f"  待处理案例: {status['pending_cases']}")
        print(f"  追踪来源: {', '.join(status['sources'])}")


if __name__ == "__main__":
    main()
