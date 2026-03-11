from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from sqlalchemy import or_
import os
from datetime import datetime, timedelta
from model import HerbClassifier
import json
from data_loader import HerbDataLoader
from PIL import Image, ImageDraw
from baidu_ai import BaiduAI
from config import ALLOWED_EXTENSIONS
from models import db, User, Herb, DetectionHistory
from routes.admin import admin as admin_blueprint
from routes.admin_herbs import admin_herbs as admin_herbs_blueprint
from urllib.parse import urlparse, urljoin
import pymysql
import random
import huawei_iot.data_analyze
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS支持
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///herbs.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保所有必要的静态文件目录存在
os.makedirs('static/uploads/detections', exist_ok=True)
os.makedirs('static/uploads/herbs', exist_ok=True)
os.makedirs('static/examples', exist_ok=True)

# 初始化数据库
db.init_app(app)
migrate = Migrate(app, db)

# 初始化登录管理器
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('需要管理员权限')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    try:
        # 创建数据加载器实例
        data_loader = HerbDataLoader('dataset')
        # 获取示例图片
        examples = data_loader.get_example_images()
        # 将示例图片按每行4个分组
        example_rows = [examples[i:i + 4] for i in range(0, len(examples), 4)]
        return render_template('index.html', example_rows=example_rows)
    except Exception as e:
        print(f"加载示例图片时出错: {str(e)}")
        return render_template('index.html', example_rows=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册接口"""
    if request.method == 'POST':
        try:
            # 处理JSON格式的POST请求
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return jsonify({'message': '2'}), 400  # 请输入账号密码

                if User.query.filter_by(username=username).first():
                    return jsonify({'message': '3'}), 400  # 用户已存在

                user = User(
                    username=username,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()

                return jsonify({'message': '1'}), 201  # 用户注册成功

            # 处理表单格式的POST请求
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')
                
                if password != confirm_password:
                    flash('两次输入的密码不一致')
                    return redirect(url_for('register'))
                
                if User.query.filter_by(username=username).first():
                    flash('用户名已存在')
                    return redirect(url_for('register'))
                
                user = User(
                    username=username,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
                
                return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"注册失败: {str(e)}")
            if request.is_json:
                return jsonify({'message': str(e)}), 500
            flash('注册失败，请稍后重试')
            return redirect(url_for('register'))

    # GET请求返回注册页面
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录接口"""
    if request.method == 'POST':
        try:
            # 处理JSON格式的POST请求
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return jsonify({'message': '2'}), 400  # 请输入账号密码

                user = User.query.filter_by(username=username).first()

                if user and check_password_hash(user.password_hash, password):
                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'is_admin': user.is_admin
                    }
                    return jsonify({'message': '1', 'user': user_data}), 200
                else:
                    return jsonify({'message': '0'}), 401  # 用户名或密码错误

            # 处理表单格式的POST请求
            else:
                username = request.form.get('username')
                password = request.form.get('password')
                remember = request.form.get('remember', False) == 'on'
                
                user = User.query.filter_by(username=username).first()
                
                if user and check_password_hash(user.password_hash, password):
                    login_user(user, remember=remember)
                    
                    # 如果是AJAX请求，返回JSON响应
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({
                            'success': True,
                            'redirect': url_for('index'),
                            'is_admin': user.is_admin
                        })
                    
                    return redirect(url_for('index'))
                
                # 登录失败的处理
                error_message = '用户名或密码错误'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': False,
                        'message': error_message
                    }), 401
                
                flash(error_message, 'danger')
                return render_template('login.html')

        except Exception as e:
            app.logger.error(f"登录失败: {str(e)}")
            if request.is_json:
                return jsonify({'message': str(e)}), 500
            flash('登录过程中出现错误，请稍后重试', 'danger')
            return render_template('login.html')
    
    # GET请求返回登录页面
    return render_template('login.html')

