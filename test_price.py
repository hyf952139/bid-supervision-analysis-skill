# -*- coding: utf-8 -*-
"""
报价异常分析测试用例
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import BidSupervisionSkill

def test_analyze_price_anomaly():
    skill = BidSupervisionSkill()
    
    # 测试正常情况
    test_prices = [
        {'bidder': '公司A', 'price': 100000},
        {'bidder': '公司B', 'price': 105000},
        {'bidder': '公司C', 'price': 95000},
        {'bidder': '公司D', 'price': 150000},
        {'bidder': '公司E', 'price': 50000}
    ]
    try:
        result = skill.analyze_price_anomaly(test_prices)
        print('✅ 报价分析测试通过：', result)
    except Exception as e:
        print('❌ 报价分析测试失败：', str(e))
    
    # 测试空数据
    try:
        skill.analyze_price_anomaly([])
        print('❌ 空数据测试未通过')
    except ValueError as e:
        print('✅ 空数据测试通过：', str(e))

if __name__ == '__main__':
    test_analyze_price_anomaly()
