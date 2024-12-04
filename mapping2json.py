import os
import json

def extract_title_from_abstract_file(folder_path):
    """从abstract文件名中提取论文标题"""
    for filename in os.listdir(folder_path):
        if '_abstract.txt' in filename:
            return filename.replace('_abstract.txt', '')
    return None

def create_paper_json(folder_path):
    """为单个论文文件夹创建JSON文件"""
    paper_data = {
        'title': '',
        'abstract': '',
        'topics': {}
    }
    
    # 获取论文标题
    title = extract_title_from_abstract_file(folder_path)
    if title:
        paper_data['title'] = title
    
    # 映射中文部分到topics的键
    topic_mapping = {
        '关键技术': 'key_technologies',
        '国内外研究现状及发展动态分析': 'research_status',
        '技术路线': 'technical_route',
        '拟解决的关键科学问题': 'key_scientific_issues',
        '本项目的特色与创新之处': 'project_features',
        '研究方法': 'research_methods',
        '研究目标': 'research_objectives',
        '科学意义与应用前景': 'scientific_significance',
        '项目的研究内容': 'research_content',
        '项目研究意义': 'research_significance'
    }
    
    # 初始化所有topics为空字符串
    for topic_zh in topic_mapping.keys():
        paper_data['topics'][topic_zh] = ''
    
    # 读取文件夹中的所有txt文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 处理abstract
            if '_abstract.txt' in filename:
                paper_data['abstract'] = content
                continue
            
            # 处理topics部分
            for topic_zh in topic_mapping.keys():
                if topic_zh in filename:
                    paper_data['topics'][topic_zh] = content
                    break
    
    return paper_data

def process_all_papers(base_path):
    """处理所有论文文件夹"""
    # 遍历Q1-Q4文件夹
    for q_folder in ['Q1', 'Q2', 'Q3', 'Q4']:
        q_path = os.path.join(base_path, q_folder)
        if not os.path.exists(q_path):
            continue
            
        # 遍历每个Q文件夹下的论文文件夹
        for paper_folder in os.listdir(q_path):
            paper_path = os.path.join(q_path, paper_folder)
            if os.path.isdir(paper_path):
                # 创建JSON数据
                paper_json = create_paper_json(paper_path)
                
                # 保存JSON文件
                json_filename = f"{paper_json['title']}.json"
                json_path = os.path.join(paper_path, json_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(paper_json, f, ensure_ascii=False, indent=4)
                
                print(f"成功创建JSON文件: {json_filename}")

# 执行转换
base_path = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd/mapping"
process_all_papers(base_path)