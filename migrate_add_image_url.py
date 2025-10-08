"""
Script migration để thêm cột image_url vào bảng books
Chạy file này một lần để cập nhật database
"""

from app import app, db
from sqlalchemy import text

def add_image_url_column():
    """Thêm cột image_url vào bảng books"""
    with app.app_context():
        try:
            # Kiểm tra xem cột đã tồn tại chưa
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='books' AND column_name='image_url'
            """)
            
            result = db.session.execute(check_query).fetchone()
            
            if result:
                print("✅ Cột 'image_url' đã tồn tại trong bảng 'books'")
                return
            
            # Thêm cột image_url với giá trị mặc định
            alter_query = text("""
                ALTER TABLE books 
                ADD COLUMN image_url VARCHAR(500) 
                DEFAULT 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400'
            """)
            
            db.session.execute(alter_query)
            db.session.commit()
            
            print("✅ Đã thêm cột 'image_url' vào bảng 'books' thành công!")
            print("📸 Giá trị mặc định: https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400")
            
            # Cập nhật tất cả các sách hiện có với hình ảnh mặc định
            update_query = text("""
                UPDATE books 
                SET image_url = 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400'
                WHERE image_url IS NULL
            """)
            
            db.session.execute(update_query)
            db.session.commit()
            
            print("✅ Đã cập nhật hình ảnh mặc định cho tất cả sách hiện có!")
            
        except Exception as e:
            print(f"❌ Lỗi khi thêm cột: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Bắt đầu migration...")
    add_image_url_column()
    print("✨ Hoàn thành!")