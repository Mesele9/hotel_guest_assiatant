from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MainCategory, Category, MenuItem, Tag, Rating
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from .forms import MainCategoryForm, CategoryForm, TagForm, MenuItemForm, RatingForm
from common_user.decorators import public_view, role_required


@public_view
def menu_view(request):
    main_categories = MainCategory.objects.all()
    
    # Default to "Restaurant" if exists, else first main category
    default_main_category = MainCategory.objects.filter(name="Restaurant").first()
    if not default_main_category and main_categories.exists():
        default_main_category = main_categories.first()
    
    # Get selected main category
    selected_main_category_id = request.GET.get('main_category')
    if selected_main_category_id:
        selected_main_category = get_object_or_404(MainCategory, id=selected_main_category_id)
    elif default_main_category:
        selected_main_category = default_main_category
    else:
        selected_main_category = None
    
    # Get parameters
    selected_subcategory = request.GET.get('subcategory')
    search_query = request.GET.get('search', '')
    
    # Get subcategories
    subcategories = Category.objects.filter(main_category=selected_main_category) if selected_main_category else []
    
    # Base queryset
    menu_items = MenuItem.objects.none()

    if selected_main_category:
        # Get all subcategory IDs for the main category
        subcategory_ids = subcategories.values_list('id', flat=True)
        
        if selected_subcategory or search_query:
            # Start with items in the main category
            menu_items = MenuItem.objects.filter(
                categories__id__in=subcategory_ids,
                is_active=True
            ).distinct()
            
            # Apply subcategory filter if selected
            if selected_subcategory:
                menu_items = menu_items.filter(categories__id=selected_subcategory)
            
            # Apply search filter if query exists
            if search_query:
                menu_items = menu_items.filter(
                    Q(name__icontains=search_query) | 
                    Q(description__icontains=search_query)
                ).distinct()

    context = {
        'main_categories': main_categories,
        'selected_main_category': selected_main_category,
        'subcategories': subcategories,
        'menu_items': menu_items,
        'selected_subcategory': selected_subcategory,
        'search_query': search_query
    }
    return render(request, 'menu/menu.html', context)


@public_view
def menu_item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    ratings = Rating.objects.filter(menu_item=item).order_by('-created_at')
    category_id = request.GET.get('category')

    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.menu_item = item
            rating.save()
            return redirect('menu_item_detail', item_id=item_id)
    else:
        form = RatingForm()

    context = {
        'item': item,
        'ratings': ratings,
        'category_id': category_id,
        'form': form
    }
    return render(request, 'menu/detail.html', context)


@role_required('fb')
@login_required
def menu_dashboard(request):
    recent_ratings = Rating.objects.select_related('menu_item').order_by('-created_at')[:5]
    menu_items_count = MenuItem.objects.count()
    categories_count = Category.objects.count()
    tags_count = Tag.objects.count()
    
    context = {
        'recent_ratings': recent_ratings,
        'menu_items_count': menu_items_count,
        'categories_count': categories_count,
        'tags_count': tags_count,
    }
    return render(request, 'menu/dashboard/menu_dashboard.html', context)


@role_required('fb')
@login_required
def menu_item_list(request):
    menu_items = MenuItem.objects.select_related().prefetch_related('categories', 'tags').all()
    selected_category = None
    search_query = ''

    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        try:
            selected_category = Category.objects.get(id=category_filter)
            menu_items = menu_items.filter(categories__id=category_filter)
        except (Category.DoesNotExist, ValueError):
            pass

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query.strip():
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    categories = Category.objects.all()
    
    context = {
        'menu_items': menu_items.distinct(),
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query
    }
    return render(request, 'menu/dashboard/menuitem_list.html', context)


@role_required('fb')
@login_required
def menu_item_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item created successfully!')
            return redirect('menu_item_list')
    else:
        form = MenuItemForm()
    
    context = {'form': form}
    return render(request, 'menu/dashboard/menuitem_form.html', context)


@role_required('fb')
@login_required
def menu_item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu_item_list')
    else:
        form = MenuItemForm(instance=item)
    
    context = {'form': form, 'item': item}
    return render(request, 'menu/dashboard/menuitem_form.html', context)


@role_required('fb')
@login_required
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return redirect('menu_item_list')
    
    context = {'item': item}
    return render(request, 'menu/dashboard/menuitem_confirm_delete.html', context)


@role_required('fb')
@login_required
def main_category_list(request):
    main_categories = MainCategory.objects.all()
    context = {'main_categories': main_categories}
    return render(request, 'menu/dashboard/maincategory_list.html', context)


@role_required('fb')
@login_required
def main_category_create(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Main category created successfully!')
            return redirect('main_category_list')
    else:
        form = MainCategoryForm()
    
    context = {'form': form}
    return render(request, 'menu/dashboard/maincategory_form.html', context)


@role_required('fb')
@login_required
def main_category_update(request, pk):
    main_category = get_object_or_404(MainCategory, pk=pk)
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, instance=main_category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Main category updated successfully!')
            return redirect('main_category_list')
    else:
        form = MainCategoryForm(instance=main_category)
    
    context = {'form': form, 'main_category': main_category}
    return render(request, 'menu/dashboard/maincategory_form.html', context)


@role_required('fb')
@login_required
def main_category_delete(request, pk):
    main_category = get_object_or_404(MainCategory, pk=pk)
    if request.method == 'POST':
        main_category.delete()
        messages.success(request, 'Main category deleted successfully!')
        return redirect('main_category_list')
    
    context = {'main_category': main_category}
    return render(request, 'menu/dashboard/maincategory_confirm_delete.html', context)


@role_required('fb')
@login_required
def category_list(request):
    categories = Category.objects.select_related('main_category').all()
    context = {'categories': categories}
    return render(request, 'menu/dashboard/category_list.html', context)


@role_required('fb')
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'menu/dashboard/category_form.html', context)


@role_required('fb')
@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'category': category}
    return render(request, 'menu/dashboard/category_form.html', context)


@role_required('fb')
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    context = {'category': category}
    return render(request, 'menu/dashboard/category_confirm_delete.html', context)


@role_required('fb')
@login_required
def tag_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'menu/dashboard/tag_list.html', context)


@role_required('fb')
@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('tag_list')
    else:
        form = TagForm()
    
    context = {'form': form}
    return render(request, 'menu/dashboard/tag_form.html', context)


@role_required('fb')
@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    
    context = {'form': form, 'tag': tag}
    return render(request, 'menu/dashboard/tag_form.html', context)


@role_required('fb')
@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tag_list')
    
    context = {'tag': tag}
    return render(request, 'menu/dashboard/tag_confirm_delete.html', context)