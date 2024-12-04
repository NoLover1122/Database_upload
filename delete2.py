import os

def clean_invalid_json_files(base_path):
    """删除无效的json文件(文件名为.json的)"""
    invalid_count = 0
    
    # 遍历Q1-Q4文件夹
    for q_folder in ['Q1', 'Q2', 'Q3', 'Q4']:
        q_path = os.path.join(base_path, q_folder)
        if not os.path.exists(q_path):
            continue
            
        # 遍历每个Q文件夹下的论文文件夹
        for paper_folder in os.listdir(q_path):
            paper_path = os.path.join(q_path, paper_folder)
            if os.path.isdir(paper_path):
                # 检查文件夹下的json文件
                for filename in os.listdir(paper_path):
                    if filename == '.json':  # 如果文件名只有.json
                        json_path = os.path.join(paper_path, filename)
                        os.remove(json_path)  # 删除文件
                        invalid_count += 1
                        print(f"删除无效文件: {json_path}")
    
    print(f"总共删除了 {invalid_count} 个无效的JSON文件")

# 执行清理
base_path = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd/mapping"
clean_invalid_json_files(base_path)