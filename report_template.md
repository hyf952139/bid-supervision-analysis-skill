# 招投标监管分析报告

**生成时间**：{{ now }}
**风险评分**：{{ risk_score }}/100

## 一、投标文件相似度分析
{% if similarity_results %}
{% for result in similarity_results %}
### {{ result.file1 }} vs {{ result.file2 }}
- **相似度**：{{ result.similarity }}
- **风险等级**：{{ result.risk_level }}
- **建议**：{{ result.suggestion }}
{% endfor %}
{% else %}
暂无相似度分析数据
{% endif %}

## 二、报价异常分析
{% if price_results %}
{% for result in price_results %}
### {{ result.bidder }}
- **报价**：{{ result.price }}元
- **价格偏差**：{{ result.deviation }}
- **是否异常**：{{ result.is_anomaly }}
- **建议**：{{ result.suggestion }}
{% endfor %}
{% else %}
暂无报价分析数据
{% endif %}

## 三、围串标风险识别
{% if collusion_results %}
{% for result in collusion_results %}
### {{ result.risk_type }}
- **风险等级**：{{ result.risk_level }}
- **详细信息**：{{ result }}
- **建议**：{{ result.suggestion }}
{% endfor %}
{% else %}
暂无围串标风险识别数据
{% endif %}

## 四、综合建议
{% if suggestions %}
{% for suggestion in suggestions %}
- {{ suggestion }}
{% endfor %}
{% else %}
- 未发现明显风险，建议正常推进招投标流程
{% endif %}
