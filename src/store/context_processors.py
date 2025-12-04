def categories_processor(request):
    """
    Context processor to make root categories and their subcategories available in all templates.
    Useful for the burger menu and navigation.
    """
    from store.models import Category
    root_categories = Category.objects.filter(parent=None).prefetch_related('subcategories')
    return {'all_categories': root_categories}

def footer_processor(request):
    """
    Context processor to make footer sections available in all templates.
    """
    from store.models import FooterSection
    footer_sections = FooterSection.objects.prefetch_related('links').all()
    return {'footer_sections': footer_sections}
