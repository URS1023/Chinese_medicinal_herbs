from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Herb
from routes.admin import admin_required
from werkzeug.utils import secure_filename
import os

admin_herbs = Blueprint('admin_herbs', __name__)

@admin_herbs.route('/herbs')
@login_required
@admin_required
def herbs():
    herbs = Herb.query.all()
    return render_template('admin/herbs.html', herbs=herbs)

@admin_herbs.route('/herbs/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_herb():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        effects = request.form.get('effects')
        properties = request.form.get('properties')
        
        if Herb.query.filter_by(name=name).first():
            flash('药材名称已存在', 'danger')
            return redirect(url_for('admin_herbs.herbs'))
        
        herb = Herb(
            name=name,
            description=description,
            effects=effects,
            properties=properties
        )
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/uploads/herbs', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                herb.image_path = file_path
        
        db.session.add(herb)
        db.session.commit()
        flash('药材添加成功', 'success')
        return redirect(url_for('admin_herbs.herbs'))
    
    return render_template('admin/add_herb.html')

@admin_herbs.route('/herbs/<int:herb_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_herb(herb_id):
    herb = Herb.query.get_or_404(herb_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        existing_herb = Herb.query.filter_by(name=name).first()
        if existing_herb and existing_herb.id != herb_id:
            flash('药材名称已存在', 'danger')
            return redirect(url_for('admin_herbs.herbs'))
        
        herb.name = name
        herb.description = request.form.get('description')
        herb.effects = request.form.get('effects')
        herb.properties = request.form.get('properties')
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/uploads/herbs', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                herb.image_path = file_path
        
        db.session.commit()
        flash('药材更新成功', 'success')
        return redirect(url_for('admin_herbs.herbs'))
    
    return render_template('admin/edit_herb.html', herb=herb)

@admin_herbs.route('/herbs/<int:herb_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_herb(herb_id):
    herb = Herb.query.get_or_404(herb_id)
    db.session.delete(herb)
    db.session.commit()
    flash('药材删除成功', 'success')
    return redirect(url_for('admin_herbs.herbs')) 