"""
用户反馈收集器 - 专利审查技能

收集、分类和处理用户反馈，用于技能进化。
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class FeedbackCollector:
    """用户反馈收集器"""
    
    # 反馈类型定义
    FEEDBACK_TYPES = {
        "rule_correction": {
            "name": "规则修正",
            "priority": "P0",
            "description": "审查标准存在错误或遗漏"
        },
        "case_addition": {
            "name": "案例补充",
            "priority": "P1", 
            "description": "缺失重要审查案例"
        },
        "boundary_clarification": {
            "name": "边界澄清",
            "priority": "P2",
            "description": "边界案例需要说明"
        },
        "error_correction": {
            "name": "错误纠正",
            "priority": "P0",
            "description": "事实性错误需要修正"
        },
        "experience_improvement": {
            "name": "体验改进",
            "priority": "P3",
            "description": "流程优化建议"
        }
    }
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        self.feedback_dir = self.base_path / "feedback"
        self.feedback_dir.mkdir(exist_ok=True)
        
        self.pending_file = self.feedback_dir / "pending.json"
        self.processed_file = self.feedback_dir / "processed.json"
        
    def submit(self, feedback_type: str, content: str, 
               evidence: List[Dict] = None, source: str = "unknown",
               contact: str = None) -> str:
        """
        提交用户反馈
        
        Args:
            feedback_type: 反馈类型
            content: 反馈内容
            evidence: 证据材料
            source: 来源标识
            contact: 联系方式（可选）
            
        Returns:
            反馈ID
        """
        if feedback_type not in self.FEEDBACK_TYPES:
            raise ValueError(f"无效的反馈类型: {feedback_type}")
        
        feedback_id = f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        feedback = {
            "id": feedback_id,
            "type": feedback_type,
            "type_name": self.FEEDBACK_TYPES[feedback_type]["name"],
            "priority": self.FEEDBACK_TYPES[feedback_type]["priority"],
            "content": content,
            "evidence": evidence or [],
            "source": source,
            "contact": contact,
            "submitted_at": datetime.now().isoformat(),
            "status": "pending",
            "first_principle_check": None
        }
        
        # 保存到pending
        pending = self._load_pending()
        pending[feedback_id] = feedback
        self._save_pending(pending)
        
        print(f"反馈已提交: {feedback_id}")
        print(f"类型: {feedback['type_name']}")
        print(f"优先级: {feedback['priority']}")
        
        return feedback_id
    
    def collect_pending(self) -> List[Dict]:
        """收集所有待处理的反馈"""
        pending = self._load_pending()
        return list(pending.values())
    
    def classify_feedback(self, feedback: Dict) -> Dict:
        """
        分类反馈并执行第一性原理检查
        
        第一性原理：
        专利法第二条 - 技术方案定义
        三要素：技术问题、技术手段、技术效果
        """
        classification = {
            "category": None,
            "target_file": None,
            "first_principle_valid": False,
            "notes": []
        }
        
        feedback_type = feedback["type"]
        
        if feedback_type in ["rule_correction", "error_correction"]:
            classification["category"] = "规则修正"
            classification["target_file"] = "workflow/knowledge/patent-law-basis.md"
            
            # 第一性检查：是否涉及技术方案三要素
            content = feedback["content"]
            if any(keyword in content for keyword in ["技术问题", "技术手段", "技术效果", "自然规律"]):
                classification["first_principle_valid"] = True
            else:
                classification["notes"].append("警告：未明确涉及技术方案三要素")
                
        elif feedback_type == "case_addition":
            classification["category"] = "案例补充"
            classification["target_file"] = "workflow/knowledge/case-database.md"
            classification["first_principle_valid"] = True  # 案例天然符合第一性
            
        elif feedback_type == "boundary_clarification":
            classification["category"] = "边界澄清"
            classification["target_file"] = "workflow/knowledge/case-database.md"
            classification["first_principle_valid"] = True
            
        elif feedback_type == "experience_improvement":
            classification["category"] = "流程优化"
            classification["target_file"] = "workflow/node-prompts.md"
            classification["first_principle_valid"] = True
        
        return classification
    
    def mark_processed(self, feedback_id: str, result: str):
        """标记反馈已处理"""
        pending = self._load_pending()
        
        if feedback_id in pending:
            feedback = pending.pop(feedback_id)
            feedback["status"] = "processed"
            feedback["processed_at"] = datetime.now().isoformat()
            feedback["result"] = result
            
            # 移动到已处理
            processed = self._load_processed()
            processed[feedback_id] = feedback
            self._save_processed(processed)
            self._save_pending(pending)
            
            print(f"反馈 {feedback_id} 已标记为已处理")
    
    def get_statistics(self) -> Dict:
        """获取反馈统计"""
        pending = self._load_pending()
        processed = self._load_processed()
        
        stats = {
            "pending_total": len(pending),
            "processed_total": len(processed),
            "pending_by_type": {},
            "pending_by_priority": {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        }
        
        for fb in pending.values():
            fb_type = fb.get("type_name", "未知")
            stats["pending_by_type"][fb_type] = stats["pending_by_type"].get(fb_type, 0) + 1
            stats["pending_by_priority"][fb["priority"]] += 1
        
        return stats
    
    def _load_pending(self) -> Dict:
        if self.pending_file.exists():
            with open(self.pending_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_pending(self, data: Dict):
        with open(self.pending_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_processed(self) -> Dict:
        if self.processed_file.exists():
            with open(self.processed_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_processed(self, data: Dict):
        with open(self.processed_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="用户反馈收集器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # submit子命令
    submit_parser = subparsers.add_parser("submit", help="提交反馈")
    submit_parser.add_argument("--type", required=True,
                               choices=list(FeedbackCollector.FEEDBACK_TYPES.keys()),
                               help="反馈类型")
    submit_parser.add_argument("--content", required=True, help="反馈内容")
    submit_parser.add_argument("--source", default="cli", help="来源")
    submit_parser.add_argument("--file", help="证据文件路径")
    
    # list子命令
    list_parser = subparsers.add_parser("list", help="列出待处理反馈")
    list_parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    collector = FeedbackCollector()
    
    if args.command == "submit":
        evidence = []
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                evidence = json.load(f)
        
        collector.submit(
            feedback_type=args.type,
            content=args.content,
            evidence=evidence,
            source=args.source
        )
        
    elif args.command == "list":
        if args.stats:
            stats = collector.get_statistics()
            print("\n反馈统计:")
            print(f"  待处理: {stats['pending_total']}")
            print(f"  已处理: {stats['processed_total']}")
            print("\n  按类型:")
            for t, c in stats["pending_by_type"].items():
                print(f"    {t}: {c}")
            print("\n  按优先级:")
            for p, c in stats["pending_by_priority"].items():
                if c > 0:
                    print(f"    {p}: {c}")
        else:
            pending = collector.collect_pending()
            print(f"\n待处理反馈 ({len(pending)}条):")
            for fb in pending:
                print(f"  [{fb['priority']}] {fb['id']}: {fb['type_name']}")
                print(f"    {fb['content'][:100]}...")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
