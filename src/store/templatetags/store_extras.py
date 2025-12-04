from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_category_placeholder_icon(category_name):
    """Return Font Awesome icon class for category"""
    category_lower = category_name.lower() if category_name else ''
    
    # Map category names to Font Awesome icons
    icon_map = {
        'мобільні': 'fa-mobile-alt',
        'телефон': 'fa-mobile-alt',
        'ноутбук': 'fa-laptop',
        'laptop': 'fa-laptop',
        'телевізор': 'fa-tv',
        'tv': 'fa-tv',
        'смарт': 'fa-watch',
        'watch': 'fa-watch',
        'планшет': 'fa-tablet-alt',
        'tablet': 'fa-tablet-alt',
        'фотоапарат': 'fa-camera',
        'camera': 'fa-camera',
    }
    
    for key, icon in icon_map.items():
        if key in category_lower:
            return icon
    
    # Default icon
    return 'fa-box'

@register.filter
def get_category_placeholder_color(category_name):
    """Return color for category placeholder"""
    category_lower = category_name.lower() if category_name else ''
    
    # Map category names to colors
    color_map = {
        'мобільні': '#007bff',
        'телефон': '#007bff',
        'ноутбук': '#6c757d',
        'laptop': '#6c757d',
        'телевізор': '#28a745',
        'tv': '#28a745',
        'смарт': '#17a2b8',
        'watch': '#17a2b8',
        'планшет': '#ffc107',
        'tablet': '#ffc107',
        'фотоапарат': '#dc3545',
        'camera': '#dc3545',
    }
    
    for key, color in color_map.items():
        if key in category_lower:
            return color
    
    # Default color
    return '#6c757d'
