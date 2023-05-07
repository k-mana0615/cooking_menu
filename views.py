from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
import json
import requests
from time import sleep
from .models import RakuRecipeCategoryLarge
from .models import RakuRecipeCategoryMedium
from .models import RakuRecipeCategorySmall
from .models import RakuRecipeMenu
from django.db.models import Q
from django.http.response import JsonResponse


def index(request):
    return render(request, 'cooking_menu/index.html')


def list(request, num=1):
    #POSTの時の遷移先
    if request.POST:
        #判定用として、大中小それぞれのPOSTを変数に格納する
        large_category_id = request.POST.getlist('large_category_id')
        medium_category_id = request.POST.getlist('medium_category_id')
        small_category_id = request.POST.getlist('small_category_id')
        large_flag = False
        medium_flag = False
        small_flag = False
        #いずれも空のリストの場合
        if large_category_id == [] and medium_category_id == [] and small_category_id == []:
            category_id = []
        #大カテゴリにて選択されていた場合
        if large_category_id != []:
            category_id = large_category_id
            large_flag = True
        #中カテゴリにて選択されていた場合
        if medium_category_id != []:
            category_id = medium_category_id
            medium_flag = True
        #小カテゴリにて選択されていた場合
        if small_category_id != []:
            category_id = small_category_id
            small_flag = True
        #リストが空じゃなければ（一つ以上の選択があれば）クエリを実行する
        if category_id != []:
            category_count = len(category_id)
            #選択された項目が単数の時
            if category_count == 1:
                #大カテゴリから遷移してきた時
                if large_flag == True:
                    recipe = RakuRecipeMenu.objects.filter(recipe_category_id__startswith=str(category_id[0]) + '-')
                #中カテゴリから遷移してきた時
                elif medium_flag == True:
                    recipe = RakuRecipeMenu.objects.filter(recipe_category_id__contains='-' + str(category_id[0]) + '-')
                #小カテゴリから遷移してきた時
                elif small_flag == True:
                    recipe = RakuRecipeMenu.objects.filter(recipe_category_id__endswith='-' + str(category_id[0]))
            #選択された項目が複数の時
            elif category_count >= 1:
                #複数条件を作成（ここではAND条件となる）
                #大カテゴリから遷移してきた時
                if large_flag == True:
                    queries = [Q(recipe_category_id__startswith=str(i) + '-') for i in category_id]
                #中カテゴリから遷移してきた時
                elif medium_flag == True:
                    queries = [Q(recipe_category_id__contains='-' + str(i) + '-') for i in category_id]
                #小カテゴリから遷移してきた時
                elif small_flag == True:
                    queries = [Q(recipe_category_id__endswith='-' + str(i)) for i in category_id]
                #作成した条件をORに変換する
                query = queries.pop()
                for item in queries:
                    query |= item
                #複数のOR条件を使用し、データ抽出する
                recipe = RakuRecipeMenu.objects.filter(query)
            #クエリ結果を変数にセットする
            page = Paginator(recipe, 3)
            params = {
                'recipe': recipe,
#                'recipe_check': page.get_page(num),
            }
            #テンプレートに渡す（チェックボックス選択時）
            return render(request, 'cooking_menu/list.html', params)
        else:
            #テンプレートに渡す（チェックボックス非選択時）
            recipe = RakuRecipeMenu.objects.all().order_by('id')
            page = Paginator(recipe, 3)
            params = {
                'recipe': page.get_page(num),
            }
            return render(request, 'cooking_menu/list.html', params)
    else:
        #テンプレートに渡す（アドレス直叩き）
        recipe = RakuRecipeMenu.objects.all().order_by('id')
        page = Paginator(recipe, 3)
        params = {
            'recipe': page.get_page(num),
        }
        return render(request, 'cooking_menu/list.html', params)


def find(request, num=1):
    material = request.POST.get('material')
    #テキスト検索された時の処理
    if request.POST:
#        if request.POST.get('material') == '':
        if material == '':
            recipe = RakuRecipeMenu.objects.all().order_by('id')
            page = Paginator(recipe, 3)
        else:
#            find_text = request.POST.get('material')
            recipe = RakuRecipeMenu.objects.filter(recipe_material__0=material)
            page = Paginator(recipe, 3)
        params = {
#            'recipe': page.get_page(num),
            'recipe': recipe,
        }
    else:
        params = {
            'recipe': '',
        }
    return render(request, 'cooking_menu/find.html', params)


def large_category(request):
    model = RakuRecipeCategoryLarge.objects.all()
    params = {
        'model': model,
    }
    return render(request, 'cooking_menu/large_category.html', params)


def medium_category(request):
    model = RakuRecipeCategoryMedium.objects.all()
    params = {
        'model': model,
    }
    return render(request, 'cooking_menu/medium_category.html', params)


def small_category(request):
    model = RakuRecipeCategorySmall.objects.all()
    params = {
        'model': model,
    }
    return render(request, 'cooking_menu/small_category.html', params)


def favorite(request, num=1):
    recipe = RakuRecipeMenu.objects.all().order_by('id')
    page = Paginator(recipe, 10)
    params = {
        'recipe': page.get_page(num),
    }
    return render(request, 'cooking_menu/favorite.html', params)


def favorite_confirm(request):
    #初期化処理
    recipe = ''
    delete_recipe = ''
    view_update_flag = False
    view_delete_update_flag = False
    #POSTの時の遷移先
    if request.POST:
        #①お気に入り登録されるリストをqueries変数に格納し、データを取得する
        #update_query変数とupdate_queries変数の初期化
        update_query = ''
        update_queries = []
        #選択されたお気に入りフラグのPOSTデータ
        favorite_flag = request.POST.getlist('favorite_flag')
        #update_queries変数の作成
        for f_id in favorite_flag:
            #現在DBに登録されているお気に入りフラグの状態を取得する
            now_favorite_after_favorite_flag = RakuRecipeMenu.objects.filter(id=f_id).values_list('favorite_flag', flat=True)
            #現在お気に入りフラグがFalseで、favorite_flagの値があるならお気に入り登録対象
            if now_favorite_after_favorite_flag[0] == False:
                #ここではAND条件となる
                update_queries.append(Q(id=f_id))                
        #作成した条件をORに変換する
        if len(update_queries) >= 1:
            update_query = update_queries.pop()
            for item in update_queries:
                update_query |= item
            #複数のOR条件を使用し、recipe変数に格納する
            recipe = RakuRecipeMenu.objects.filter(update_query)
            view_update_flag = True
            
        
        #②お気に入り登録から削除されるリストをdelete_queries変数に格納し、データを取得する
        #delete_query変数とdelete_queries変数の初期化
        delete_query = ''
        delete_queries = []
        #現在DBに登録されているお気に入りフラグの状態
        now_favorite_flag = request.POST.getlist('now_favorite_flag')
        for nf_id in now_favorite_flag:
            #現在DBに登録されているお気に入りフラグの状態を取得する
            now_favorite_after_delete_flag = RakuRecipeMenu.objects.filter(id=nf_id).values_list('favorite_flag', flat=True)
            #delete_flagの初期化(更新対象の判定フラグ)
            delete_flag = True
            #現在お気に入りフラグがTrueだが、favorite_flagの値が無いデータは、お気に入り削除されるデータ
            if now_favorite_after_delete_flag[0] == True:
                #登録予定のデータ(f_id)と不一致なら削除対象となる
                for f_id in favorite_flag:
                    #f_idにあれば、True→Trueのレコードのため、delete_flagはFalse(お気に入り登録対象)とする
                    if f_id == nf_id:
                        delete_flag = False
                #delete_flagがTrueのままだったので、削除対象とする
                if delete_flag == True:
                    #ここではAND条件となる
                    delete_queries.append(Q(id=nf_id))
        #作成した条件をORに変換する
        if len(delete_queries) >= 1:
            delete_query = delete_queries.pop()
            for item in delete_queries:
                delete_query |= item
            #複数のOR条件を使用し、delete_recipe変数に格納する
            delete_recipe = RakuRecipeMenu.objects.filter(delete_query)
            view_delete_update_flag = True
            

        params = {
            'recipe': recipe,
            'delete_recipe': delete_recipe,
            'view_update_flag': view_update_flag,
            'view_delete_update_flag': view_delete_update_flag,
        }

        if view_update_flag == False and view_delete_update_flag == False:
            params = {
                'message': 'お気に入り登録の変更がありません',
            }
            return render(request, 'cooking_menu/favorite_confirm.html', params)
        else:
            return render(request, 'cooking_menu/favorite_confirm.html', params)