def url_is_safe(target):
    """检查重定向URL是否安全"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 注册蓝图
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(admin_herbs_blueprint, url_prefix='/admin')

@app.route('/admin')
def admin_index():
    return redirect(url_for('admin.dashboard'))

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/herbs')
@login_required
@admin_required
def admin_herbs():
    herbs = Herb.query.all()
    return render_template('admin/herbs.html', herbs=herbs)

@app.route('/admin/history')
@login_required
@admin_required
def admin_history():
    history = DetectionHistory.query.order_by(DetectionHistory.detection_time.desc()).all()
    return render_template('admin/history.html', history=history)

# 药材管理
@app.route('/admin/herbs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_herb():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        similar_herbs = request.form.get('similar_herbs')
        effects = request.form.get('effects')
        properties = request.form.get('properties')
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'herbs', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                
                herb = Herb(
                    name=name,
                    image_path=file_path,
                    description=description,
                    similar_herbs=similar_herbs,
                    effects=effects,
                    properties=properties
                )
                db.session.add(herb)
                db.session.commit()
                flash('药材添加成功')
                return redirect(url_for('admin_herbs'))
    
    return render_template('admin/add_herb.html')

@app.route('/admin/herbs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_herb(id):
    herb = Herb.query.get_or_404(id)
    if request.method == 'POST':
        herb.name = request.form.get('name')
        herb.description = request.form.get('description')
        herb.similar_herbs = request.form.get('similar_herbs')
        herb.effects = request.form.get('effects')
        herb.properties = request.form.get('properties')
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'herbs', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                herb.image_path = file_path
        
        db.session.commit()
        flash('药材信息更新成功')
        return redirect(url_for('admin_herbs'))
    
    return render_template('admin/edit_herb.html', herb=herb)

@app.route('/admin/herbs/delete/<int:id>')
@login_required
@admin_required
def delete_herb(id):
    try:
        herb = Herb.query.get_or_404(id)
        
        # 首先删除与该药材关联的所有检测历史记录
        DetectionHistory.query.filter_by(herb_id=id).delete()
        
        # 然后删除药材本身
        db.session.delete(herb)
        db.session.commit()
        
        # 如果药材有关联的图片，也可以选择删除图片文件
        if herb.image_path:
            try:
                image_path = os.path.join('static', herb.image_path)
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                app.logger.error(f"删除药材图片失败: {str(e)}")
        
        flash('药材删除成功')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"删除药材失败: {str(e)}")
        flash('删除药材失败，请稍后重试')
    
    return redirect(url_for('admin_herbs'))

# 用户历史记录
@app.route('/history')
@login_required
def user_history():
    history = DetectionHistory.query.filter_by(user_id=current_user.id).order_by(DetectionHistory.detection_time.desc()).all()
    return render_template('history.html', history=history)

@app.route('/history/export')
@login_required
def export_history():
    history = DetectionHistory.query.filter_by(user_id=current_user.id).all()
    history_data = []
    for record in history:
        history_data.append({
            'id': record.id,
            'herb_name': record.herb.name,
            'detection_time': record.detection_time.strftime('%Y-%m-%d %H:%M:%S'),
            'confidence': record.confidence,
            'is_correct': record.is_correct
        })
    return jsonify(history_data)

# 添加文件类型检查函数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_similar_herbs(herb, limit=3):
    """获取相似药材推荐"""
    similar_herbs = []
    
    # 首先尝试从similar_herbs字段获取
    if herb.similar_herbs:
        similar_names = [name.strip() for name in herb.similar_herbs.split('、')]
        for name in similar_names:
            similar = Herb.query.filter_by(name=name).first()
            if similar and similar.id != herb.id and similar not in similar_herbs:
                similar_herbs.append(similar)
                if len(similar_herbs) >= limit:
                    return similar_herbs

    # 基于性味进行推荐
    if herb.properties:
        properties_list = [p.strip() for p in herb.properties.split('、')]
        properties_conditions = [Herb.properties.like(f"%{p}%") for p in properties_list]
        similar_by_properties = Herb.query.filter(
            Herb.id != herb.id,
            ~Herb.id.in_([h.id for h in similar_herbs]),
            or_(*properties_conditions)
        ).limit(limit - len(similar_herbs)).all()
        similar_herbs.extend(similar_by_properties)
    
    # 基于功效进行推荐
    if herb.effects and len(similar_herbs) < limit:
        effects_list = [e.strip() for e in herb.effects.split('、')]
        effects_conditions = [Herb.effects.like(f"%{e}%") for e in effects_list]
        
        similar_by_effects = Herb.query.filter(
            Herb.id != herb.id,
            ~Herb.id.in_([h.id for h in similar_herbs]),
            or_(*effects_conditions)
        ).limit(limit - len(similar_herbs)).all()
        similar_herbs.extend(similar_by_effects)
    
    return similar_herbs[:limit]

@app.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('没有选择文件')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # 保存上传的图片
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                relative_path = f"uploads/detections/{unique_filename}"
                save_path = os.path.join('static', relative_path)
                
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file.save(save_path)
                
                if not os.path.exists(save_path):
                    raise Exception("图片保存失败")
                
                # 创建数据加载器获取类别名称
                data_loader = HerbDataLoader('dataset')
                class_names = data_loader.get_class_names()
                
                # 使用本地模型进行预测
                model = HerbClassifier(model_path='models/model_weights.h5', num_classes=len(class_names))
                local_result = model.predict(save_path, class_names)
                
                # 使用百度AI进行预测
                try:
                    baidu_ai = BaiduAI()
                    baidu_result = baidu_ai.recognize_image(save_path)
                    # 处理百度AI结果以确保数据结构正确
                    if isinstance(baidu_result, dict) and baidu_result.get('name'):
                        formatted_baidu_result = baidu_result
                    else:
                        formatted_baidu_result = None
                        app.logger.warning("百度AI返回了无效的结果格式")
                except Exception as e:
                    app.logger.error(f"百度AI识别失败: {str(e)}")
                    formatted_baidu_result = None
                
                # 查找对应的药材信息
                herb = Herb.query.filter_by(name=local_result['name']).first()
                if not herb:
                    herb = Herb(
                        name=local_result['name'],
                        description="暂无描述",
                        effects="暂无功效记录",
                        properties="暂无性质记录"
                    )
                    db.session.add(herb)
                    db.session.commit()
                
                # 获取相似药材推荐
                similar_herbs = []
                
                # 1. 基于性味特征查找相似药材
                if herb.properties:
                    properties_list = [p.strip() for p in herb.properties.split('、')]
                    properties_conditions = [Herb.properties.like(f"%{p}%") for p in properties_list]
                    similar_by_properties = Herb.query.filter(
                        Herb.id != herb.id,
                        or_(*properties_conditions)
                    ).limit(5).all()  # 增加到5个
                    similar_herbs.extend([h for h in similar_by_properties if h not in similar_herbs])
                
                # 2. 基于功效查找相似药材
                if herb.effects:
                    effects_list = [e.strip() for e in herb.effects.split('、')]
                    effects_conditions = [Herb.effects.like(f"%{e}%") for e in effects_list]
                    
                    similar_by_effects = Herb.query.filter(
                        Herb.id != herb.id,
                        ~Herb.id.in_([h.id for h in similar_herbs]),
                        or_(*effects_conditions)
                    ).limit(5 - len(similar_herbs)).all()
                    similar_herbs.extend(similar_by_effects)
                
                # 3. 基于使用部位查找
                if len(similar_herbs) < 5 and herb.usage_parts:
                    similar_by_usage = Herb.query.filter(
                        Herb.id != herb.id,
                        ~Herb.id.in_([h.id for h in similar_herbs]),
                        Herb.usage_parts == herb.usage_parts
                    ).limit(5 - len(similar_herbs)).all()
                    similar_herbs.extend(similar_by_usage)
                
                # 4. 如果还不够，基于描述匹配
                if len(similar_herbs) < 5 and herb.description:
                    similar_by_desc = Herb.query.filter(
                        Herb.id != herb.id,
                        ~Herb.id.in_([h.id for h in similar_herbs]),
                        Herb.description.like(f"%{herb.description[:30]}%")  # 使用前30个字符进行匹配
                    ).limit(5 - len(similar_herbs)).all()
                    similar_herbs.extend(similar_by_desc)
                
                # 5. 如果有预定义的相似药材，确保它们也被包含
                if len(similar_herbs) < 5 and herb.similar_herbs:
                    predefined_similar = [name.strip() for name in herb.similar_herbs.split('、')]
                    for name in predefined_similar:
                        similar = Herb.query.filter_by(name=name).first()
                        if similar and similar.id != herb.id and similar not in similar_herbs:
                            similar_herbs.append(similar)
                            if len(similar_herbs) >= 5:
                                break
                
                # 准备相似药材的完整信息
                similar_herbs_data = []
                for similar_herb in similar_herbs[:5]:  # 限制最多显示5个
                    similar_herb_data = {
                        'id': similar_herb.id,
                        'name': similar_herb.name,
                        'english_name': similar_herb.english_name if hasattr(similar_herb, 'english_name') else None,
                        'properties': similar_herb.properties,
                        'effects': similar_herb.effects,
                        'usage_parts': similar_herb.usage_parts,
                        'description': similar_herb.description,
                        'season': similar_herb.season if hasattr(similar_herb, 'season') else None,
                        'image_path': similar_herb.image_path.replace('static/', '') if similar_herb.image_path else 'images/no-image.png'
                    }
                    similar_herbs_data.append(similar_herb_data)
                
                # 保存检测记录
                history = DetectionHistory(
                    user_id=current_user.id,
                    herb_id=herb.id,
                    image_path=relative_path,
                    confidence=local_result['confidence']
                )
                db.session.add(history)
                db.session.commit()
                
                app.logger.info(f"找到 {len(similar_herbs)} 个相似药材")
                
                # 准备完整的药材信息
                herb_json = {
                    'id': herb.id,
                    'name': herb.name,
                    'english_name': herb.english_name if hasattr(herb, 'english_name') else None,
                    'properties': herb.properties,
                    'effects': herb.effects,
                    'usage_parts': herb.usage_parts,
                    'description': herb.description,
                    'season': herb.season if hasattr(herb, 'season') else None,
                    'image_path': relative_path,
                    'similar_herbs': herb.similar_herbs
                }
                
                return render_template('result.html', 
                                     herb=herb, 
                                     herb_json=herb_json,
                                     confidence=local_result['confidence'],
                                     image_path=relative_path,
                                     similar_herbs=similar_herbs_data,
                                     baidu_result=formatted_baidu_result)
            
            except Exception as e:
                app.logger.error(f"识别过程中出现错误: {str(e)}")
                flash(f'识别过程中出现错误: {str(e)}')
                return redirect(request.url)
        else:
            flash('不支持的文件类型')
            return redirect(request.url)
    
    return render_template('detect.html')

# 添加一个用于修复历史图片路径的函数
def fix_image_paths():
    with app.app_context():
        records = DetectionHistory.query.all()
        for record in records:
            if record.image_path:
                # 统一使用正斜杠
                fixed_path = record.image_path.replace('\\', '/')
                # 移除开头的 static/ 如果存在
                if fixed_path.startswith('static/'):
                    fixed_path = fixed_path[7:]
                # 确保路径格式正确
                if not fixed_path.startswith('uploads/'):
                    fixed_path = f"uploads/detections/{os.path.basename(fixed_path)}"
                record.image_path = fixed_path
        db.session.commit()

# 在应用启动时修复历史图片路径
@app.before_request
def before_request():
    # 在这里添加需要在每个请求之前执行的代码
    pass  # 现在可以为空，因为初始化已经在应用启动时完成

@app.route('/herb_recommend')
@login_required
def herb_recommend():
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')
    per_page = 12

    # 基础查询
    query = Herb.query.filter(~Herb.name.in_(['train', 'test']))

    # 根据过滤类型筛选
    if filter_type == 'common':
        # 常用药材（照片数量大于5的）
        query = query.filter(Herb.photo_number > 5)
    elif filter_type == 'seasonal':
        # 应季药材（根据当前月份）
        current_month = datetime.now().month
        season_map = {
            12: '冬', 1: '冬', 2: '冬',
            3: '春', 4: '春', 5: '春',
            6: '夏', 7: '夏', 8: '夏',
            9: '秋', 10: '秋', 11: '秋'
        }
        current_season = season_map[current_month]
        query = query.filter(Herb.season == current_season)

    # 分页
    herbs = query.order_by(Herb.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('herb_recommend.html', 
                         herbs=herbs,
                         filter=filter_type)

@app.route('/api/herb/<int:herb_id>')
@login_required
def get_herb_detail(herb_id):
    try:
        herb = Herb.query.get_or_404(herb_id)
        return jsonify({
            'id': herb.id,
            'name': herb.name,
            'english_name': herb.english_name,
            'photo_number': herb.photo_number,
            'page_number': herb.page_number,
            'description': herb.description,
            'effects': herb.effects,
            'properties': herb.properties,
            'similar_herbs': herb.similar_herbs,
            'usage_parts': herb.usage_parts,
            'image_path': herb.image_path.replace('static/', '') if herb.image_path else None,
            'season': herb.season
        })
    except Exception as e:
        app.logger.error(f"获取药材详情时出错: {str(e)}")
        return jsonify({'error': '获取药材详情失败'}), 500

@app.route('/api/history/<int:record_id>')
@login_required
def get_history_detail(record_id):
    record = DetectionHistory.query.get_or_404(record_id)
    # 确保只能访问自己的历史记录
    if record.user_id != current_user.id:
        return jsonify({'error': '无权访问此记录'}), 403
    
    # 获取相似药材
    similar_herbs = get_similar_herbs(record.herb)
    
    return jsonify({
        'id': record.id,
        'image_path': record.image_path,
        'detection_time': record.detection_time.strftime('%Y-%m-%d %H:%M:%S'),
        'confidence': record.confidence,
        'herb': {
            'id': record.herb.id,
            'name': record.herb.name,
            'properties': record.herb.properties,
            'effects': record.herb.effects,
            'usage_parts': record.herb.usage_parts,
            'description': record.herb.description,
            'image_path': record.herb.image_path
        },
        'similar_herbs': [{
            'id': herb.id,
            'name': herb.name,
            'properties': herb.properties,
            'effects': herb.effects,
            'usage_parts': herb.usage_parts,
            'image_path': herb.image_path
        } for herb in similar_herbs]
    })

# 添加Sensor模型
class Sensor(db.Model):
    __tablename__ = 'sensor'
    temp = db.Column(db.String)  # 使用String类型，因为数据是字符串形式
    humi = db.Column(db.String)
    sound = db.Column(db.String)
    tilt = db.Column(db.String)
    vibrate = db.Column(db.String)
    fire = db.Column(db.String)
    smoke = db.Column(db.String)
    light_sense = db.Column(db.String)
    event_time = db.Column(db.String, primary_key=True)  # 使用String类型，因为数据是字符串形式

def init_sensor_table():
    """初始化sensor表结构"""
    try:
        # 检查表是否存在
        if not db.engine.dialect.has_table(db.engine, 'sensor'):
            # 如果表不存在，创建表
            db.create_all()
            print("sensor表创建成功")
        else:
            # 如果表存在，检查是否需要更新结构
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('sensor')]
            required_columns = ['temp', 'humi', 'sound', 'tilt', 'vibrate', 'fire', 'smoke', 'light_sense', 'event_time']
            
            # 检查是否缺少必要的列
            missing_columns = [col for col in required_columns if col not in columns]
            if missing_columns:
                print(f"sensor表缺少以下列: {missing_columns}")
                # 这里可以添加更新表结构的代码
    except Exception as e:
        print(f"初始化sensor表时出错: {str(e)}")

@app.route('/api/sensor/realtime', methods=['GET', 'POST'])
def get_sensor_realtime():
    """获取传感器实时数据接口"""
    if request.method == 'POST':
        try:
            # 获取POST数据
            data = request.get_json()
            select_sensors = data.get('sensors', [])  # 获取要查询的传感器列表
            sensor_num = data.get('sensor_num', 10)  # 获取查询数量，默认10条

            # 构建查询
            query = Sensor.query.order_by(Sensor.event_time.desc()).limit(sensor_num)
            
            # 执行查询
            results = query.all()
            
            if not results:
                return jsonify({
                    'success': False,
                    'message': '暂无传感器数据'
                }), 404

            # 获取最新的一条数据
            latest_data = results[0]
            result = {
                'temp': latest_data.temp,
                'humi': latest_data.humi,
                'sound': latest_data.sound,
                'tilt': latest_data.tilt,
                'vibrate': latest_data.vibrate,
                'fire': latest_data.fire,
                'smoke': latest_data.smoke,
                'light_sense': latest_data.light_sense,
                'event_time': latest_data.event_time
            }

            # 如果指定了要查询的传感器，只返回这些传感器的数据
            if select_sensors:
                filtered_result = {k: v for k, v in result.items() if k in select_sensors}
                filtered_result['event_time'] = result['event_time']  # 确保event_time始终存在
                return jsonify(filtered_result), 200

            return jsonify(result), 200
            
        except Exception as e:
            app.logger.error(f"处理传感器数据请求失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'处理请求失败: {str(e)}'
            }), 500
    
    # GET请求处理
    try:
        # 获取最新的传感器数据
        latest_data = Sensor.query.order_by(Sensor.event_time.desc()).first()
        
        if not latest_data:
            return jsonify({
                'success': False,
                'message': '暂无传感器数据'
            }), 404
            
        return jsonify({
            'success': True,
            'data': {
                'temperature': latest_data.temp,
                'humidity': latest_data.humi,
                'sound': latest_data.sound,
                'tilt': latest_data.tilt,
                'vibrate': latest_data.vibrate,
                'fire': latest_data.fire,
                'smoke': latest_data.smoke,
                'light_sense': latest_data.light_sense,
                'event_time': latest_data.event_time
            }
        })
    except Exception as e:
        app.logger.error(f"获取传感器实时数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取传感器数据失败'
        }), 500

@app.route('/api/sensor/history', methods=['GET'])
def get_sensor_history():
    """获取传感器历史数据接口"""
    try:
        # 获取查询参数
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        limit = request.args.get('limit', 100, type=int)
        
        # 构建查询
        query = Sensor.query
        
        # 添加时间过滤
        if start_time:
            start_timestamp = str(int(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp()))
            query = query.filter(Sensor.event_time >= start_timestamp)
        if end_time:
            end_timestamp = str(int(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp()))
            query = query.filter(Sensor.event_time <= end_timestamp)
            
        # 获取数据
        history_data = query.order_by(Sensor.event_time.desc()).limit(limit).all()
        
        # 格式化数据
        formatted_data = [{
            'temperature': record.temp,
            'humidity': record.humi,
            'sound': record.sound,
            'tilt': record.tilt,
            'vibrate': record.vibrate,
            'fire': record.fire,
            'smoke': record.smoke,
            'light_sense': record.light_sense,
            'event_time': record.event_time
        } for record in history_data]
        
        return jsonify({
            'success': True,
            'data': formatted_data,
            'total': len(formatted_data)
        })
    except Exception as e:
        app.logger.error(f"获取传感器历史数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取历史数据失败'
        }), 500

@app.route('/api/sensor/statistics', methods=['GET'])
def get_sensor_statistics():
    """获取传感器统计数据接口"""
    try:
        # 获取时间范围参数
        days = request.args.get('days', 7, type=int)
        
        # 首先获取数据库中的时间范围
        latest_record = Sensor.query.order_by(Sensor.event_time.desc()).first()
        oldest_record = Sensor.query.order_by(Sensor.event_time.asc()).first()
        
        if not latest_record or not oldest_record:
            return jsonify({
                'success': True,
                'data': {
                    'temperature': {'avg': 0, 'max': 0, 'min': 0},
                    'humidity': {'avg': 0, 'max': 0, 'min': 0},
                    'light': {'avg': 0, 'max': 0, 'min': 0}
                }
            })
        
        # 使用数据库中的最新时间作为结束时间
        end_timestamp = latest_record.event_time
        # 计算开始时间
        start_timestamp = str(int(end_timestamp) - (days * 24 * 60 * 60))
        
        app.logger.info(f"查询时间范围: {start_timestamp} 到 {end_timestamp}")
        
        # 查询指定时间范围内的数据
        records = Sensor.query.filter(
            Sensor.event_time >= start_timestamp,
            Sensor.event_time <= end_timestamp
        ).all()
        
        app.logger.info(f"查询到 {len(records)} 条记录")
        
        if not records:
            app.logger.info(f"数据库中共有 {Sensor.query.count()} 条记录")
            app.logger.info(f"最新记录时间: {latest_record.event_time}")
            app.logger.info(f"最旧记录时间: {oldest_record.event_time}")
            return jsonify({
                'success': True,
                'data': {
                    'temperature': {'avg': 0, 'max': 0, 'min': 0},
                    'humidity': {'avg': 0, 'max': 0, 'min': 0},
                    'light': {'avg': 0, 'max': 0, 'min': 0}
                }
            })
        
        # 计算统计数据
        try:
            temps = [float(r.temp) for r in records if r.temp and r.temp.strip()]
            humis = [float(r.humi) for r in records if r.humi and r.humi.strip()]
            lights = [float(r.light_sense) for r in records if r.light_sense and r.light_sense.strip()]
            
            app.logger.info(f"有效数据数量 - 温度: {len(temps)}, 湿度: {len(humis)}, 光照: {len(lights)}")
            
            if temps:
                app.logger.info(f"温度数据示例: {temps[:5]}")
            if humis:
                app.logger.info(f"湿度数据示例: {humis[:5]}")
            if lights:
                app.logger.info(f"光照数据示例: {lights[:5]}")
            
            statistics = {
                'temperature': {
                    'avg': round(sum(temps) / len(temps), 2) if temps else 0,
                    'max': round(max(temps), 2) if temps else 0,
                    'min': round(min(temps), 2) if temps else 0
                },
                'humidity': {
                    'avg': round(sum(humis) / len(humis), 2) if humis else 0,
                    'max': round(max(humis), 2) if humis else 0,
                    'min': round(min(humis), 2) if humis else 0
                },
                'light': {
                    'avg': round(sum(lights) / len(lights), 2) if lights else 0,
                    'max': round(max(lights), 2) if lights else 0,
                    'min': round(min(lights), 2) if lights else 0
                }
            }
            
            app.logger.info(f"统计结果: {statistics}")
            
            return jsonify({
                'success': True,
                'data': statistics
            })
        except Exception as e:
            app.logger.error(f"计算统计数据时出错: {str(e)}")
            return jsonify({
                'success': True,
                'data': {
                    'temperature': {'avg': 0, 'max': 0, 'min': 0},
                    'humidity': {'avg': 0, 'max': 0, 'min': 0},
                    'light': {'avg': 0, 'max': 0, 'min': 0}
                },
                'error': str(e)
            })
    except Exception as e:
        app.logger.error(f"获取传感器统计数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取统计数据失败'
        }), 500

@app.route('/sensor_dashboard')
@login_required
def sensor_dashboard():
    """传感器数据监控页面"""
    return render_template('sensor_dashboard.html')

@app.route('/sensor_items', methods=['POST'])
# @login_required
def sensor_items():
    """获取传感器数据项接口"""
    try:
        # 定义传感器字段映射
        sensor_fields = {
            "temp": "温度",
            "humi": "湿度",
            "sound": "声音",
            "tilt": "倾斜",
            "vibrate": "振动",
            "fire": "火焰",
            "smoke": "烟雾",
            "light_sense": "光敏",
        }

        # 获取POST数据
        data = request.get_json()
        select_sensors = data.get('sensors', [])  # 获取要查询的传感器列表
        sensor_num = data.get('sensor_num', 10)  # 获取查询数量，默认10条

        if not select_sensors or select_sensors not in sensor_fields:
            return jsonify({
                'success': False,
                'message': '无效的传感器类型'
            }), 400

        value_sensor = sensor_fields[select_sensors]

        # 构建查询
        query = Sensor.query.with_entities(
            getattr(Sensor, select_sensors),
            Sensor.event_time
        ).order_by(Sensor.event_time.desc()).limit(sensor_num)

        # 执行查询
        results = query.all()

        if not results:
            return jsonify({
                'success': False,
                'message': '暂无传感器数据'
            }), 404

        # 处理查询结果
        formatted_results = []
        for result in results:
            item = {
                select_sensors: str(result[0]),  # 传感器值
                'event_time': result[1]  # 时间戳
            }
            # 添加dataItem字段
            item['dataItem'] = item[select_sensors]
            # 删除原始传感器字段
            del item[select_sensors]
            formatted_results.append(item)

        # 调用数据分析函数
        analyse = huawei_iot.data_analyze.all_result(select_sensors, {'subscriptions': formatted_results})

        return jsonify({
            'subscriptions': formatted_results,
            'value': [value_sensor],
            'analyse': analyse
        }), 200

    except Exception as e:
        app.logger.error(f"获取传感器数据项失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取数据失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    with app.app_context():
        # 初始化sensor表
        init_sensor_table()
        # 创建数据库表
        db.create_all()
        # 修复历史图片路径
        fix_image_paths()
        # 确保必要的目录存在
        os.makedirs('static/uploads/detections', exist_ok=True)
        os.makedirs('static/uploads/herbs', exist_ok=True)
        os.makedirs('static/examples', exist_ok=True)
        # 创建默认的 no-image 图片
        if not os.path.exists('static/images/no-image.png'):
            # 如果没有默认图片，创建一个简单的占位图片
            img = Image.new('RGB', (200, 200), color='lightgray')
            d = ImageDraw.Draw(img)
            d.text((70, 90), "无图片", fill='darkgray')
            os.makedirs('static/images', exist_ok=True)
            img.save('static/images/no-image.png')
    
    # 启动应用
    app.run(debug=True, host='0.0.0.0', port=5000) 