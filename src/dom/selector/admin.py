from django.contrib import admin
from dom.selector.models import Card
from dom.selector.models import Set


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'cardid', 'name', 'ename', 'set', 'cost', 'potion', 'vp',\
                    'action', 'coin', 'draw', 'buy', 'attack', 'reaction', 'text')


class SetAdmin(admin.ModelAdmin):
    list_display = ('id', 'setid', 'defaulton', 'name', 'ename')


admin.site.register(Card, CardAdmin)
admin.site.register(Set, SetAdmin)


