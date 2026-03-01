# tasks.py - handles all task related routes
# dashboard, task CRUD, timer updates, exports

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response
from flask_login import login_required, current_user
from models import db, Task, CATEGORIES
from datetime import datetime, timedelta
import pandas as pd
import os

tasks_bp = Blueprint('tasks_bp', __name__)


@tasks_bp.route('/')
@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    # get user's tasks for dashboard stats
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # calculate stats for dashboard
    total_tasks = len(user_tasks)
    completed = len([t for t in user_tasks if t.status == 'Completed'])
    pending = total_tasks - completed
    
    # total time spent across all tasks
    total_time = sum([t.time_spent for t in user_tasks])
    
    # time spent per category for chart
    category_time = {}
    for cat in CATEGORIES:
        cat_tasks = [t for t in user_tasks if t.category == cat]
        category_time[cat] = sum([t.time_spent for t in cat_tasks])
    
    # weekly data for chart - last 7 days
    weekly_data = get_weekly_stats(current_user.id)
    
    # format total time
    hours = total_time // 3600
    minutes = (total_time % 3600) // 60
    formatted_time = f"{hours}h {minutes}m"
    
    return render_template('dashboard.html', 
                          total_tasks=total_tasks,
                          completed=completed,
                          pending=pending,
                          total_time=formatted_time,
                          category_time=category_time,
                          weekly_data=weekly_data,
                          categories=CATEGORIES)


# helper function for weekly stats
def get_weekly_stats(user_id):
    today = datetime.utcnow().date()
    weekly = {}
    
    # start from 6 days ago and go to today (oldest to newest)
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_name = day.strftime('%a')
        
        # get completed tasks for this day
        completed_count = Task.query.filter(
            Task.user_id == user_id,
            Task.status == 'Completed',
            db.func.date(Task.completed_at) == day
        ).count()
        
        weekly[day_name] = completed_count
    
    return weekly


@tasks_bp.route('/tasks')
@login_required
def tasks_list():
    # get all tasks for current user
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks, categories=CATEGORIES)


@tasks_bp.route('/task/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description', '')
    category = request.form.get('category', 'Personal')
    
    # simple validation before insert
    if not title:
        flash('Task title is required!', 'error')
        return redirect(url_for('tasks_bp.tasks_list'))
    
    # create new task
    new_task = Task(
        title=title,
        description=description,
        category=category,
        user_id=current_user.id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    flash('Task added successfully!', 'success')
    return redirect(url_for('tasks_bp.tasks_list'))


@tasks_bp.route('/task/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # make sure user owns this task
    if task.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('tasks_bp.tasks_list'))
    
    task.title = request.form.get('title', task.title)
    task.description = request.form.get('description', task.description)
    task.category = request.form.get('category', task.category)
    
    db.session.commit()
    flash('Task updated!', 'success')
    return redirect(url_for('tasks_bp.tasks_list'))


@tasks_bp.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # security check
    if task.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('tasks_bp.tasks_list'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted.', 'info')
    return redirect(url_for('tasks_bp.tasks_list'))


@tasks_bp.route('/task/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    # toggle status
    if task.status == 'Pending':
        task.status = 'Completed'
        task.completed_at = datetime.utcnow()
    else:
        task.status = 'Pending'
        task.completed_at = None
    
    db.session.commit()
    return jsonify({'status': task.status})


@tasks_bp.route('/task/update-time/<int:task_id>', methods=['POST'])
@login_required
def update_time(task_id):
    # saving task time after pause
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    time_spent = data.get('time_spent', 0)
    
    # update the time
    task.time_spent = time_spent
    db.session.commit()
    
    return jsonify({'success': True, 'time_spent': task.time_spent})


@tasks_bp.route('/export/csv')
@login_required
def export_csv():
    # get user tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # prepare data for pandas
    data = []
    for t in tasks:
        data.append({
            'Title': t.title,
            'Description': t.description or '',
            'Category': t.category,
            'Status': t.status,
            'Time Spent': t.get_formatted_time(),
            'Created': t.created_at.strftime('%Y-%m-%d %H:%M'),
            'Completed': t.completed_at.strftime('%Y-%m-%d %H:%M') if t.completed_at else 'N/A'
        })
    
    # create dataframe and convert to csv
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    
    # return as downloadable file
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=tasks_export.csv'}
    )


@tasks_bp.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    # api endpoint for charts
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # category time data
    category_time = {}
    for cat in CATEGORIES:
        cat_tasks = [t for t in user_tasks if t.category == cat]
        category_time[cat] = sum([t.time_spent for t in cat_tasks]) // 60  # convert to minutes
    
    # weekly completion data
    weekly_data = get_weekly_stats(current_user.id)
    
    # status counts
    completed = len([t for t in user_tasks if t.status == 'Completed'])
    pending = len([t for t in user_tasks if t.status == 'Pending'])
    
    return jsonify({
        'categoryTime': category_time,
        'weeklyData': weekly_data,
        'statusData': {'Completed': completed, 'Pending': pending}
    })
