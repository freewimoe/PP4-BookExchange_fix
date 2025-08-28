#!/usr/bin/env python
"""
Script to create test users for BookExchange app
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookexchange.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Create test users as specified in README.md"""
    
    # Create assessor (admin) user
    if not User.objects.filter(username='assessor').exists():
        assessor = User.objects.create_user(
            username='assessor',
            email='assessor@example.com',
            password='test123'
        )
        assessor.is_staff = True
        assessor.is_superuser = True
        assessor.save()
        print("✅ Created admin user 'assessor' with password 'test123'")
    else:
        print("ℹ️ Admin user 'assessor' already exists")
    
    # Create student user
    if not User.objects.filter(username='student').exists():
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='demo123'
        )
        student.save()
        print("✅ Created student user 'student' with password 'demo123'")
    else:
        print("ℹ️ Student user 'student' already exists")

if __name__ == '__main__':
    create_test_users()
    print("\n🎉 Test users created successfully!")
    print("\nTest Accounts:")
    print("Admin: assessor / test123")
    print("Student: student / demo123")
