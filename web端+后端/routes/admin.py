from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Herb, DetectionHistory
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('您没有权限访问此页面', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    herb_count = Herb.query.count()
    detection_count = DetectionHistory.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_history = DetectionHistory.query.order_by(DetectionHistory.detection_time.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         user_count=user_count,
                         herb_count=herb_count,
                         detection_count=detection_count,
                         recent_users=recent_users,
                         recent_history=recent_history)

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    if User.query.filter_by(username=username).first():
        flash('用户名已存在', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    
    flash('用户添加成功', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>')
@login_required
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'username': user.username,
        'is_admin': user.is_admin
    })

@admin.route('/users/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id and not request.form.get('is_admin'):
        flash('不能取消自己的管理员权限', 'danger')
        return redirect(url_for('admin.users'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != user_id:
        flash('用户名已存在', 'danger')
        return redirect(url_for('admin.users'))
    
    user.username = username
    if password:
        user.password_hash = generate_password_hash(password)
    user.is_admin = is_admin
    
    db.session.commit()
    flash('用户信息更新成功', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({'error': '不能删除自己的账号'}), 400
    
    user = User.query.get_or_404(user_id)
    if user.is_admin and user.id == current_user.id:
        return jsonify({'error': '不能删除自己的管理员账号'}), 400
    
    DetectionHistory.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': '用户删除成功'})

@admin.route('/users/<int:user_id>/view')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    history = DetectionHistory.query.filter_by(user_id=user_id).order_by(DetectionHistory.detection_time.desc()).all()
    return render_template('admin/user_detail.html', user=user, history=history)

@admin.route('/history')
@login_required
@admin_required
def history():
    history = DetectionHistory.query.order_by(DetectionHistory.detection_time.desc()).all()
    return render_template('admin/history.html', history=history) 