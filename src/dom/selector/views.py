# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.csrf.middleware import csrf_exempt

from dom.selector.forms import SelectorForm
from dom.selector.models import Card

import random

def SupplyGenerate(data, n):
    #セットフィルター
    c = Card.objects.filter(set__in = data['setfilter'])

    #返り値
    #1:カード名
    #2:セット名
    #3:カードコスト
    #4:追記（例：災いカード）
    #5:セットid（ソートに必要っぽい）
    #6:カードid

    def ReturnSupplyList(tmpdata, n, description):
        if(data['englishfilter']):
            name = tmpdata[n].ename
            setname = tmpdata[n].set.ename
        else:
            name = tmpdata[n].name
            setname = tmpdata[n].set.name
        return([name, setname, tmpdata[n].cost, description, tmpdata[n].set.setid, tmpdata[n].cardid])


    #コストフィルター
    if data['costfilter']:
        c = c.filter(cost__in = data['costfilter'])

    #ポーションフィルター
    if data['potionfilter']:
        c = c.filter(potion = 0)

    #色々フィルター
    foo = int(data['typefilter'])
    if   (foo == 1):
        c = c.exclude(coin = 0).filter(action = 0)
    elif (foo == 2):
        c = c.exclude(vp = 0)
    elif (foo == 3):
        c = c.exclude(action = 0)
    elif (foo == 4):
        c = c.filter(attack = True)
    elif (foo == 5):
        c = c.filter(reaction = True)

    #特殊フィルター
    bar = int(data['effectfilter'])
    if   (bar == 1):#act+1
        c = c.exclude(action = 0).exclude(action = 1)
    elif (bar == 2):#act+2
        c = c.exclude(action = 0).exclude(action = 1).exclude(action = 2)
    elif (bar == 3):#draw+1
        c = c.exclude(draw = 0).exclude(draw = -1)
    elif (bar == 4):#draw+2
        c = c.exclude(draw = 0).exclude(draw = 1).exclude(draw = -1)
    elif (bar == 5):#draw+3
        c = c.exclude(draw = 0).exclude(draw = 1).exclude(draw = 2).exclude(draw = -1)
    elif (bar == 6):#coin+1
        c = c.exclude(action = 0).exclude(coin = 0)
    elif (bar == 7):#coin+2
        c = c.exclude(action = 0).exclude(coin = 0).exclude(coin = 1)
    elif (bar == 8):#buy+1
        c = c.exclude(buy = 0)
    elif (bar == 9):#cantrip
        c = c.filter(action = 2).filter(draw = 1)
    elif (bar == 10):# !(draw and action)
        c = c.filter(action = 1).filter(draw = 0)
    elif (bar == 11):# !(draw and action and coin and buy)
        c = c.filter(action = 1).filter(draw = 0).filter(coin = 0).filter(buy = 0)

    tmplist = []
    supply = []
    bane = False
    #選んだセットのカードの数がサプライ総数よりも少なければErrorを吐く
    if (len(c) < n):
        return "error_card_shorted"

    for i in range(0,len(c)):
        tmplist.append(i)

    random.shuffle(tmplist)

    for i in range(0,n):
        supply.append(ReturnSupplyList(c, tmplist[i], ''))
        #魔女娘が存在するかどうか
        if(c[tmplist[i]].cardid == 125):
            bane = True

    #災いカードの処理
    if bane:
        tmp = False
        for i in range(n,len(c)):
            if (c[tmplist[i]].cost == 2 or c[tmplist[i]].cost == 3):
                if data['englishfilter']:
                    banedesc = 'Bane Card'
                else:
                    banedesc = u'災いカード'
                supply.insert(20, ReturnSupplyList(c, tmplist[i], banedesc))
                tmp = True
                break

        #魔女娘がいるのに適切な災いカードが選ばれなかったらErrorを吐く
        if (tmp == False):
            return "error_bane_card_not_generated"
    return supply


#CSRF対策を外す　基本的には消さない事
@csrf_exempt
def formview(request):
    def Sorting_Set(x, y):
        return cmp(x[4],y[4]) or cmp(x[2],y[2])

    if (request.method == "POST"):
        f = SelectorForm(request.POST)
        supply_tmp=[]
        supply = []

        #Validation
        if f.is_valid():
            if f.cleaned_data['number']:
                n = 20
            else:
                n = 10

            #魔女娘エラー対策
            #20回もやれば大丈夫じゃないかな（白目
            for i in range(0,20):
                supply_tmp.append(SupplyGenerate(f.cleaned_data, n))
                if(supply_tmp[i] != "error_bane_card_not_generated"):
                    supply = supply_tmp[i]
                    break

            if (supply == "error_card_shorted"):
                response = HttpResponse(u"Error!<br><br>サプライを生成する為のカードの種類が足りません<br>\
                                        1サプライ生成時は10種類以上、2サプライ生成時は20種類以上のカードを選択して下さい<br>")
                return response
            elif (supply == []):
                response = HttpResponse(u"Error!<br><br>災いカード云々でエラーが出ました　やり直してみてください<br>\
                                                                                            たぶん災いカードとして選べるコスト2or3のカードが余ってません")
                return response

            else:
                supply1_list = supply[0:10]
                supply2_list = supply[10:20]
                other_list = supply[20:30]
                tweet1 = ""
                tweet2 = ""
                tmpbane = [False, False]
                supply1_list.sort(Sorting_Set)
                supply2_list.sort(Sorting_Set)
                for i in range(0,10):
                    tweet1 += supply1_list[i][0] + u"+"
                    #魔女娘がいる
                    if(supply1_list[i][5] == 125):
                        tmpbane[0] = True
                #Bane Card
                if tmpbane[0]:
                    if (f.cleaned_data['number']):
                        tweet1 += u"（災いカード：" + other_list[0][0] + u"）+"
                    else:
                        tweet1 += u"（災いカード：" + supply2_list[0][0] + u"）+"

                if f.cleaned_data['number']:
                    for i in range(0,10):
                        tweet2 += supply2_list[i][0] + u"+"
                        if(supply2_list[i][5] == 125):
                            tmpbane[1] = True
                if tmpbane[1]:
                    tweet2 += u"（災いカード：" + other_list[0][0] + u"）+"

                context = {'supply1':supply1_list, 'supply2':supply2_list,\
                           'other':other_list, 'Twitter1':tweet1, 'Twitter2':tweet2}
                return direct_to_template(request, "supply.html", context)

        else:
            return HttpResponse(u"Error!<br><br>なんか正体不明でやばげなエラーが出ました<br>\
                                                                            作者に報告してください<br>f.is_valid() is not True.<br>")
    else:
        f = SelectorForm()
        context = {'form':f}
        return direct_to_template(request, "selector.html", context)


