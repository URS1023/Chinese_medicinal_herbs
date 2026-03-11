import tensorflow as tf
# 配置使用 CPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
tf.config.set_visible_devices([], 'GPU')

from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetV2B0
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import numpy as np
from PIL import Image
from data_loader import HerbDataLoader
import matplotlib.pyplot as plt
from datetime import datetime
import json

class CustomCallback(tf.keras.callbacks.Callback):
    """自定义回调函数，用于每个epoch结束后保存图表"""
    def __init__(self, save_dir='results'):
        super().__init__()
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.history = {'accuracy': [], 'val_accuracy': [], 'loss': [], 'val_loss': []}
    
    def on_epoch_end(self, epoch, logs=None):
        if logs is None:
            logs = {}
        
        # 更新历史记录
        for key in self.history.keys():
            if key in logs:
                self.history[key].append(float(logs[key]))
        
        # 保存图表和指标
        self.plot_training_history(self.history, epoch + 1)
        self.save_training_metrics(self.history, epoch + 1)
    
    def plot_training_history(self, history, epoch):
        """绘制训练历史图表"""
        try:
            # 创建图表
            plt.figure(figsize=(20, 15))
            
            # 绘制准确率
            plt.subplot(2, 2, 1)
            plt.plot(history['accuracy'], label='训练准确率', color='blue')
            plt.plot(history['val_accuracy'], label='验证准确率', color='red')
            plt.title('模型准确率')
            plt.xlabel('轮次')
            plt.ylabel('准确率')
            plt.legend()
            plt.grid(True)
            
            # 绘制损失
            plt.subplot(2, 2, 2)
            plt.plot(history['loss'], label='训练损失', color='blue')
            plt.plot(history['val_loss'], label='验证损失', color='red')
            plt.title('模型损失')
            plt.xlabel('轮次')
            plt.ylabel('损失')
            plt.legend()
            plt.grid(True)
            
            # 绘制学习率变化
            if 'lr' in history:
                plt.subplot(2, 2, 3)
                plt.plot(history['lr'], label='学习率', color='green')
                plt.title('学习率变化')
                plt.xlabel('轮次')
                plt.ylabel('学习率')
                plt.legend()
                plt.grid(True)
            
            # 绘制准确率分布
            plt.subplot(2, 2, 4)
            plt.hist(history['accuracy'], bins=20, alpha=0.5, label='训练准确率', color='blue')
            plt.hist(history['val_accuracy'], bins=20, alpha=0.5, label='验证准确率', color='red')
            plt.title('准确率分布')
            plt.xlabel('准确率')
            plt.ylabel('频次')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            
            # 保存图表
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.save_dir, f'training_history_epoch_{epoch}_{timestamp}.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"训练历史图表已保存至: {save_path}")
            return True
        except Exception as e:
            print(f"保存训练历史图表时出错: {str(e)}")
            return False
    
    def save_training_metrics(self, history, epoch):
        """保存训练指标"""
        try:
            metrics = {
                'epoch': epoch,
                'accuracy': history['accuracy'][-1] if history['accuracy'] else 0,
                'val_accuracy': history['val_accuracy'][-1] if history['val_accuracy'] else 0,
                'loss': history['loss'][-1] if history['loss'] else 0,
                'val_loss': history['val_loss'][-1] if history['val_loss'] else 0,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.save_dir, f'training_metrics_epoch_{epoch}_{timestamp}.json')
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=4, ensure_ascii=False)
            
            print(f"训练指标已保存至: {save_path}")
            return True
        except Exception as e:
            print(f"保存训练指标时出错: {str(e)}")
            return False

class HerbClassifier:
    def __init__(self, model_path=None, num_classes=26):
        self.num_classes = num_classes
        self.model = self.build_model()
        if model_path and os.path.exists(model_path):
            self.model.load_weights(model_path)
    
    def build_model(self):
        # 使用预训练的EfficientNetV2B0作为基础模型
        base_model = EfficientNetV2B0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        
        # 冻结基础模型
        base_model.trainable = False
        
        # 构建模型
        inputs = layers.Input(shape=(224, 224, 3))
        x = base_model(inputs)
        
        # 添加全局平均池化
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.BatchNormalization()(x)
        
        # 添加深度特征提取层
        x = layers.Dense(1024)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Dropout(0.5)(x)
        
        # 添加注意力机制
        attention = layers.Dense(1024, activation='tanh')(x)
        attention = layers.Dense(1, activation='sigmoid')(attention)
        x = layers.Multiply()([x, attention])
        
        x = layers.Dense(512)(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Dropout(0.3)(x)
        
        # 添加分类层
        predictions = layers.Dense(self.num_classes, activation='softmax')(x)
        
        model = models.Model(inputs=inputs, outputs=predictions)
        
        # 编译模型
        model.compile(
            optimizer=Adam(learning_rate=1e-4),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, data_loader, epochs=50, save_path='model_weights.h5'):
        # 创建回调函数
        callbacks = [
            ModelCheckpoint(
                save_path,
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            ),
            EarlyStopping(
                monitor='val_loss',
                patience=20,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.1,
                patience=8,
                min_lr=1e-8,
                verbose=1
            ),
            CustomCallback(save_dir='results')  # 添加自定义回调函数
        ]
        
        # 获取数据生成器
        train_generator = data_loader.get_train_generator()
        val_generator = data_loader.get_val_generator()
        
        # 训练模型
        print("开始训练模型...")
        history = self.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def evaluate(self, data_loader):
        test_generator = data_loader.get_test_generator()
        return self.model.evaluate(test_generator)
    
    def preprocess_image(self, image_path):
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def predict(self, image_path, class_names):
        img_array = self.preprocess_image(image_path)
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class]
        
        return {
            'class_id': predicted_class,
            'confidence': float(confidence),
            'name': class_names[predicted_class]
        }
    
    def save_model(self, model_path):
        self.model.save_weights(model_path) 