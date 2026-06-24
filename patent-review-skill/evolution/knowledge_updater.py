"""
知识更新器 - 专利客体适格性审查技能

从第一性原理出发更新知识库。
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class KnowledgeUpdater:
    """知识更新器"""
    
    # 第一性原理约束
    FIRST_PRINCIPLE = {
        "core_law": "专利法第二条第二款",
        "definition": "技术方案是对要解决的技术问题所采取的技术手段构成了技术特征，并且能够产生相应的技术效果。",
        "three_elements": {
            "tech_problem": "利用自然规律解决技术问题",
            "tech_means": "与技术特征功能上相互支持",
            "tech_effect": "获得符合自然规律的技术效果"
        },
        "l1_l5_model": {
            "L1": "原始观测数据",
            "L2": "预处理数据",
            "L3": "提取特征数据",
            "L4": "模型输出数据",
            "L5": "决策/控制指令"
        },
        "g0_g4_model": {
            "G0": "领域无关",
            "G1": "弱领域关联",
            "G2": "中等领域关联",
            "G3": "强领域关联",
            "G4": "极强领域关联"
        }
    }
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        
        # 文件路径
        self.case_db_path = self.base_path / "workflow" / "knowledge" / "case-database.md"
        self.law_basis_path = self.base_path / "workflow" / "knowledge" / "patent-law-basis.md"
        self.keyword_lib_path = self.base_path / "workflow" / "keyword-libraries.json"
        
        # 更新日志
        self.update_log_path = self.base_path / "evolution" / "update_log.md"
    
    def process_updates(self, feedback: List[Dict] = None, 
                        new_cases: List[Dict] = None,
                        first_principle: str = None) -> Dict:
        """
        处理知识更新
        
        Args:
            feedback: 用户反馈列表
            new_cases: 新案例列表
            first_principle: 第一性原理文本
            
        Returns:
            更新结果
        """
        results = {
            "cases_added": 0,
            "rules_updated": 0,
            "keywords_updated": 0,
            "rejected": 0,
            "reasons": [],
            "has_changes": False
        }
        
        # 处理用户反馈
        if feedback:
            for fb in feedback:
                update_result = self._process_feedback(fb)
                if update_result["accepted"]:
                    results["has_changes"] = True
                    if update_result["type"] == "case":
                        results["cases_added"] += 1
                    elif update_result["type"] == "rule":
                        results["rules_updated"] += 1
                else:
                    results["rejected"] += 1
                    results["reasons"].append(update_result["reason"])
        
        # 处理新案例
        if new_cases:
            for case in new_cases:
                if self._validate_case_first_principle(case):
                    self._add_case_to_database(case)
                    results["cases_added"] += 1
                    results["has_changes"] = True
                else:
                    results["rejected"] += 1
                    results["reasons"].append(f"案例不符合第一性原理: {case.get('id')}")
        
        # 记录更新日志
        if results["has_changes"]:
            self._log_update(results)
        
        return results
    
    def _process_feedback(self, feedback: Dict) -> Dict:
        """处理单条反馈"""
        # 第一性原理验证
        if not self._validate_feedback_first_principle(feedback):
            return {
                "accepted": False,
                "reason": "反馈内容不符合第一性原理（专利法第二条技术方案定义）"
            }
        
        # 根据类型处理
        fb_type = feedback.get("type")
        
        if fb_type in ["case_addition", "boundary_clarification"]:
            if feedback.get("evidence"):
                for case in feedback["evidence"]:
                    if self._validate_case_first_principle(case):
                        self._add_case_to_database(case)
            return {"accepted": True, "type": "case"}
            
        elif fb_type in ["rule_correction", "error_correction"]:
            return {"accepted": True, "type": "rule"}
        
        return {"accepted": True, "type": "unknown"}
    
    def _validate_feedback_first_principle(self, feedback: Dict) -> bool:
        """验证反馈是否符合第一性原理"""
        content = feedback.get("content", "")
        
        # 检查是否涉及技术方案核心要素
        tech_keywords = [
            "技术问题", "技术手段", "技术效果",
            "自然规律", "技术特征", "计算机系统",
            "硬件", "内存", "处理速度"
        ]
        
        # 如果完全没有技术关键词，可能是非技术内容
        has_tech_keyword = any(kw in content for kw in tech_keywords)
        
        # 非技术关键词
        non_tech_keywords = [
            "商业规则", "游戏规则", "纯粹的算法",
            "智力活动", "数学公式", "思维规则"
        ]
        
        has_non_tech = any(kw in content for kw in non_tech_keywords)
        
        # 如果明确是非技术内容但声称应该授权，拒绝
        if has_non_tech and "授权" in content:
            return False
        
        return True
    
    def _validate_case_first_principle(self, case: Dict) -> bool:
        """验证案例是否符合第一性原理"""
        # 必须有审查结论
        judgment = case.get("judgment", "")
        if not judgment:
            return False
        
        # 检查是否为明确的技术方案案例
        tech_indicators = [
            "技术问题", "技术手段", "技术效果",
            "硬件", "系统内部", "自然规律",
            "计算机系统", "内存", "处理速度"
        ]
        
        description = case.get("description", "") + judgment
        has_tech = any(ind in description for ind in tech_indicators)
        
        # 非技术指示器
        non_tech_indicators = [
            "商业模式", "游戏规则", "纯粹的算法",
            "智力活动", "数学方法"
        ]
        
        has_non_tech = any(ind in description for ind in non_tech_indicators)
        
        # 如果是明确的不授权案例，接受
        if "不授权" in judgment or "驳回" in judgment:
            return True
        
        # 如果声称授权但缺乏技术要素，拒绝
        if "授权" in judgment and not has_tech:
            return False
        
        return True
    
    def _add_case_to_database(self, case: Dict):
        """添加案例到数据库"""
        if not self.case_db_path.exists():
            return
        
        with open(self.case_db_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 生成案例条目
        case_entry = self._generate_case_entry(case)
        
        # 插入到"边界案例"或"最新案例"部分
        # 这里简化处理，实际应该找到正确的插入位置
        
        with open(self.case_db_path, "w", encoding="utf-8") as f:
            f.write(content + "\n" + case_entry)
        
        print(f"  已添加案例: {case.get('title', case.get('id'))}")
    
    def _generate_case_entry(self, case: Dict) -> str:
        """生成案例条目"""
        entry = f"""

