from app import app, db, Book

with app.app_context():
    books = [
        Book(title='Đắc Nhân Tâm', author='Dale Carnegie', price=95000, 
             description='Cuốn sách nổi tiếng về nghệ thuật giao tiếp và ứng xử', stock=50),
        Book(title='Nhà Giả Kim', author='Paulo Coelho', price=79000,
             description='Hành trình tìm kiếm kho báu và ý nghĩa cuộc sống', stock=30),
        Book(title='Sapiens', author='Yuval Noah Harari', price=199000,
             description='Lược sử loài người từ thời nguyên thủy đến hiện đại', stock=25),
        Book(title='Atomic Habits', author='James Clear', price=149000,
             description='Cách xây dựng thói quen tốt và phá bỏ thói quen xấu', stock=40),
        Book(title='Tuổi Trẻ Đáng Giá Bao Nhiêu', author='Rosie Nguyễn', price=89000,
             description='Sách về phát triển bản thân cho giới trẻ', stock=60)
    ]
    
    for book in books:
        db.session.add(book)
    
    db.session.commit()
    print(f"✅ Đã thêm {len(books)} cuốn sách mẫu!")