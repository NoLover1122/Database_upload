import os
import re
from pathlib import Path

def extract_abstract(file_path):
    """提取MD文件中Abstract和第一个#之间的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找Abstract和第一个#之间的内容
        pattern = r'Abstract\s*(.*?)(?=#|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {str(e)}")
        return ""

def process_md_files():
    # 基础路径
    base_path = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd"
    output_base = os.path.join(base_path, "abstract")
    
    # 确保输出基础目录存在
    os.makedirs(output_base, exist_ok=True)
    
    # 处理Q1-Q4文件夹
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        input_quarter_path = os.path.join(base_path, quarter)
        output_quarter_path = os.path.join(output_base, quarter)
        
        # 如果源文件夹不存在，跳过
        if not os.path.exists(input_quarter_path):
            print(f"文件夹 {input_quarter_path} 不存在，跳过")
            continue
        
        # 创建对应的输出文件夹
        os.makedirs(output_quarter_path, exist_ok=True)
        
        # 处理所有md文件
        for root, _, files in os.walk(input_quarter_path):
            # 获取相对路径
            rel_path = os.path.relpath(root, input_quarter_path)
            output_dir = os.path.join(output_quarter_path, rel_path)
            os.makedirs(output_dir, exist_ok=True)
            
            for file in files:
                if file.endswith('.md'):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(
                        output_dir, 
                        file.replace('.md', '_abstract.txt')
                    )
                    
                    # 提取摘要
                    abstract = extract_abstract(input_file)
                    
                    # 保存摘要
                    if abstract:
                        try:
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(abstract)
                            print(f"已处理: {input_file} -> {output_file}")
                        except Exception as e:
                            print(f"保存文件 {output_file} 时发生错误: {str(e)}")
                    else:
                        print(f"警告: 未在 {input_file} 中找到摘要")

def main():
    print("开始处理MD文件...")
    process_md_files()
    print("处理完成！")

if __name__ == "__main__":
    main()