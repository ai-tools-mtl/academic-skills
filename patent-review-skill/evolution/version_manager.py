"""
版本管理器 - 专利客体适格性审查技能

管理技能版本，支持回滚和发布。
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class VersionManager:
    """版本管理器"""
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        
        # 版本文件
        self.version_file = self.base_path / "evolution" / "version.json"
        self.versions_dir = self.base_path / "evolution" / "versions"
        self.versions_dir.mkdir(exist_ok=True)
        
        # 初始化版本文件
        if not self.version_file.exists():
            self._init_version_file()
    
    def _init_version_file(self):
        """初始化版本文件"""
        version_data = {
            "current": "v1.0.0",
            "last_updated": datetime.now().isoformat(),
            "history": [
                {
                    "version": "v1.0.0",
                    "date": datetime.now().isoformat(),
                    "changes": "初始版本",
                    "type": "major"
                }
            ]
        }
        
        with open(self.version_file, "w", encoding="utf-8") as f:
            json.dump(version_data, f, ensure_ascii=False, indent=2)
    
    def get_current_version(self) -> str:
        """获取当前版本"""
        with open(self.version_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["current"]
    
    def create_update_version(self, update_results: Dict) -> str:
        """
        创建新版本
        
        版本规则:
        - MAJOR: 核心法律依据重大变更
        - MINOR: 新增案例/规则完善
        - PATCH: 修正错误/优化表述
        """
        current = self.get_current_version()
        major, minor, patch = self._parse_version(current)
        
        # 根据更新内容确定版本类型
        if update_results.get("rules_updated", 0) > 0:
            # 规则更新 -> MINOR
            new_version = f"v{major}.{minor + 1}.{patch}"
        elif update_results.get("cases_added", 0) > 0:
            # 案例更新 -> PATCH
            new_version = f"v{major}.{minor}.{patch + 1}"
        else:
            new_version = f"v{major}.{minor}.{patch + 1}"
        
        # 创建版本快照
        self._create_version_snapshot(new_version, update_results)
        
        # 更新版本文件
        self._update_version_file(new_version, update_results)
        
        return new_version
    
    def _parse_version(self, version: str) -> tuple:
        """解析版本号"""
        v = version.lstrip("v")
        parts = v.split(".")
        return int(parts[0]), int(parts[1]), int(parts[2])
    
    def _create_version_snapshot(self, version: str, update_results: Dict):
        """创建版本快照"""
        snapshot_dir = self.versions_dir / version
        snapshot_dir.mkdir(exist_ok=True)
        
        # 快照关键文件
        files_to_snapshot = [
            "workflow/knowledge/case-database.md",
            "workflow/knowledge/patent-law-basis.md",
            "workflow/keyword-libraries.json",
            "workflow/node-prompts.md"
        ]
        
        for file_path in files_to_snapshot:
            src = self.base_path / file_path
            if src.exists():
                dst = snapshot_dir / file_path.replace("/", "_")
                shutil.copy2(src, dst)
        
        # 保存更新摘要
        summary_file = snapshot_dir / "update_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(update_results, f, ensure_ascii=False, indent=2)
    
    def _update_version_file(self, new_version: str, update_results: Dict):
        """更新版本文件"""
        with open(self.version_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 添加新版本
        data["current"] = new_version
        data["last_updated"] = datetime.now().isoformat()
        data["history"].append({
            "version": new_version,
            "date": datetime.now().isoformat(),
            "changes": self._summarize_changes(update_results),
            "type": self._get_version_type(new_version, data["history"][-1]["version"])
        })
        
        with open(self.version_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _summarize_changes(self, results: Dict) -> str:
        """总结变更"""
        parts = []
        if results.get("cases_added"):
            parts.append(f"新增{results['cases_added']}个案例")
        if results.get("rules_updated"):
            parts.append(f"更新{results['rules_updated']}条规则")
        if results.get("keywords_updated"):
            parts.append(f"更新关键词库")
        return "; ".join(parts) if parts else "小优化"
    
    def _get_version_type(self, new_ver: str, old_ver: str) -> str:
        """获取版本变更类型"""
        n = self._parse_version(new_ver)
        o = self._parse_version(old_ver)
        
        if n[0] > o[0]:
            return "major"
        elif n[1] > o[1]:
            return "minor"
        else:
            return "patch"
    
    def rollback(self, version: str) -> bool:
        """
        回滚到指定版本
        
        Args:
            version: 目标版本号（如v1.0.0）
            
        Returns:
            是否成功
        """
        snapshot_dir = self.versions_dir / version
        if not snapshot_dir.exists():
            print(f"版本 {version} 不存在")
            return False
        
        # 恢复文件
        for snapshot_file in snapshot_dir.glob("*.md"):
            original = self.base_path / "workflow" / "knowledge" / snapshot_file.name
            shutil.copy2(snapshot_file, original)
        
        for snapshot_file in snapshot_dir.glob("*.json"):
            if "update_summary" not in snapshot_file.name:
                original = self.base_path / "workflow" / snapshot_file.name
                shutil.copy2(snapshot_file, original)
        
        print(f"已回滚到版本 {version}")
        return True
    
    def list_versions(self) -> List[Dict]:
        """列出所有版本"""
        with open(self.version_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["history"]
    
    def release(self, version: str = None) -> str:
        """
        发布版本
        
        Args:
            version: 版本号，如果为None则使用当前版本
            
        Returns:
            发布版本号
        """
        if version is None:
            version = self.get_current_version()
        
        print(f"\n{'='*50}")
        print(f"发布版本: {version}")
        print(f"{'='*50}")
        
        # 验证版本
        snapshot_dir = self.versions_dir / version
        if not snapshot_dir.exists():
            print(f"警告: 版本 {version} 快照不存在")
        
        print(f"\n版本特性:")
        for v in self.list_versions():
            if v["version"] == version:
                print(f"  - {v['changes']}")
                break
        
        print(f"\n发布完成!")
        return version


def main():
    parser = argparse.ArgumentParser(description="版本管理器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 当前版本
    subparsers.add_parser("current", help="查看当前版本")
    
    # 列出版本
    subparsers.add_parser("list", help="列出所有版本")
    
    # 发布版本
    release_parser = subparsers.add_parser("release", help="发布版本")
    release_parser.add_argument("--version", help="版本号")
    
    # 回滚
    rollback_parser = subparsers.add_parser("rollback", help="回滚版本")
    rollback_parser.add_argument("--version", required=True, help="目标版本")
    
    args = parser.parse_args()
    
    manager = VersionManager()
    
    if args.command == "current":
        print(f"当前版本: {manager.get_current_version()}")
        
    elif args.command == "list":
        print("\n版本历史:")
        for v in manager.list_versions():
            current_marker = " <=" if v["version"] == manager.get_current_version() else ""
            print(f"  {v['version']} ({v['type']}){current_marker}")
            print(f"    {v['date'][:10]}: {v['changes']}")
    
    elif args.command == "release":
        manager.release(args.version)
    
    elif args.command == "rollback":
        manager.rollback(args.version)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
