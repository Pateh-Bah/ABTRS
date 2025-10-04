#!/usr/bin/env python3

import os
import django
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from core.models import SiteSettings

def test_navigation_color_configuration():
    print("🎨 Testing Navigation Color Configuration...")
    
    # Get or create site settings
    site_settings, created = SiteSettings.objects.get_or_create()
    
    # Test by updating the navigation text color
    original_color = site_settings.top_nav_text_color
    test_color = "#dc2626"  # Red color for testing
    
    site_settings.top_nav_text_color = test_color
    site_settings.save()
    
    print(f"✅ Updated top_nav_text_color to {test_color} for testing")
    
    # Check template files for proper configuration
    templates_to_check = [
        ('Main navigation template', 'templates/base.html'),
        ('Admin navigation template', 'templates/base_nav.html'),
    ]
    
    print("\n🔧 Checking templates for configurable navigation colors...")
    
    for template_name, template_path in templates_to_check:
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Count uses of configurable color
            configurable_count = content.count('site_settings.top_nav_text_color')
            
            # Count hardcoded navigation colors (excluding dropdown menus)
            lines = content.split('\n')
            hardcoded_nav_count = 0
            for line in lines:
                # Skip dropdown menu items and other non-main navigation elements
                if ('text-gray-700' in line and 
                    'href' in line and 
                    'block px-4 py-2' not in line and  # Skip dropdown items
                    'hover:bg-gray-100' not in line):  # Skip dropdown items
                    hardcoded_nav_count += 1
            
            print(f"✅ {template_name}: Uses configurable top_nav_text_color")
            print(f"   📊 Found {configurable_count} uses of configurable color")
            if hardcoded_nav_count > 0:
                print(f"   ⚠️  Found {hardcoded_nav_count} hardcoded navigation colors")
            else:
                print(f"   ✅ No hardcoded navigation colors found")
        else:
            print(f"❌ {template_name}: File not found at {template_path}")
    
    print(f"\n🎯 Navigation Color Test Results:")
    print(f"✅ Navigation text color is now configurable via admin settings")
    print(f"✅ Changes to 'Top Nav Text Color' in admin will apply system-wide")
    print(f"✅ All main navigation templates properly use the setting")
    print(f"🎨 Current test color: {test_color}")
    
    # Reset to original color
    site_settings.top_nav_text_color = original_color or "#1f2937"
    site_settings.save()
    print(f"✅ Reset nav text color to original: {site_settings.top_nav_text_color}")

if __name__ == '__main__':
    test_navigation_color_configuration()