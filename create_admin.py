from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Xóa admin cũ nếu có
    old_admin = User.query.filter_by(username='admin').first()
    if old_admin:
        db.session.delete(old_admin)
    
    # Tạo admin mới
    admin = User(
        username='admin',
        email='admin@bookstore.com',
        password=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Tạo admin thành công!")
    print("Username: admin")
    print("Password: admin123")