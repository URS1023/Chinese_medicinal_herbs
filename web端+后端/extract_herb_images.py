import os
import shutil
from app import app, db
from models import Herb

def extract_herb_images():
    dataset_path = os.path.join('dataset', 'train')  # 从训练集中提取图片
    target_path = 'static/uploads/herbs'  # 目标路径
    
    # 确保目标目录存在
    os.makedirs(target_path, exist_ok=True)
    
    with app.app_context():
        herbs = Herb.query.all()
        for herb in herbs:
            try:
                # 在数据集中查找对应的药材文件夹
                herb_folder = os.path.join(dataset_path, herb.name)
                if os.path.exists(herb_folder):
                    # 获取文件夹中的第一张图片
                    images = [f for f in os.listdir(herb_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    if images:
                        # 选择第一张图片
                        source_image = os.path.join(herb_folder, images[0])
                        # 构建目标路径
                        target_image = os.path.join(target_path, f"{herb.name}_{images[0]}")
                        # 复制图片
                        shutil.copy2(source_image, target_image)
                        # 更新数据库中的图片路径
                        herb.image_path = os.path.join('uploads/herbs', f"{herb.name}_{images[0]}")
                        print(f"已提取图片: {herb.name}")
                    else:
                        print(f"未找到图片: {herb.name}")
                else:
                    print(f"未找到文件夹: {herb.name}")
            except Exception as e:
                print(f"处理 {herb.name} 时出错: {str(e)}")
        
        # 保存更改
        db.session.commit()
        print("图片提取完成！")

if __name__ == '__main__':
    extract_herb_images() 