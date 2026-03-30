import os
import json
import pandas as pd
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from copaw_skill import BaseSkill

class BidSupervisionSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.name = "招投标监管分析"
        self.description = "自动检测投标文件雷同度、分析报价异常、识别围串标嫌疑"
        self.config = self.load_config()
        self.report_template = self.load_report_template()

    def load_config(self):
        """加载配置文件"""
        with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
            import yaml
            return yaml.safe_load(f)

    def load_report_template(self):
        """加载报告模板"""
        template_path = os.path.join(os.path.dirname(__file__), "templates", "report_template.md")
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def extract_pdf_text(self, pdf_path):
        """提取PDF文件文本内容"""
        try:
            return extract_text(pdf_path)
        except Exception as e:
            self.logger.error(f"提取PDF文本失败: {str(e)}")
            return ""

    def detect_document_similarity(self, pdf_files):
        """检测多份投标文件相似度"""
        texts = []
        for pdf_file in pdf_files:
            text = self.extract_pdf_text(pdf_file)
            texts.append(text)
        
        # 使用TF-IDF和余弦相似度计算
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # 生成相似度报告
        report = []
        for i in range(len(similarity_matrix)):
            for j in range(i+1, len(similarity_matrix)):
                similarity_score = round(similarity_matrix[i][j], 2)
                report.append({
                    "文件1": os.path.basename(pdf_files[i]),
                    "文件2": os.path.basename(pdf_files[j]),
                    "相似度得分": similarity_score,
                    "风险等级": "高" if similarity_score > 0.8 else "中" if similarity_score > 0.6 else "低"
                })
        return report

    def analyze_abnormal_pricing(self, pricing_data):
        """分析报价异常"""
        df = pd.DataFrame(pricing_data)
        df["报价"] = pd.to_numeric(df["报价"], errors="coerce")
        
        # 计算均值和标准差
        mean_price = df["报价"].mean()
        std_price = df["报价"].std()
        
        # 识别偏离均值2倍标准差的异常值
        df["偏离度"] = abs(df["报价"] - mean_price) / std_price
        abnormal_items = df[df["偏离度"] > 2].to_dict("records")
        
        return {
            "均值报价": round(mean_price, 2),
            "标准差": round(std_price, 2),
            "异常报价数量": len(abnormal_items),
            "异常详情": abnormal_items
        }

    def detect_collusion_risk(self, bidder_info):
        """识别围串标风险"""
        risk_factors = []
        df = pd.DataFrame(bidder_info)
        
        # 检查IP/MAC地址重复
        ip_counts = df["IP地址"].value_counts()
        for ip, count in ip_counts.items():
            if count > 1:
                risk_factors.append(f"发现{count}家投标人使用同一IP地址：{ip}")
        
        # 检查报价规律
        if len(set(df["报价"])) < len(df)*0.8:
            risk_factors.append("投标人报价高度趋同，存在围标嫌疑")
        
        # 检查资质关联
        company_counts = df["关联公司"].value_counts()
        for company, count in company_counts.items():
            if count > 1 and company != "无":
                risk_factors.append(f"发现{count}家投标人关联同一公司：{company}")
        
        return risk_factors

    def calculate_risk_score(self, similarity_result, pricing_result, collusion_result):
        """计算综合风险评分"""
        score = 100
        
        # 相似度扣分
        high_similarity = sum(1 for item in similarity_result if item["风险等级"] == "高")
        score -= high_similarity * 20
        
        # 异常报价扣分
        score -= pricing_result["异常报价数量"] * 10
        
        # 围串标风险扣分
        score -= len(collusion_result) * 30
        
        return max(0, min(100, score))

    def generate_report(self, similarity_result, pricing_result, collusion_result, risk_score):
        """生成最终分析报告"""
        return self.report_template.format(
            risk_score=risk_score,
            similarity_count=len(similarity_result),
            similarity_details=json.dumps(similarity_result, indent=2, ensure_ascii=False),
            abnormal_count=pricing_result["异常报价数量"],
            abnormal_details=json.dumps(pricing_result["异常详情"], indent=2, ensure_ascii=False),
            collusion_count=len(collusion_result),
            collusion_details="\n- ".join(collusion_result),
            suggestions=self.generate_suggestions(risk_score, collusion_result)
        )

    def generate_suggestions(self, risk_score, collusion_result):
        """生成合规建议"""
        suggestions = []
        if risk_score < 60:
            suggestions.append("建议立即启动人工复核程序，重点核查高风险项目")
        if len(collusion_result) > 0:
            suggestions.append("建议对存在关联关系的投标人进行资质复查")
        suggestions.append("建议建立投标文件电子指纹库，提高围串标检测效率")
        suggestions.append("建议优化报价评分机制，减少异常报价影响")
        return "\n- ".join(suggestions)

    def execute(self, user_input, context=None):
        """技能执行入口"""
        try:
            # 解析用户输入
            input_data = self.parse_user_input(user_input)
            
            # 执行分析流程
            similarity_result = self.detect_document_similarity(input_data["pdf_files"])
            pricing_result = self.analyze_abnormal_pricing(input_data["pricing_data"])
            collusion_result = self.detect_collusion_risk(input_data["bidder_info"])
            risk_score = self.calculate_risk_score(similarity_result, pricing_result, collusion_result)
            
            # 生成报告
            report = self.generate_report(similarity_result, pricing_result, collusion_result, risk_score)
            
            return report
        except Exception as e:
            self.logger.error(f"技能执行失败: {str(e)}")
            return f"分析失败，请检查输入数据格式是否正确。错误信息：{str(e)}"

    def parse_user_input(self, user_input):
        """解析用户输入数据"""
        # 实际应用中可根据CoPaw消息格式解析输入
        # 这里简化处理，假设用户输入包含所有必要数据路径
        return {
            "pdf_files": user_input.get("pdf_files", []),
            "pricing_data": user_input.get("pricing_data", []),
            "bidder_info": user_input.get("bidder_info", [])
        }

# 技能注册接口
def register_skill():
    return BidSupervisionSkill()
