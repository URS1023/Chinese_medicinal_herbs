from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    detections = db.relationship('DetectionHistory', backref='user', lazy=True)

# 药材模型
class Herb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    english_name = db.Column(db.String(100))
    photo_number = db.Column(db.Integer, default=0)
    page_number = db.Column(db.String(50))
    description = db.Column(db.Text)
    effects = db.Column(db.Text)
    properties = db.Column(db.Text)
    similar_herbs = db.Column(db.Text)
    usage_parts = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    season = db.Column(db.String(20))  # 添加season字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    detections = db.relationship('DetectionHistory', backref='herb', lazy=True)

# 检测历史记录模型
class DetectionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    herb_id = db.Column(db.Integer, db.ForeignKey('herb.id'), nullable=False)
    image_path = db.Column(db.String(200))
    confidence = db.Column(db.Float)
    detection_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_correct = db.Column(db.Boolean, default=True) 