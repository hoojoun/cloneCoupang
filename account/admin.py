"""
My module
~~~~~~~
"""

from abc import ABCMeta

from django.contrib import admin
from .models import *
from django.db.models import Count
from rangefilter.filters import DateRangeFilter
from shops.models import *
import datetime
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from .customsignal import blacklist_update


class InputFilter(admin.SimpleListFilter, metaclass=ABCMeta):
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    """
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return (),

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class ConsentCountFilter(InputFilter):
    parameter_name = 'consentsCount'
    title = 'n개의 약관에 동의한 유저'

    def queryset(self, request, queryset):
        if self.value() is not None and self.value() != '':
            if int(self.value()) > 0:
                value = self.value()
                consent_list = []
                consents = UserConsent.objects.filter(ccheck=1).values('user_id').annotate(count=Count('user_id'))
                print(consents.query)
                for consent in consents:
                    if consent['count'] >= int(value):
                        consent_list.append(consent['user_id'])
                return queryset.filter(id__in=consent_list)
        else:
            return queryset.all()


class IsSellerFilter(admin.SimpleListFilter):
    title = '판매자 또는 사용자?'
    parameter_name = 'isSeller'

    def lookups(self, request, model_admin):
        return (
            ('Y3', '판매자 보기'),
            ('N3', '판매자 빼고 보기'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Y3':
            return queryset.filter(username__contains="S_")
        elif value == 'N3':
            return queryset.filter(username__contains="U_")
        else:
            return queryset.all()


class UserConsentInline(admin.TabularInline):
    model = UserConsent
    extra = 0


class CustomSellerInline(admin.TabularInline):
    model = CustomSeller
    extra = 0


# @admin.register(CustomUser)
class CustomUserAdmin(SimpleHistoryAdmin):
    def consent_count(self, obj):
        return UserConsent.objects.filter(user_id=obj, ccheck=1).count()

    def is_seller(self, obj):
        return 1 if obj.username.find("S_") != -1 else 0

    model = CustomUser
    inlines = [UserConsentInline, CustomSellerInline]
    fields = ['username', 'password', 'name', 'phone', 'date_joined', 'last_login', 'activate']
    list_display = ['id', 'username', 'date_joined', 'consent_count', 'is_seller', 'activate', ]
    list_display_links = ['id', 'username']
    list_filter = (IsSellerFilter, ConsentCountFilter, ('date_joined', DateRangeFilter))

    def get_rangefilter_created_at_default(self, request):
        return (datetime.date.today, datetime.date.today)

    def get_rangefilter_created_at_title(self, request, field_path):
        return 'custom title'


class UserConsentAdmin(admin.ModelAdmin):
    model = UserConsent
    list_display = ['user', 'cid', 'ccheck']


class ProductAdmin(admin.ModelAdmin):
    model = Products
    list_display = ['name', 'price', 'seller']


# Register your models here.

class ConsentAdmin(admin.ModelAdmin):
    model = Consent
    list_display = ['id', 'title', 'isUser', 'activate']
    list_filter = ['isUser', 'activate']


class ConsentAdmin(admin.ModelAdmin):
    model = Consent
    list_display = ['id', 'title', 'isUser', 'activate']
    list_filter = ['isUser', 'activate']


def make_blacklist(modeladmin, request, queryset):
    for report in list(queryset):
        report.reported_user.activate = False
        report.reported_user.save()
        blacklist_update.send(sender=report.reported_user)


make_blacklist.short_description = "blacklist 만들기"


def no_blacklist(modeladmin, request, queryset):
    for report in list(queryset):
        report.reported_user.activate = True
        report.reported_user.save()
        blacklist_update.send(sender=report.reported_user)


no_blacklist.short_description = "blacklist 풀기"


class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ['id', 'custom_field', 'reported_user', 'content']
    actions = [make_blacklist, no_blacklist]

    @staticmethod
    def custom_field(obj):
        url = obj.product.id
        name = obj.product.name
        return format_html('<a href={}>' + name + '</a>', '/product/' + str(url))


class BlackListHistoryAdmin(admin.ModelAdmin):
    model = BlackListHistory
    list_display = ['id', 'blacklist', 'content', 'date']


admin.site.register(Consent, ConsentAdmin)
admin.site.register(UserConsent, UserConsentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(BlackListHistory, BlackListHistoryAdmin)
