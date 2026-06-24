"""
工作流测试用例
"""

import pytest
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestWorkflowConfig:
    """工作流配置测试"""

    def test_workflow_json_valid(self):
        """测试工作流JSON文件是否有效"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "patent-review-workflow.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        assert "workflow" in config
        assert config["workflow"]["id"] == "patent-eligibility-review"
        assert len(config["workflow"]["stages"]) == 4

    def test_workflow_stages_count(self):
        """测试工作流阶段数量"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "patent-review-workflow.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        stages = config["workflow"]["stages"]
        assert len(stages) == 4
        
        # 验证每个阶段的节点数量
        expected_node_counts = [6, 6, 5, 4]
        for i, stage in enumerate(stages):
            assert len(stage["nodes"]) == expected_node_counts[i]

    def test_human_review_nodes(self):
        """测试人工审查节点配置"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "patent-review-workflow.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 统计人工审查节点
        human_nodes = []
        for stage in config["workflow"]["stages"]:
            for node in stage["nodes"]:
                if node["type"] == "human_review":
                    human_nodes.append(node)
        
        assert len(human_nodes) == 4  # 四个阶段各一个人工节点


class TestNodePrompts:
    """节点Prompt测试"""

    def test_node_prompts_exists(self):
        """测试节点Prompt文件是否存在"""
        prompts_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "node-prompts.md"
        )
        
        assert os.path.exists(prompts_path)
        
        with open(prompts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证包含所有节点
        assert "## 1.1 特征提取与标注" in content
        assert "## 2.1 技术问题穿透-删除测试" in content
        assert "## 3.1 数据含义量化" in content
        assert "## 4.1 类案匹配" in content


class TestKnowledgeBase:
    """知识库测试"""

    def test_patent_law_basis_exists(self):
        """测试法律依据文件是否存在"""
        basis_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "knowledge",
            "patent-law-basis.md"
        )
        
        assert os.path.exists(basis_path)

    def test_case_database_exists(self):
        """测试案例库文件是否存在"""
        case_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "knowledge",
            "case-database.md"
        )
        
        assert os.path.exists(case_path)
        
        with open(case_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证包含案例类型
        assert "授权案例" in content or "授权" in content
        assert "不授权" in content


class TestKeywordLibraries:
    """关键词库测试"""

    def test_keyword_libraries_valid(self):
        """测试关键词库是否有效"""
        lib_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "keyword-libraries.json"
        )
        
        with open(lib_path, 'r', encoding='utf-8') as f:
            libraries = json.load(f)
        
        assert "algorithm_keywords" in libraries
        assert "business_keywords" in libraries
        assert "tech_effect_keywords" in libraries
        assert "algo_effect_keywords" in libraries


class TestWorkflowLogic:
    """工作流逻辑测试"""

    def test_stage_exit_conditions(self):
        """测试阶段退出条件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "patent-review-workflow.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证每个阶段都有退出条件
        for stage in config["workflow"]["stages"]:
            if "exit_conditions" in stage:
                assert len(stage["exit_conditions"]) > 0

    def test_node_connections(self):
        """测试节点连接关系"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "patent-review-workflow.json"
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证节点都有后续连接
        for stage in config["workflow"]["stages"]:
            for node in stage["nodes"]:
                if node["type"] == "ai_process":
                    assert "next_nodes" in node
                    assert len(node["next_nodes"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
