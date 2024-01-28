from .models import Category, Tags


def category_context(request):
    category = Category.objects.all()
    tags = Tags.objects.all()
    context = {
        'category': category,
        'tags': tags,
    }
    return context
