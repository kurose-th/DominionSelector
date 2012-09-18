# -*- coding: utf-8 -*-
from django import forms

from dom.selector.models import Set


class SelectorForm(forms.Form):

    #tmplist = [(i.id, i.name) for i in Set.objects.all()]
    items = []
    initlist = []
    for i in Set.objects.all():
        items.append((i.id,i.name))
        if i.defaulton:
            initlist.append(i.id)
    setfilter = forms.MultipleChoiceField(choices=items, widget=forms.CheckboxSelectMultiple,\
                                        label=u"使用セット", required=False, initial=initlist)

    items = [(0,'0コスト'), (2,'2コスト'), (3,'3コスト'), (4,'4コスト'), (5,'5コスト'), (6,'6コスト'), (7,'7コスト'), (8,'8コスト')]
    costfilter = forms.MultipleChoiceField(choices=items, widget=forms.CheckboxSelectMultiple,\
                                           label=u"特定コストのみ使用", required=False)

    number = forms.BooleanField(label = u"2セット同時生成", required=False)

    potionfilter = forms.BooleanField(label = u"ポーションカード非使用", required=False)

    items = [(0,u"なし"), (1,u"財宝オンリー"), (2,u"勝利点オンリー"), (3,u"アクションオンリー"),\
            (4,u"アタックカードオンリー"), (5,u"リアクションオンリー")]
    typefilter = forms.ChoiceField(label = u"種類別フィルター", choices=items, required=False)

    items = [(0,u"なし"), (1,u"アクション+1以上"), (2,u"アクション+2以上"), (3,u"ドロー+1以上"), (4,u"ドロー+2以上"),\
             (5,u"ドロー+3以上"), (6,u"仮想コイン+1以上"), (7,u"仮想コイン+2以上"), (8,u"購入+1以上"), (9,u"キャントリップ"),\
             (10,u"アクション/ドロー枯渇"), (11,u"act/draw/coin/buy枯渇")]
    effectfilter = forms.ChoiceField(label = u"特殊フィルター", choices=items, required=False)

    englishfilter = forms.BooleanField(label = u"英語で出力", required=False)