def favorite_result(request):
    #選択するか分からないので、初期化処理
    recipe = ''
    delete_recipe = ''
    #①お気に入り登録されるリストをupdate
    favorite_flag = request.POST.getlist('favorite_flag')
    for i in favorite_flag:
        RakuRecipeMenu.objects.filter(id=str(i)).update(favorite_flag=True)
    favorite_count = len(favorite_flag)
    #選択された項目が単数の時
    if favorite_count == 1:
        recipe = RakuRecipeMenu.objects.filter(id=str(favorite_flag[0]))
    #選択された項目が複数の時
    elif favorite_count >= 1:
        #複数条件を作成（ここではAND条件となる）
        #大カテゴリから遷移してきた時
        queries = [Q(id=str(i)) for i in favorite_flag]
        #作成した条件をORに変換する
        query = queries.pop()
        for item in queries:
            query |= item
        #複数のOR条件を使用し、データ抽出する
        recipe = RakuRecipeMenu.objects.filter(query)

    #②お気に入りから削除されるリストをupdate
    delete_favorite_flag = request.POST.getlist('delete_favorite_flag')
    for i in delete_favorite_flag:
        RakuRecipeMenu.objects.filter(id=str(i)).update(favorite_flag=False)
    delete_favorite_count = len(delete_favorite_flag)
    #選択された項目が単数の時
    if delete_favorite_count == 1:
        delete_recipe = RakuRecipeMenu.objects.filter(id=str(delete_favorite_flag[0]))
    #選択された項目が複数の時
    elif delete_favorite_count >= 1:
        #複数条件を作成（ここではAND条件となる）
        queries = [Q(id=str(i)) for i in delete_favorite_flag]
        #作成した条件をORに変換する
        query = queries.pop()
        for item in queries:
            query |= item
        #複数のOR条件を使用し、データ抽出する
        delete_recipe = RakuRecipeMenu.objects.filter(query)

    #テンプレートに渡し、更新結果を表示する
    params = {
        'recipe': recipe,
        'delete_recipe': delete_recipe,
    }
    #テンプレートに渡す（チェックボックス選択時）
    return render(request, 'cooking_menu/favorite_result.html', params)
    

def favorite_js(request, num=1):
    recipe = RakuRecipeMenu.objects.all()
    page = Paginator(recipe, 10)
    params = {
        'recipe': page.get_page(num),
    }
    
    #チェックボックスの動きに応じた値取得
    checked_id = request.POST.get('value_id')
    checked_favorite_flag = request.POST.get('value_favorite_flag')

    #チェックボックスが操作された際、JSファイルで送信された真偽値をpythonの真偽値に反映させ、updateクエリを実行する
    if checked_id is not None:
        if checked_favorite_flag == 'true':
            checked_favorite_flag = True
        else:
            checked_favorite_flag = False
        RakuRecipeMenu.objects.filter(id=str(checked_id)).update(favorite_flag=checked_favorite_flag)
        #以下のようにすれば、favorite_js.jsからajax送信されたPOSTデータを確認できる
        #print(checked_id)
    return render(request, 'cooking_menu/favorite_js.html', params)


def favorite_page(request, num=1):
    recipe = RakuRecipeMenu.objects.filter(favorite_flag=True).order_by('id')
    page = Paginator(recipe, 5)
    params = {
        'recipe': page.get_page(num),
    }
    return render(request, 'cooking_menu/favorite_page.html', params)
