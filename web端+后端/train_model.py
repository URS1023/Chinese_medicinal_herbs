import os
import tensorflow as tf
from model import HerbClassifier
from data_loader import HerbDataLoader
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime
import matplotlib
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 使用 DejaVu Sans 字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def plot_confusion_matrix(y_true, y_pred, class_names, save_dir='results'):
    """绘制混淆矩阵"""
    try:
        # 计算混淆矩阵
        cm = confusion_matrix(y_true, y_pred)
        
        # 创建图表
        plt.figure(figsize=(15, 15))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names,
                   yticklabels=class_names)
        plt.title('混淆矩阵')
        plt.xlabel('预测类别')
        plt.ylabel('真实类别')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        # 保存图表
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = os.path.join(save_dir, f'confusion_matrix_{timestamp}.png')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"混淆矩阵已保存至: {save_path}")
        return True
    except Exception as e:
        print(f"保存混淆矩阵时出错: {str(e)}")
        return False

def plot_class_accuracy(y_true, y_pred, class_names, save_dir='results'):
    """绘制每个类别的准确率"""
    try:
        # 计算每个类别的准确率
        report = classification_report(y_true, y_pred, output_dict=True)
        class_accuracies = [report[str(i)]['precision'] for i in range(len(class_names))]
        
        # 创建图表
        plt.figure(figsize=(15, 8))
        bars = plt.bar(range(len(class_names)), class_accuracies)
        plt.title('各类别准确率')
        plt.xlabel('类别')
        plt.ylabel('准确率')
        plt.xticks(range(len(class_names)), class_names, rotation=45, ha='right')
        
        # 在柱状图上添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        # 保存图表
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = os.path.join(save_dir, f'class_accuracy_{timestamp}.png')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"类别准确率图表已保存至: {save_path}")
        return True
    except Exception as e:
        print(f"保存类别准确率图表时出错: {str(e)}")
        return False

def plot_confidence_distribution(model, test_generator, save_dir='results'):
    """绘制预测置信度分布"""
    try:
        # 获取预测结果
        predictions = model.predict(test_generator)
        confidences = np.max(predictions, axis=1)
        
        # 创建图表
        plt.figure(figsize=(10, 6))
        plt.hist(confidences, bins=50, alpha=0.7, color='blue')
        plt.title('预测置信度分布')
        plt.xlabel('置信度')
        plt.ylabel('样本数量')
        plt.grid(True, alpha=0.3)
        
        # 保存图表
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = os.path.join(save_dir, f'confidence_distribution_{timestamp}.png')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"置信度分布图表已保存至: {save_path}")
        return True
    except Exception as e:
        print(f"保存置信度分布图表时出错: {str(e)}")
        return False

def main():
    # 设置GPU内存增长
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)
    
    # 创建输出目录
    os.makedirs('models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # 配置参数
    BATCH_SIZE = 32
    EPOCHS = 50  # 增加训练轮次
    LEARNING_RATE = 0.001
    
    print("正在加载数据...")
    data_loader = HerbDataLoader('dataset', batch_size=BATCH_SIZE)
    num_classes = data_loader.get_num_classes()
    print(f"检测到{num_classes}个药材类别")
    
    # 保存类别名称
    class_names = data_loader.get_class_names()
    with open('models/class_names.txt', 'w', encoding='utf-8') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print("正在创建模型...")
    model = HerbClassifier(num_classes=num_classes)
    
    # 获取数据生成器
    train_generator = data_loader.get_train_generator()
    val_generator = data_loader.get_val_generator()
    test_generator = data_loader.get_test_generator()
    
    print("开始训练模型...")
    history = model.train(
        data_loader,
        epochs=EPOCHS,
        save_path='models/model_weights.h5'
    )
    
    # 在测试集上评估模型
    print("\n在测试集上评估模型...")
    test_loss, test_accuracy = model.evaluate(data_loader)
    print(f"测试集准确率: {test_accuracy:.4f}")
    print(f"测试集损失: {test_loss:.4f}")
    
    # 获取测试集的预测结果
    test_generator = data_loader.get_test_generator()
    y_pred = model.model.predict(test_generator)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = test_generator.classes
    
    # 绘制额外的评估图表
    print("\n生成评估图表...")
    plot_confusion_matrix(y_true, y_pred_classes, class_names)
    plot_class_accuracy(y_true, y_pred_classes, class_names)
    plot_confidence_distribution(model.model, test_generator)
    
    # 保存测试结果
    test_results = {
        'test_accuracy': float(test_accuracy),
        'test_loss': float(test_loss),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open('results/test_results.json', 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=4, ensure_ascii=False)
    
    print("\n训练完成！")
    print("模型权重已保存至: models/model_weights.h5")
    print("类别名称已保存至: models/class_names.txt")
    print("测试结果已保存至: results/test_results.json")
    print("混淆矩阵已保存至: results/confusion_matrix_*.png")
    print("类别准确率图表已保存至: results/class_accuracy_*.png")
    print("置信度分布图表已保存至: results/confidence_distribution_*.png")

if __name__ == '__main__':
    main() 