import os
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import shutil

class HerbDataLoader:
    def __init__(self, data_dir, img_size=(224, 224), batch_size=32):
        self.data_dir = data_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.class_names = sorted(os.listdir(os.path.join(data_dir, 'train')))
        self.num_classes = len(self.class_names)
        
        # 创建数据增强器
        self.train_datagen = ImageDataGenerator(
            preprocessing_function=tf.keras.applications.efficientnet_v2.preprocess_input,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # 验证和测试集只需要预处理，不需要增强
        self.val_datagen = ImageDataGenerator(
            preprocessing_function=tf.keras.applications.efficientnet_v2.preprocess_input
        )
        self.test_datagen = ImageDataGenerator(
            preprocessing_function=tf.keras.applications.efficientnet_v2.preprocess_input
        )
        
        # 确保静态文件目录存在
        self.static_dir = 'static'
        self.examples_dir = os.path.join(self.static_dir, 'examples')
        os.makedirs(self.examples_dir, exist_ok=True)
        
        # 复制示例图片
        self.copy_example_images()
    
    def copy_example_images(self):
        """为每个类别复制一个示例图片到static/examples目录"""
        print("开始复制示例图片...")
        train_dir = os.path.join(self.data_dir, 'train')
        
        for class_name in self.class_names:
            class_dir = os.path.join(train_dir, class_name)
            if os.path.exists(class_dir):
                # 获取该类别的所有图片
                images = [f for f in os.listdir(class_dir) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                if images:
                    # 源文件路径
                    src_path = os.path.join(class_dir, images[0])
                    # 目标文件路径（使用类名作为文件名）
                    dst_filename = f"{class_name}.jpg"
                    dst_path = os.path.join(self.examples_dir, dst_filename)
                    
                    try:
                        # 打开、转换和保存图片
                        img = Image.open(src_path)
                        img = img.convert('RGB')
                        img = img.resize(self.img_size, Image.LANCZOS)
                        img.save(dst_path, 'JPEG', quality=95)
                        print(f"成功复制图片: {class_name}")
                    except Exception as e:
                        print(f"处理图片时出错 {class_name}: {str(e)}")
    
    def get_example_images(self):
        """获取所有类别的示例图片信息"""
        examples = []
        for class_name in self.class_names:
            image_path = f"examples/{class_name}.jpg"
            if os.path.exists(os.path.join(self.static_dir, image_path)):
                examples.append({
                    'name': class_name,
                    'image_path': image_path
                })
            else:
                print(f"警告: 找不到图片 {image_path}")
        return examples
    
    def get_train_generator(self):
        return self.train_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'train'),
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=True
        )
    
    def get_val_generator(self):
        return self.val_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'val'),
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False
        )
    
    def get_test_generator(self):
        return self.test_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'test'),
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False
        )
    
    def get_class_names(self):
        return self.class_names
    
    def get_num_classes(self):
        return self.num_classes 