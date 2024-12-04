import os
import shutil
from pathlib import Path

def extract_title(filename):
    # 去掉.txt后缀
    filename = filename.replace('.txt', '')
    
    # 处理以paper_开头的情况
    if filename.startswith('paper_'):
        parts = filename.split('_', 2)
        if len(parts) >= 2:
            return parts[1]
    
    # 处理以paper开头但没有下划线的情况
    elif filename.startswith('paper'):
        # 去掉开头的paper，然后在第一个下划线处分割
        title = filename[5:].split('_')[0]
        return title
    
    # 如果不是paper开头，按原来的方式处理
    return filename.split('_')[0]

def create_mapping():
    abstract_base = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd/abstract"
    topics_base = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd_Summary/MinerU_4463_PureMd_Summary"
    mapping_base = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd/mapping"

    os.makedirs(mapping_base, exist_ok=True)

    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        abstract_quarter = os.path.join(abstract_base, quarter)
        topics_quarter = os.path.join(topics_base, quarter)
        mapping_quarter = os.path.join(mapping_base, quarter)

        # 如果源文件夹不存在就跳过
        if not os.path.exists(abstract_quarter) or not os.path.exists(topics_quarter):
            print(f"处理 {quarter}")
            continue

        os.makedirs(mapping_quarter, exist_ok=True)

        # 获取并处理所有文件
        all_files = {
            'abstract': [(f, abstract_quarter) for f in os.listdir(abstract_quarter) if f.endswith('.txt')],
            'topics': [(f, topics_quarter) for f in os.listdir(topics_quarter) if f.endswith('.txt')]
        }

        # 根据title复制文件
        for source_type, files in all_files.items():
            for filename, source_path in files:
                title = extract_title(filename)
                title_dir = os.path.join(mapping_quarter, title)
                os.makedirs(title_dir, exist_ok=True)
                
                src = os.path.join(source_path, filename)
                dst = os.path.join(title_dir, filename)
                try:
                    shutil.copy2(src, dst)
                    print(f"复制文件: {filename} -> {title}")
                except Exception as e:
                    print(f"复制失败 {filename}: {str(e)}")

if __name__ == "__main__":
    create_mapping()
    print("完成！")