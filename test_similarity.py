# -*- coding: utf-8 -*-
"""
投标文件相似度检测测试用例
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import BidSupervisionSkill

def test_analyze_bid_similarity():
    skill = BidSupervisionSkill()
    
    # 测试正常情况
    test_files = ['examples/sample_bid_docs/bid1.pdf', 'examples/sample_bid_docs/bid2.pdf']
    try:
        result = skill.analyze_bid_similarity(test_files)
        print('✅ 相似度分析测试通过：', result)
    except Exception as e:
        print('❌ 相似度分析测试失败：', str(e))
    
    # 测试文件不存在
    try:
        skill.analyze_bid_similarity(['examples/sample_bid_docs/nonexistent.pdf'])
        print('❌ 文件不存在测试未通过')
    except ValueError as e:
        print('✅ 文件不存在测试通过：', str(e))
    
    # 测试不支持的文件类型
    try:
        skill.analyze_bid_similarity(['examples/sample_bid_docs/test.txt'])
        print('❌ 不支持的文件类型测试未通过')
    except ValueError as e:
        print('✅ 不支持的文件类型测试通过：', str(e))

if __name__ == '__main__':
    test_analyze_bid_similarity()
