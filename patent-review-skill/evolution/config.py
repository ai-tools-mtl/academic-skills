"""
自我进化配置
"""

# 进化频率配置
EVOLUTION_CONFIG = {
    # 自动进化触发条件
    "auto_evolution": {
        "enabled": True,
        "min_feedback_count": 5,      # 最少反馈数触发
        "check_interval_hours": 168,   # 每周检查一次（7*24）
    },
    
    # 案例追踪配置
    "case_tracking": {
        "enabled": True,
        "check_interval_days": 7,      # 每周检查一次
        "sources": [
            "cnipa_cases",            # 国家知识产权局
            "court_cases",            # 最高人民法院
            "review_guide"            # 审查指南
        ],
        "retention_days": 365          # 案例保留一年
    },
    
    # 第一性原理约束
    "first_principle": {
        "core_definition": "专利法第二条第二款：技术方案是对要解决的技术问题所采取的技术手段构成了技术特征，并且能够产生相应的技术效果。",
        "three_elements": {
            "tech_problem": "利用自然规律解决技术问题",
            "tech_means": "与技术特征功能上相互支持",
            "tech_effect": "获得符合自然规律的技术效果"
        },
        # 合规检查关键词
        "required_keywords": ["技术问题", "技术手段", "技术效果", "自然规律"],
        # 排除关键词
        "excluded_keywords": ["商业模式", "游戏规则", "纯粹的算法", "智力活动"]
    },
    
    # 验证配置
    "validation": {
        "run_tests_on_update": True,
        "require_first_principle_check": True,
        "min_test_coverage": 0.8
    },
    
    # 版本管理
    "version": {
        "format": "v{MAJOR}.{MINOR}.{PATCH}",
        "auto_increment": True,
        "changelog_required": True
    },
    
    # 反馈优先级
    "feedback_priority": {
        "P0": ["rule_correction", "error_correction"],  # 立即处理
        "P1": ["case_addition"],                         # 高优先级
        "P2": ["boundary_clarification"],                # 中优先级
        "P3": ["experience_improvement"]                  # 低优先级
    }
}


def get_config(key: str = None):
    """获取配置"""
    if key is None:
        return EVOLUTION_CONFIG
    return EVOLUTION_CONFIG.get(key)


def is_auto_evolution_enabled() -> bool:
    """是否启用自动进化"""
    return EVOLUTION_CONFIG.get("auto_evolution", {}).get("enabled", False)


def should_trigger_evolution(pending_count: int) -> bool:
    """是否应该触发进化"""
    config = EVOLUTION_CONFIG.get("auto_evolution", {})
    return pending_count >= config.get("min_feedback_count", 5)
