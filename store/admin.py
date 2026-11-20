from django.contrib import admin
from .models import Product, Attribute, AttributeValue, ProductVariant, Order


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'created_at')
    list_filter = ('category',)
    inlines = [ProductVariantInline]


admin.site.register(ProductVariant)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_paid', 'created')
    list_filter = ('created',)
    readonly_fields = ('first_name', 'last_name', 'email', 'address', 'city', 'total_paid', 'created')