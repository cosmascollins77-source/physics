#!/usr/bin/env python
"""
Comprehensive test script for Physics Learning Platform
Tests all major components and pages
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse
from django.template.loader import get_template

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'physics_application.settings')
django.setup()

def test_database():
    """Test database models and data"""
    print("🔍 Testing Database...")
    
    from topics.models import PhysicsTopic, CBCGrade
    from simulations.models import Simulation
    from quizzes.models import Quiz
    
    try:
        topics_count = PhysicsTopic.objects.count()
        grades_count = CBCGrade.objects.count()
        simulations_count = Simulation.objects.count()
        quizzes_count = Quiz.objects.count()
        
        print(f"✅ Topics: {topics_count}")
        print(f"✅ Grades: {grades_count}")
        print(f"✅ Simulations: {simulations_count}")
        print(f"✅ Quizzes: {quizzes_count}")
        
        if topics_count > 0 and grades_count > 0:
            print("✅ Database: WORKING")
            return True
        else:
            print("❌ Database: NO DATA")
            return False
    except Exception as e:
        print(f"❌ Database: ERROR - {e}")
        return False

def test_templates():
    """Test template loading"""
    print("\n🔍 Testing Templates...")
    
    templates = [
        'base/base.html',
        'topics/home.html',
        'topics/topic_list.html',
        'topics/topic_detail.html',
        'simulations/simulation_list.html',
        'simulations/interactive.html',
        'quizzes/quiz_list.html',
    ]
    
    try:
        for template in templates:
            get_template(template)
            print(f"✅ {template}")
        print("✅ Templates: ALL WORKING")
        return True
    except Exception as e:
        print(f"❌ Templates: ERROR - {e}")
        return False

def test_urls():
    """Test URL patterns"""
    print("\n🔍 Testing URLs...")
    
    urls = [
        ('topics:home', '/'),
        ('topics:topic_list', '/topics/'),
        ('simulations:simulation_list', '/simulations/'),
        ('quizzes:quiz_list', '/quizzes/'),
    ]
    
    try:
        for url_name, expected_path in urls:
            actual_path = reverse(url_name)
            if actual_path == expected_path:
                print(f"✅ {url_name}: {actual_path}")
            else:
                print(f"❌ {url_name}: Expected {expected_path}, got {actual_path}")
                return False
        print("✅ URLs: ALL WORKING")
        return True
    except Exception as e:
        print(f"❌ URLs: ERROR - {e}")
        return False

def test_pages():
    """Test page responses"""
    print("\n🔍 Testing Pages...")
    
    client = Client()
    pages = [
        ('/', 'Home'),
        ('/topics/', 'Topics List'),
        ('/simulations/', 'Simulations List'),
        ('/quizzes/', 'Quizzes List'),
    ]
    
    try:
        for url, name in pages:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: {url} (200)")
            else:
                print(f"❌ {name}: {url} ({response.status_code})")
                return False
        print("✅ Pages: ALL WORKING")
        return True
    except Exception as e:
        print(f"❌ Pages: ERROR - {e}")
        return False

def test_topic_detail():
    """Test topic detail page"""
    print("\n🔍 Testing Topic Detail...")
    
    try:
        from topics.models import PhysicsTopic
        topic = PhysicsTopic.objects.first()
        if topic:
            client = Client()
            response = client.get(f'/topic/{topic.slug}/')
            if response.status_code == 200:
                print(f"✅ Topic Detail: /topic/{topic.slug}/ (200)")
                return True
            else:
                print(f"❌ Topic Detail: {response.status_code}")
                return False
        else:
            print("❌ Topic Detail: NO TOPICS FOUND")
            return False
    except Exception as e:
        print(f"❌ Topic Detail: ERROR - {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Physics Learning Platform - Comprehensive Test")
    print("=" * 50)
    
    tests = [
        test_database,
        test_templates,
        test_urls,
        test_pages,
        test_topic_detail,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Platform is working perfectly!")
        print(f"✅ {passed}/{total} tests passed")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("❌ Some issues found. Check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

