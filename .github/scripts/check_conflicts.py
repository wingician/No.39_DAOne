#!/usr/bin/env python3
"""
翼术师世界设定冲突检查器
使用 AI 检查新提交的内容是否与现有世界观设定冲突
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

try:
    import openai
except ImportError:
    openai = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


class WorldSettingChecker:
    """世界设定冲突检查器"""
    
    def __init__(self, api_key: str = None, provider: str = "openai"):
        self.provider = provider
        if provider == "openai" and openai:
            self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic" and Anthropic:
            self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        else:
            self.client = None
    
    def load_world_knowledge(self) -> str:
        """加载现有世界设定知识库"""
        knowledge = []
        
        # 核心世界观文档
        core_docs = [
            "故事背景/大纲——世界的构成的设想.md",
            "故事背景/背景和寓意/（工事）世界观.md",
            "故事背景/时间线(历史)/时间主干线.md",
            "故事背景/魔法/魔法的本质.md",
            "故事背景/天文地理和历史/稻一大陆.md",
        ]
        
        for doc in core_docs:
            doc_path = Path(doc)
            if doc_path.exists():
                content = doc_path.read_text(encoding='utf-8')
                knowledge.append(f"=== {doc} ===\n{content}\n")
        
        return "\n\n".join(knowledge)
    
    def read_changed_files(self, file_list: List[str]) -> Dict[str, str]:
        """读取变更的文件内容"""
        changes = {}
        for file_path in file_list:
            path = Path(file_path)
            if path.exists() and path.suffix == '.md':
                changes[file_path] = path.read_text(encoding='utf-8')
        return changes
    
    def check_conflicts_with_ai(self, world_knowledge: str, new_content: Dict[str, str]) -> Dict[str, Any]:
        """使用AI检查冲突"""
        
        prompt = f"""你是翼术师世界的设定审查助手。请仔细审查新提交的内容是否与现有世界观设定存在冲突。

## 现有世界观设定

{world_knowledge}

## 新提交的内容

"""
        for file_path, content in new_content.items():
            prompt += f"\n### 文件: {file_path}\n\n{content}\n\n"
        
        prompt += """

## 检查要点

请检查以下方面的潜在冲突：

1. **时间线冲突**
   - 事件发生时间是否符合历史纪元设定
   - 角色出现时间是否合理（已死亡/未出生）
   - 时代背景是否一致

2. **地理冲突**
   - 地点是否存在于已知的九神州大陆
   - 地理位置描述是否与已有设定矛盾

3. **魔法体系冲突**
   - 魔法理论是否符合四大魔法本质理论
   - 魔法能力是否合理
   - 是否引入了不符合世界观的科技元素

4. **人物冲突**
   - 角色等级体系是否正确（学徒、耶师、亲师、翼术师）
   - 人物关系是否合理
   - 能力设定是否过于夸张

5. **文化冲突**
   - 社会习俗是否符合世界设定
   - 节日、传统是否与已有文化矛盾

6. **世界观核心**
   - 是否保持"外表西方、内核东方"的设定原则
   - 是否体现阴阳镜像世界的概念
   - 是否符合"文化和文字隐喻"的主题

## 输出格式

请以JSON格式返回检查结果：

```json
{
  "has_conflicts": true/false,
  "conflicts": [
    {
      "type": "冲突类型",
      "file": "文件路径",
      "description": "冲突描述",
      "suggestion": "修改建议"
    }
  ],
  "warnings": [
    "警告或建议1",
    "警告或建议2"
  ],
  "summary": "总体评价"
}
```

如果没有发现明显冲突，conflicts 数组应为空，但可以在 warnings 中提供改进建议。
"""
        
        try:
            if self.provider == "openai" and self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "你是一个专业的世界观设定审查助手，精通中国传统文化和奇幻世界构建。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result_text = response.choices[0].message.content
                
            elif self.provider == "anthropic" and self.client:
                response = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                result_text = response.content[0].text
            else:
                return {
                    "has_conflicts": False,
                    "conflicts": [],
                    "warnings": ["AI检查服务未配置，请手动审核"],
                    "summary": "自动检查不可用"
                }
            
            # 解析JSON结果
            # 尝试从markdown代码块中提取JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(result_text)
            
        except Exception as e:
            print(f"AI检查出错: {e}", file=sys.stderr)
            return {
                "has_conflicts": False,
                "conflicts": [],
                "warnings": [f"AI检查出错: {str(e)}，请手动审核"],
                "summary": "检查失败"
            }
    
    def check(self, changed_files: List[str]) -> Dict[str, Any]:
        """执行完整的冲突检查"""
        print("正在加载世界设定知识库...")
        world_knowledge = self.load_world_knowledge()
        
        print(f"正在读取 {len(changed_files)} 个变更文件...")
        new_content = self.read_changed_files(changed_files)
        
        if not new_content:
            return {
                "has_conflicts": False,
                "conflicts": [],
                "warnings": ["没有找到需要检查的Markdown文件"],
                "summary": "无内容需要检查"
            }
        
        print("正在使用AI检查冲突...")
        result = self.check_conflicts_with_ai(world_knowledge, new_content)
        
        return result


def main():
    parser = argparse.ArgumentParser(description='翼术师世界设定冲突检查')
    parser.add_argument('--changed-files', required=True, help='变更的文件列表（空格分隔）')
    parser.add_argument('--pr-number', help='Pull Request 编号')
    parser.add_argument('--output', default='check_result.json', help='输出文件路径')
    parser.add_argument('--provider', default='openai', choices=['openai', 'anthropic'], help='AI提供商')
    
    args = parser.parse_args()
    
    # 解析文件列表
    changed_files = args.changed_files.split()
    
    print(f"开始检查 PR #{args.pr_number or 'N/A'}")
    print(f"变更文件: {len(changed_files)} 个")
    
    # 创建检查器
    checker = WorldSettingChecker(provider=args.provider)
    
    # 执行检查
    result = checker.check(changed_files)
    
    # 保存结果
    output_path = Path(args.output)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n检查完成! 结果已保存到 {args.output}")
    print(f"发现冲突: {result.get('has_conflicts', False)}")
    print(f"冲突数量: {len(result.get('conflicts', []))}")
    print(f"警告数量: {len(result.get('warnings', []))}")
    
    # 如果有冲突，返回非零退出码（但不阻止PR）
    if result.get('has_conflicts'):
        print("\n⚠️  发现潜在冲突，请查看详细报告")
        # 不返回错误码，让PR可以继续
        # sys.exit(1)
    else:
        print("\n✅ 未发现明显冲突")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
