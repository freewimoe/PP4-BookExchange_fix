#!/usr/bin/env python
"""
Script to create test users for Code Institute assessment
Run this in VS Code or as a standalone script
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookexchange.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Create or update test users with known passwords"""
    
    # Delete existing test users to avoid conflicts
    User.objects.filter(username__in=['testadmin', 'demo', 'assessor']).delete()
    
    print("Creating test users...")
    
    # 1. Admin User
    admin_user = User.objects.create_user(
        username='assessor',
        email='assessor@codeinstitutetest.com',
        password='test123',
        first_name='Code',
        last_name='Institute'
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("✅ Created admin user: assessor / test123")
    
    # 2. Demo Student User  
    demo_user = User.objects.create_user(
        username='student',
        email='student@test.com',
        password='demo123',
        first_name='Demo',
        last_name='Student'
    )
    print("✅ Created demo user: student / demo123")
    
    # 3. Export users for Heroku
    from django.core.management import call_command
    import json
    
    # Export test users
    call_command('dumpdata', 'auth.User', '--indent=2', '--output=test_users.json')
    print("✅ Exported users to test_users.json")
    
    print("\n🎯 TEST ACCOUNTS READY:")
    print("Admin: assessor / test123")
    print("Student: student / demo123")
    print("\n📝 Add to README.md:")
    print("**Admin:** assessor / test123")
    print("**Demo:** student / demo123")

if __name__ == "__main__":
    create_test_users()