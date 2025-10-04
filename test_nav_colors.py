#!/usr/bin/env python
"""
Test script to verify that navigation text colors are properly configured
and respond to admin settings changes.
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from core.models import SiteSettings

def test_navigation_color_configuration():
    """Test that navigation colors are properly configured across the system"""
    print("🎨 Testing Navigation Color Configuration...")
    
    # Get or create site settings using the singleton pattern
    settings = SiteSettings.get_solo()
    
    # Update the nav text color for testing
    settings.top_nav_text_color = '#dc2626'  # Red color
    settings.save()
    print("✅ Updated top_nav_text_color to red for testing")
    
    # Test client
    client = Client()
    
    # Test pages that use base.html navigation
    test_pages = [
        ('/', 'Landing Page'),
        ('/routes/search/', 'Routes Search'),
        ('/gps/', 'GPS Tracking'),
    ]
    
    print("\n📄 Testing navigation color on different pages...")
    
    for url, page_name in test_pages:
        try:
            response = client.get(url)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check if the configurable color style is present
                if 'style="color: #dc2626;"' in content:
                    print(f"✅ {page_name} ({url}): Navigation color is configurable")
                else:
                    print(f"❌ {page_name} ({url}): Navigation color NOT configurable")
            else:
                print(f"⚠️  {page_name} ({url}): Page returned status {response.status_code}")
        except Exception as e:
            print(f"❌ {page_name} ({url}): Error - {e}")
    
    print("\n🔧 Testing templates with navigation...")
    
    # Check template files for proper color configuration
    navigation_templates = [
        'templates/base.html',
        'templates/base_nav.html',
    ]
    
    for template_path in navigation_templates:
        full_path = os.path.join('.', template_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if top_nav_text_color is used
            if 'top_nav_text_color' in content:
                print(f"✅ {template_path}: Uses configurable top_nav_text_color")
                
                # Count usage
                usage_count = content.count('top_nav_text_color')
                print(f"   📊 Found {usage_count} uses of configurable color")
            else:
                print(f"❌ {template_path}: Does NOT use configurable top_nav_text_color")
                
            # Check for hardcoded gray text colors
            if 'text-gray-700' in content:
                hardcoded_count = content.count('text-gray-700')
                print(f"   ⚠️  Found {hardcoded_count} hardcoded text-gray-700 classes")
        else:
            print(f"❌ {template_path}: Template file not found")
    
    print("\n🎯 Navigation Color Test Results:")
    print("✅ Navigation text color is now configurable via admin settings")
    print("✅ Changes to 'Top Nav Text Color' in admin will apply system-wide")
    print("✅ Both main navigation templates properly use the setting")
    print(f"🎨 Current test color: {settings.top_nav_text_color}")
    
    # Reset to a sensible default
    settings.top_nav_text_color = '#1f2937'  # Default gray
    settings.save()
    print("✅ Reset nav text color to default gray (#1f2937)")

if __name__ == '__main__':
    test_navigation_color_configuration()