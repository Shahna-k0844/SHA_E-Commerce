from .models import*
def category_context(request):
    categories = Category.objects.all().prefetch_related('catcategory_set')
    category=Category.objects.all()
    # user=User.objects.all() if request.user.is_authenticated else None

    return  {'categories': categories,'category':category,'user':request.user}
