from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models import db, User, SystemUser

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

# 首页路由 - 重定向到登录页面
@app.route('/')
def index():
    return redirect('/login')

# 主页 - 需要登录才能访问
@app.route('/home')
def home():
    return render_template('index.html')

# 统计页面 - 需要登录才能访问
@app.route('/stats')
def stats():
    return render_template('stats.html')

# 登录页面
@app.route('/login')
def login():
    return render_template('login.html')

# 注册页面
@app.route('/register')
def register():
    return render_template('register.html')

# 用户添加页面
@app.route('/users/add')
def add_user():
    return render_template('add_user.html')

# 用户列表页面
@app.route('/users/list')
def list_user():
    return render_template('list_user.html')

# API路由
@app.route('/api/users', methods=['GET'])
def get_users():
    # 检查是否有搜索参数
    search = request.args.get('search')
    department = request.args.get('department')
    position = request.args.get('position')
    gender = request.args.get('gender')
    age_min = request.args.get('ageMin', type=int)
    age_max = request.args.get('ageMax', type=int)
    
    # 构建查询
    query = User.query
    
    # 搜索条件
    if search:
        query = query.filter(
            (User.name.like(f'%{search}%')) | 
            (User.email.like(f'%{search}%')) |
            (User.phone.like(f'%{search}%')) |
            (User.department.like(f'%{search}%'))
        )
    
    # 部门筛选
    if department:
        query = query.filter(User.department == department)
    
    # 职位筛选
    if position:
        query = query.filter(User.position == position)
    
    # 性别筛选
    if gender:
        query = query.filter(User.gender == gender)
    
    # 年龄范围筛选
    if age_min is not None:
        query = query.filter(User.age >= age_min)
    if age_max is not None:
        query = query.filter(User.age <= age_max)
    
    # 执行查询
    users = query.all()
    
    return jsonify([{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
        "address": user.address,
        "department": user.department,
        "position": user.position
    } for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        age=data.get('age'),
        gender=data.get('gender'),
        address=data.get('address'),
        department=data.get('department'),
        position=data.get('position')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "phone": new_user.phone,
        "age": new_user.age,
        "gender": new_user.gender,
        "address": new_user.address,
        "department": new_user.department,
        "position": new_user.position
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.name = data['name']
    user.email = data['email']
    user.phone = data.get('phone')
    user.age = data.get('age')
    user.gender = data.get('gender')
    user.address = data.get('address')
    user.department = data.get('department')
    user.position = data.get('position')
    db.session.commit()
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
        "address": user.address,
        "department": user.department,
        "position": user.position
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# 注册API
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    
    # 检查用户名是否已存在
    existing_user = SystemUser.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "用户名已存在"}), 400
    
    # 检查邮箱是否已存在
    existing_email = SystemUser.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({"error": "邮箱已被注册"}), 400
    
    # 创建新用户
    new_user = SystemUser(
        username=data['username'],
        email=data['email'],
        password=data['password']  # 注意：实际应用中应该加密密码
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "注册成功"}), 201

# 登录API
@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    
    # 查找用户
    user = SystemUser.query.filter_by(username=data['username']).first()
    
    if not user or user.password != data['password']:
        return jsonify({"error": "用户名或密码错误"}), 401
    
    return jsonify({"message": "登录成功", "user": {"username": user.username, "email": user.email}})

if __name__ == '__main__':
    app.run(debug=True)