# 招投标监管分析技能（2024增强版）
## 技能基本信息
- **技能ID**：bid-supervision-analysis-v2024
- **技能名称**：招投标监管分析技能（2024增强版）
- **技能版本**：2.0.0
- **技能作者**：魔搭创空间用户
- **技能描述**：专业的招投标监管分析助手，支持投标文件相似度检测、报价异常分析、围串标风险识别和监管报告生成（2024增强版）
- **技能标签**：招投标,监管,分析,报告,AI Agent,2024增强版
- **适用平台**：CoPaw个人智能体工作台
- **依赖模型**：通义千问-Qwen-Plus, 通义千问-Qwen-Lite
- **运行环境**：Python 3.10+
- **依赖包**：见requirements.txt

## 技能功能说明
### 核心功能
1. **投标文件相似度检测**：自动比对多份标书的文本雷同度，识别抄袭嫌疑
2. **报价异常分析**：分析投标报价的合理性，发现异常低价/高价
3. **围串标风险识别**：检测投标人IP地址、报价规律等围串标迹象
4. **监管报告生成**：输出符合监管要求的专业分析报告
5. **AI智能审核**：基于大模型的智能审核功能，提供专业的合规建议

## 输入输出示例
### 示例1：投标文件相似度检测
**输入**：
```json
{
  "action": "analyze_similarity",
  "parameters": {
    "file_paths": [
      "bid1.pdf",
      "bid2.pdf"
    ]
  }
}
{
  "status": "success",
  "output": [
    {
      "file1": "bid1.pdf",
      "file2": "bid2.pdf",
      "similarity": 0.85,
      "risk_level": "高风险",
      "suggestion": "建议进一步核查"
    }
  ],
  "message": ""
}
{
  "action": "analyze_price",
  "parameters": {
    "price_data": [
      {"bidder": "公司A", "price": 100000},
      {"bidder": "公司B", "price": 105000},
      {"bidder": "公司C", "price": 95000},
      {"bidder": "公司D", "price": 150000},
      {"bidder": "公司E", "price": 50000}
    ]
  }
}
{
  "status": "success",
  "output": [
    {"bidder": "公司A", "price": 100000, "deviation": 0.0, "is_anomaly": false, "suggestion": "正常"},
    {"bidder": "公司B", "price": 105000, "deviation": 0.05, "is_anomaly": false, "suggestion": "正常"},
    {"bidder": "公司C", "price": 95000, "deviation": 0.05, "is_anomaly": false, "suggestion": "正常"},
    {"bidder": "公司D", "price": 150000, "deviation": 0.5, "is_anomaly": true, "suggestion": "建议核查报价合理性"},
    {"bidder": "公司E", "price": 50000, "deviation": 0.5, "is_anomaly": true, "suggestion": "建议核查报价合理性"}
  ],
  "message": ""
}
