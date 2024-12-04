from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import os
import json

# 初始化QdrantClient
qdrant = QdrantClient("http://localhost:6333")
encoder = SentenceTransformer("Alibaba-NLP/gte-Qwen2-7B-instruct", device="cuda:0", trust_remote_code=True)

# 读取所有Q1-Q4文件夹中的json文件
base_path = "/mnt/hdd/data/marker_extracted/MinerU_4463_PureMd/mapping"
paper_data = []

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
                if filename.endswith('.json'):
                    file_path = os.path.join(paper_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        paper = json.load(file)
                        paper_data.append(paper)

print(f"已读取 {len(paper_data)} 个论文数据")

if paper_data:
    print("\n第一篇论文的键：", paper_data[0].keys())

# 生成向量和payload
vectors = []
payload = []
for i, paper in enumerate(paper_data):
    try:
        # 使用title和abstract生成向量
        full_text = f"{paper['title']}. {paper['abstract']}"
        vector = encoder.encode(full_text)
        vectors.append(vector)
        
        # payload只包含需要的字段
        payload.append({
            "title": paper['title'],
            "abstract": paper['abstract'],
            "research_significance": paper['topics'].get('项目研究意义', ''),
            "research_status": paper['topics'].get('国内外研究现状及发展动态分析', ''),
            "scientific_significance": paper['topics'].get('科学意义与应用前景', ''),
            "research_content": paper['topics'].get('项目的研究内容', ''),
            "research_objectives": paper['topics'].get('研究目标', ''),
            "key_scientific_issues": paper['topics'].get('拟解决的关键科学问题', ''),
            "research_methods": paper['topics'].get('研究方法', ''),
            "technical_route": paper['topics'].get('技术路线', ''),
            "key_technologies": paper['topics'].get('关键技术', ''),
            "project_features": paper['topics'].get('本项目的特色与创新之处', '')
        })
        
        if (i + 1) % 100 == 0:
            print(f"已处理 {i + 1} 篇论文")
            
    except Exception as e:
        print(f"处理第 {i+1} 篇论文时出错")
        print(f"错误信息：{e}")
        continue

print(f"\n成功处理 {len(vectors)} 篇论文")
print(f"向量维度：{vectors[0].shape if vectors else 'No vectors generated'}")

# 创建collection
qdrant.create_collection(
    collection_name="CS",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE
    )
)

# 上传数据
qdrant.upload_collection(
    collection_name="CS",
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size=256,
)

# 验证上传结果
collection_info = qdrant.get_collection("CS")
print(f"jian_papers集合中的数据数量: {collection_info.points_count}")