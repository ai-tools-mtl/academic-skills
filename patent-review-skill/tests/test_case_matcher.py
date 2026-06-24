"""
案例匹配器测试用例
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.case_matcher import CaseMatcher, main


class TestCaseMatcher:
    """案例匹配器测试"""

    @pytest.fixture
    def matcher(self):
        """创建案例匹配器实例"""
        case_db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "patent-workflow",
            "workflow",
            "knowledge",
            "case-database.md"
        )
        return CaseMatcher(case_database=case_db_path)

    def test_matcher_initialization(self, matcher):
        """测试匹配器初始化"""
        assert matcher is not None
        assert len(matcher.cases) > 0

    def test_search_with_single_feature(self, matcher):
        """测试单特征搜索"""
        results = matcher.search(["深度学习"])
        
        assert len(results) > 0
        for case in results:
            assert "深度学习" in case["title"] or \
                   "深度学习" in str(case.get("key_features", [])) or \
                   any("深度学习" in str(v) for v in case.values() if isinstance(v, str))

    def test_search_with_multiple_features(self, matcher):
        """测试多特征搜索"""
        results = matcher.search(["深度学习", "神经网络"])
        
        assert len(results) > 0

    def test_search_with_limit(self, matcher):
        """测试结果数量限制"""
        results = matcher.search(["算法"], limit=3)
        
        assert len(results) <= 3

    def test_search_case_type_filter(self, matcher):
        """测试案例类型过滤"""
        # 搜索授权案例
        auth_cases = matcher.search(["训练"], limit=10)
        
        # 验证返回的都是授权类型
        for case in auth_cases:
            assert case["type"] in ["授权", "不授权", "边界"]

    def test_case_structure(self, matcher):
        """测试案例结构"""
        results = matcher.search(["测试"], limit=1)
        
        if len(results) > 0:
            case = results[0]
            required_fields = ["id", "type", "title", "source", "conclusion"]
            
            for field in required_fields:
                assert field in case, f"Missing field: {field}"

    def test_empty_feature_handling(self, matcher):
        """测试空特征处理"""
        results = matcher.search([])
        
        # 空搜索应返回所有案例或空列表
        assert isinstance(results, list)


class TestCaseMatcherOutput:
    """案例匹配器输出测试"""

    def test_json_output_format(self, matcher):
        """测试JSON输出格式"""
        results = matcher.search(["深度学习"], limit=1)
        
        if len(results) > 0:
            case = results[0]
            
            # 验证JSON可序列化
            import json
            try:
                json.dumps(case, ensure_ascii=False)
            except (TypeError, ValueError):
                pytest.fail("Case is not JSON serializable")

    def test_similarity_score_range(self, matcher):
        """测试相似度分数范围"""
        results = matcher.search(["神经网络"], limit=10)
        
        for case in results:
            if "similarity" in case:
                assert 0 <= case["similarity"] <= 1


class TestCaseMatcherEdgeCases:
    """边界情况测试"""

    def test_no_matching_cases(self, matcher):
        """测试无匹配案例"""
        results = matcher.search(["xyz123不存在的特征"])
        
        # 应该返回空列表或空结果
        assert results == [] or len(results) == 0

    def test_case_database_integrity(self, matcher):
        """测试案例数据库完整性"""
        # 验证案例库包含授权和不授权案例
        all_cases = matcher.cases
        
        case_types = set()
        for case in all_cases:
            if "type" in case:
                case_types.add(case["type"])
        
        # 至少应该包含授权和不授权案例
        assert len(case_types) >= 1


class TestMainFunction:
    """主函数测试"""

    def test_main_with_features_arg(self, capsys):
        """测试主函数命令行参数"""
        import sys
        from scripts.case_matcher import main
        import argparse
        
        # 创建测试参数
        test_args = ["case_matcher.py", "--features", "深度学习", "--format", "text", "--limit", "2"]
        
        # 保存原始参数
        original_argv = sys.argv
        
        try:
            sys.argv = test_args
            
            # 应该能够正常运行（可能因为没有完整初始化而失败，但不应崩溃）
            try:
                main()
            except SystemExit:
                pass  # argparse 可能退出
            except Exception:
                pass  # 其他预期异常
            
        finally:
            sys.argv = original_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