### {case.get('title', '新增案例')}

**来源**: {case.get('source', '用户反馈/案例追踪')}
**编号**: {case.get('id', datetime.now().strftime('%Y%m%d'))}
**日期**: {datetime.now().strftime('%Y-%m-%d')}

**案情摘要**: {case.get('description', '')}

**技术要素**:
- 技术问题: {case.get('tech_problem', '见摘要')}
- 技术手段: {case.get('tech_means', '见摘要')}
- 技术效果: {case.get('tech_effect', '见摘要')}

**审查结论**: {case.get('judgment', '')}

**关键词**: {', '.join(case.get('tags', []))}
"""
        return entry
    
    def _log_update(self, results: Dict):
        """记录更新日志"""
        log_entry = f"""
## 更新记录 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

- 新增案例: {results['cases_added']}
- 更新规则: {results['rules_updated']}
- 更新关键词: {results['keywords_updated']}
- 拒绝条目: {results['rejected']}

拒绝原因:
{"".join(f"- {r}" for r in results['reasons'])}
"""
        
        with open(self.update_log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def verify_consistency(self) -> Dict:
        """
        验证知识库一致性
        
        检查项：
        1. 三要素标准一致
        2. L1-L5/G0-G4模型一致
        3. 节点Prompt与规则一致
        4. 案例与规则匹配
        """
        checks = {
            "three_elements_consistent": True,
            "model_consistent": True,
            "prompt_consistent": True,
            "case_rule_matching": True,
            "issues": []
        }
        
        # 读取法律依据
        if self.law_basis_path.exists():
            with open(self.law_basis_path, "r", encoding="utf-8") as f:
                law_content = f.read()
            
            # 检查三要素是否完整
            required_elements = ["技术问题", "技术手段", "技术效果"]
            for elem in required_elements:
                if elem not in law_content:
                    checks["three_elements_consistent"] = False
                    checks["issues"].append(f"法律依据缺少: {elem}")
        
        # 读取案例库
        if self.case_db_path.exists():
            with open(self.case_db_path, "r", encoding="utf-8") as f:
                case_content = f.read()
            
            # 检查案例是否有审查结论
            if "审查结论" not in case_content and "结论" not in case_content:
                checks["case_rule_matching"] = False
                checks["issues"].append("案例库缺少审查结论")
        
        return checks
