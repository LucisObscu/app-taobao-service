from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
import json
import requests
from getdata.models import (User_Info,Prohibition,Naver_Product,
                            Sourcing,Sourcing_Product,Sourcing_Option_Category,Sourcing_Option_Deep_Category,
                            Main_Images,Content_Images,
                            Product,Problem_Product,Secret_Key)
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime,timedelta
from django.core import serializers
from django.forms.models import model_to_dict
#from getdata.serializers import SourcingSerializer,Sourcing_ProductSerializer,Sourcing_OptionSerializer
#from rest_framework import viewsets
from pytz import timezone
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        encoded_object = str(obj)
        return encoded_object
import math
import traceback


def sum_pk(pk_data):
    data = pk_data['fields']
    data['pk'] = pk_data['pk']
    return data



def sourcing_delect(request):
    data = {
        "code": 200,
        "msg":"업로드 완료",
    }
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    Sourcing.objects.filter(id__in = [i['pk'] for i in dt],admin_email=admin_email).delete() 
    
    return HttpResponse(json.dumps(data), content_type = "application/json")



def sourcing_update(request):
    data = {
        "code": 200,
        "msg":"업로드 완료",
    }
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    
    product_settings = dt['product_settings']
    all_op_list = dt['all_op_list']
    product_info = dt['product_info']
    status = dt['status']
    
    sourcing_one = Sourcing.objects.get(id = product_info['pk'],admin_email=admin_email)
    sourcing_one.org_title = product_info['org_title']
    sourcing_one.tag = product_info['tag']
    sourcing_one.change_thumbnail = product_info['change_thumbnail']    
    sourcing_one.status = status
    sourcing_one.save()
    
    one = Sourcing_Product.objects.get(id = product_settings['pk'])
    one.margin = product_settings['margin']
    one.isClothes = product_settings['isClothes']
    one.isShoes = product_settings['isShoes']
    one.weight = product_settings['weight']
    one.weightPrice = product_settings['price']
    one.memo = product_settings['memo']
    one.save()
    for op_list in all_op_list:
        for op in op_list:
            one_op = Sourcing_Option_Category.objects.get(id=op['pk'],sourcing_id=op['sourcing_id'])
            one_op.ctg_korTypeName = op['ctg_korTypeName']
            one_op.korTypeName = op['korTypeName']
            one_op.image = op['image']
            one_op.select = op['select']
            one_op.save()
    

    
    

    return HttpResponse(json.dumps(data), content_type = "application/json")



def sourcing_upload(request):
    
    dt = json.loads(request.body.decode('utf-8'))
    email = request.session['email']
    admin_email = request.session['admin_email']
    #Sourcing.objects.create()
    data = {
        "code": 200,
        "msg":"업로드 완료",
        "data":None
    }
    Sourcing.objects.create(item_id='',org_title=dt['title'],constructor=email,manager=email,change_thumbnail=dt['sub_thumbnail'],status=0,
                            date=datetime.now(timezone('Asia/Seoul')).replace(microsecond=0),cannel_id=dt['cannel_id'],product_id=dt['product_id'],admin_email=admin_email,tag='')

    return HttpResponse(json.dumps(data), content_type = "application/json")

def get_sourcing_data(one_sourcing):
    sourcing = [sum_pk(i) for i in json.loads(serializers.serialize("json", Sourcing.objects.filter(id=one_sourcing.id)))]
    sourcing_pr = [sum_pk(i) for i in json.loads(serializers.serialize("json", Sourcing_Product.objects.filter(sourcing_id=one_sourcing)))]
    sourcing_op_ctg = [sum_pk(i) for i in json.loads(serializers.serialize("json", Sourcing_Option_Category.objects.filter(sourcing_id=one_sourcing)))]
    sourcing_op_deep_ctg = [sum_pk(i) for i in json.loads(serializers.serialize("json", Sourcing_Option_Deep_Category.objects.filter(sourcing_id=one_sourcing)))]
    main_img = [sum_pk(i) for i in json.loads(serializers.serialize("json", Main_Images.objects.filter(sourcing_id=one_sourcing)))]
    cont_img = [sum_pk(i) for i in json.loads(serializers.serialize("json", Content_Images.objects.filter(sourcing_id=one_sourcing)))]
    return {'sourcing':sourcing,'sourcing_pr':sourcing_pr,'sourcing_op_ctg':sourcing_op_ctg,'sourcing_op_deep_ctg':sourcing_op_deep_ctg,'cont_img':cont_img,'main_img':main_img}
    

def sourcing_product_delete(request):
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    pk = dt['pk']
    for one_sourcing in Sourcing.objects.filter(id=pk,admin_email=admin_email):
        [i.delete() for i in Sourcing_Product.objects.filter(sourcing_id=one_sourcing)]
        [i.delete() for i in Sourcing_Option_Category.objects.filter(sourcing_id=one_sourcing)]
        [i.delete() for i in Sourcing_Option_Deep_Category.objects.filter(sourcing_id=one_sourcing)]
        [i.delete() for i in Main_Images.objects.filter(sourcing_id=one_sourcing)]
        [i.delete() for i in Content_Images.objects.filter(sourcing_id=one_sourcing)]
        one_sourcing.item_id = ''
    data = {
        "code": 200,
        "msg":"삭제 완료",
    }    
    return HttpResponse(json.dumps(data), content_type = "application/json")   
    
def sourcing_product_confirm(request):
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    pk_id = dt['pk']
    one = Sourcing.objects.get(id=pk_id,admin_email=admin_email)
    data = {
        "code": 200,
        "msg":"업로드 완료",
        "data":None
    }

    data['data'] = get_sourcing_data(one)
    return HttpResponse(json.dumps(data), content_type = "application/json")   


    

def sourcing_product_upload(request):
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    pk_id = dt['pk']
    data = dt['data']
    item_id = data['item_id']
    one = Sourcing.objects.get(id=pk_id,admin_email=admin_email)
    one.item_id=item_id
    try:
        one.change_thumbnail = data['main_imgs'][0]
    except:
        pass
    one.save()
    Sourcing_Product.objects.create(title=data['title'], sourcing_id=one, korTitle=data['ko_title'],
                                    margin=10, weightPrice=6000,weight=1, memo='', brand='기타')
    for i in data['main_imgs']:
        Main_Images.objects.create(sourcing_id=one, src=i)
    for i in data['detail_imgs']:
        Content_Images.objects.create(sourcing_id=one, src=i)
    
    for i in data['sku_props']:
        pid = i['pid']
        ctg_name = i['prop_name']
        ctg_korTypeName = i['ko_name']
        if i['values']:
            for k in i['values']:
                name = k['name']
                vid = k['vid']
                korTypeName = k['ko_name']
                imageUrl = ''
                try:
                    imageUrl = k['imageUrl']
                except:
                    pass
                Sourcing_Option_Category.objects.create(sourcing_id=one, pid=pid, ctg_name=ctg_name, ctg_korTypeName=ctg_korTypeName,
                                                        vid=vid, name=name, korTypeName=korTypeName, image=imageUrl)
        else:
            Sourcing_Option_Category.objects.create(sourcing_id=one, pid=pid, ctg_name=ctg_name, ctg_korTypeName=ctg_korTypeName,
                                                    vid='', name='', korTypeName='', image='')
    for i in data['skus']:
        ids = i['props_ids']
        
        sale_price = i['sale_price']
        origin_price = i['origin_price']
        if i['origin_price']:
            origin_price = float(i['origin_price'])
        else:
            origin_price = sale_price
        sale_price = float(sale_price)
        skuid = i['skuid']
        stock = i['stock']
        Sourcing_Option_Deep_Category.objects.create(sourcing_id=one, ids=ids, sale_price=sale_price, origin_price=origin_price, skuid=skuid, stock=stock)
        
    data = {
        "code": 200,
        "msg":"업로드 완료"
    }        
        
    return HttpResponse(json.dumps(data), content_type = "application/json")   
def naver_page(request):
    admin_email = request.session['admin_email']
    email = request.session['email']
    dt = json.loads(request.body.decode('utf-8'))
    page = dt['page']
    option = dt['option']
    
    goods_day = option["goods_day"]
    three_day = option["three_day"]
    six_mon_s = option["six_mon_s"]
    six_mon_e = option["six_mon_e"]
    review_s = option["review_s"]
    review_e = option["review_e"]
    price_min = option["price_min"]
    price_max = option["price_max"]
    problem_product = option["problem_product"]
    status = option["status"]
    one_user_info = User_Info.objects.get(email=email,admin_email=admin_email)
    
    one_user_info.goods_day = goods_day
    one_user_info.three_day = three_day
    one_user_info.six_mon_s = six_mon_s
    one_user_info.six_mon_e = six_mon_e
    one_user_info.review_s = review_s
    one_user_info.review_e = review_e
    one_user_info.price_min = price_min
    one_user_info.price_max = price_max
    one_user_info.problem_product = problem_product
    one_user_info.status = ','.join(status)
    one_user_info.save()
    
    d_day = datetime.now(timezone('Asia/Seoul')) - timedelta(goods_day)
    d_day = datetime(d_day.year,d_day.month,d_day.day)
    naver_product_list = Naver_Product.objects.filter(admin_email=admin_email,
                                             six_mon__gte=six_mon_s,six_mon__lte=six_mon_e,
                                             review__gte=review_s,review__lte=review_e,
                                             price_sum_delivery__gte=price_min,price_sum_delivery__lte=price_max,
                                             date__gte=d_day,three_day=three_day).order_by('-date')
    
    
    cut_naver_product_list = []
    sourcing_status_list = []
    problem_product_list = []
    for one in naver_product_list:
        cannel_id = one.cannel_id
        product_id = one.product_id
        problem_list = Problem_Product.objects.filter(product_num='{0}-{1}'.format(cannel_id, product_id))

        status_list = [i.status for i in Sourcing.objects.filter(admin_email=admin_email,cannel_id=cannel_id, product_id=product_id)]
        status_dt = {i:status_list.count(i) for i in range(4) if status_list.count(i) != 0}
        if status:
            sw = False
            for i in status:
                try:
                    if status_dt[int(i)] != 0:
                        sw = True
                        break
                except:
                    pass
            if sw:
                if not (problem_list and problem_product):
                    cut_naver_product_list.append(one)
                    sourcing_status_list.append(status_dt)
                    if problem_list:
                        problem_product_list.append(True)
                    else:
                        problem_product_list.append(False)
            
        else:
            if not (problem_list and problem_product):
                cut_naver_product_list.append(one)
                sourcing_status_list.append(status_dt)
                if problem_list:
                    problem_product_list.append(True)
                else:
                    problem_product_list.append(False)
    
    top = len(cut_naver_product_list)
    cut = 10
    start = (cut*page)
    end = start - cut
    if page == 0:
        naver_list = []
    else:
        naver_list = []
        naver_page_list = json.loads(serializers.serialize("json", cut_naver_product_list[end:start]))
        sourcing_status_list = sourcing_status_list[end:start]
        problem_blo_list = problem_product_list[end:start]
        for index,v in enumerate(naver_page_list):
            one = v['fields']
            one['pk'] = v['pk']
            one['status'] = sourcing_status_list[index]
            one['problem'] = problem_blo_list[index]
            naver_list.append(one)
    data = {
        "code": 200,
        "msg":"업로드 완료",
        "data":{'list':naver_list,'count':top,'cut':10,'page':page}
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")


def problem_set(request):
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    product_num=dt['all_id']
    problem_list = Problem_Product.objects.filter(product_num=product_num,admin_email=admin_email)
    if dt['problem_check']:
        if not problem_list:
            Problem_Product.objects.create(admin_email=admin_email, product_num=product_num)
    else:
        if problem_list:
            problem_list.delete()
    
    data = {
        "code": 200,
        "msg":"업로드 완료"
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")    

def sourcing_page(request):
    admin_email = request.session['admin_email']
    dt = json.loads(request.body.decode('utf-8'))
    
    date_s = dt['data']['date']['date_s']
    date_e = dt['data']['date']['date_e']
    constructor_email = dt['data']['constructor_email']
    manager_email = dt['data']['manager_email']
    status = dt['data']['status']
    date_s = datetime.strptime(date_s, '%Y-%m-%d')
    date_e = datetime.strptime(date_e, '%Y-%m-%d') + timedelta(days=1)
    if constructor_email == 0 and manager_email == 0:
        if status:
            sourcing_page_list = Sourcing.objects.filter(status__in=status,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
        else:
            sourcing_page_list = Sourcing.objects.filter(admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
    else:
        if constructor_email != 0 and manager_email != 0:
            if status:
                sourcing_page_list = Sourcing.objects.filter(status__in=status,constructor=constructor_email,manager=manager_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
            else:
                sourcing_page_list = Sourcing.objects.filter(constructor=constructor_email,manager=manager_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
        elif  constructor_email == 0:
            if status:
                sourcing_page_list = Sourcing.objects.filter(status__in=status,manager=manager_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
            else:
                sourcing_page_list = Sourcing.objects.filter(manager=manager_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
        else:
            if status:
                sourcing_page_list = Sourcing.objects.filter(status__in=status,constructor=constructor_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
            else:
                sourcing_page_list = Sourcing.objects.filter(constructor=constructor_email,admin_email=admin_email,date__range=[date_s, date_e]).order_by('-date')
        
        
    
    page = dt['page']
    top = sourcing_page_list.count()
    cut = 10
    start = (cut*page)
    end = start - cut
    if page == 0:
        naver_list = []
    else:
        naver_list = []
        for i in json.loads(serializers.serialize("json", sourcing_page_list[end:start])):
            one = i['fields']
            one['pk'] = i['pk']
            naver_list.append(one)
    data = {
        "code": 200,
        "msg":"업로드 완료",
        "data":{'list':naver_list,'count':top,'cut':10,'page':page}
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")

def manager_update(request):
    dt = json.loads(request.body.decode('utf-8'))
    admin_email = request.session['admin_email']
    email = dt['email']
    
    pk_list = [i['pk'] for i in dt['pk_list']]
    user = User_Info(email=email, admin_email=admin_email)
    sourcing_list = Sourcing.objects.filter(id__in = pk_list,admin_email=admin_email)
    for i in sourcing_list:
        i.manager = email
        i.save()
    
    data = {
        "code": 200,
        "msg":"업로드 완료",
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")    

def naver_all_upload(request):
    data = {
        "code": 200,
        "msg": "업로드 완료"
    }
    lst2 = ['title', 'price', 'delivery', 'price_sum_delivery', 'org_thumbnail', 'sub_thumbnail',
            'img_detailed', 'cannel_id', 'product_id', 'date', 'img_width', 'img_height', 'three_day',
            'six_mon', 'review', 'review_score']
    try:
        dt = json.loads(request.body.decode('utf-8'))
        if dt != []:
            if not set(lst2).difference(list(dt[0].keys())):
                admin = request.session['admin']
                email = request.session['email']
                admin_email = request.session['admin_email']
                if admin:
                    Naver_Product.objects.filter(admin_email=admin_email).delete()
                    for i,v in enumerate(dt):
                        dt[i]["date"] = datetime.strptime(dt[i]["date"], '%Y-%m-%d %H:%M:%S')
                        dt[i]["admin_email"] = email
                    for i in dt:
                        print('===============')
                        for k in i.keys():
                            print('{0} : {1}'.format(k,i[k]))
                        print('===============')

                        Naver_Product.objects.create(admin_email=i['admin_email'],title=i['title'], price=i['price'], delivery=i['delivery'], price_sum_delivery=i['price_sum_delivery'],
                                                     org_thumbnail=i['org_thumbnail'],sub_thumbnail=i['sub_thumbnail'], img_detailed=i['img_detailed'],cannel_id=i['cannel_id'],
                                                     product_id=i['product_id'], date=i['date'], img_width=i['img_width'],img_height=i['img_height'], six_mon=i['six_mon'],
                                                     review=i['review'],review_score=i['review_score'],three_day=i['three_day'])
                else:
                    data["code"] = 201
                    data["msg"] = "관리자 권한이 없습니다"
            else:
                data["code"] = 204
                data["msg"] = "잘못된 데이터 입니다."
        else:
            data["code"] = 202
            data["msg"] = "데이터가 비어있습니다"
    except:
        data["code"] = 203
        data["msg"] = "로그인을 다시 시도해 주세요"
        data["msg"] = traceback.format_exc()
    return HttpResponse(json.dumps(data), content_type = "application/json")



def setting_save(request):
    dt = json.loads(request.body.decode('utf-8'))
    if request.session['admin']:
        admin_email = request.session['admin_email']
        email = request.session['email']
        key = dt['key']
        tax = dt['tax']
        if Secret_Key.objects.filter(admin_email=admin_email):
            one = Secret_Key.objects.get(admin_email=admin_email)
            one.key = key
            one.save()
        else:
            Secret_Key.objects.create(admin_email=admin_email,key=key)
        if User_Info.objects.filter(admin_email=admin_email,email=email):
           one = User_Info.objects.get(admin_email=admin_email,email=email)
           one.tax = tax
           one.save()
    
    data = {
        "code": 200,
        "msg":"업로드 완료"
    }    
    
    return HttpResponse(json.dumps(data), content_type = "application/json")
    
def prohibition(request):
    admin_email = request.session['admin_email']
    email = request.session['email']
    dt = json.loads(request.body.decode('utf-8'))
    if request.session['admin']:
        keyword = dt['prohihition_keyword']
        update = dt['update']
        if type(keyword) == list:
            pass
        elif type(keyword) == str:
            if update:
                try:
                    Prohibition.objects.get(admin_email=admin_email, keyword=keyword)
                except:
                    Prohibition.objects.create(email=email,admin_email=admin_email, keyword=keyword)
            else:
                try:
                    Prohibition.objects.filter(admin_email=admin_email, keyword=keyword).delete()
                except:
                    pass
    data = {
        "code": 200,
        "msg":"업로드 완료"
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")

def prohibition_list_get(request):
    admin_email = request.session['admin_email']
    
    prohibition_list = []
    
    
    for i in json.loads(serializers.serialize("json", Prohibition.objects.filter(admin_email=admin_email))):
        one = i['fields']
        one['pk'] = i['pk']
        prohibition_list.append(one)
    
    data = {
        "code": 200,
        "msg":"업로드 완료",
        "data":prohibition_list
    }
    return HttpResponse(json.dumps(data), content_type = "application/json")    
    
    

def login(request):
    print(request.session.session_key)
    
    dt = json.loads(request.body.decode('utf-8'))
    data = {'email':dt['email'],'password':dt['password']}
    text = dt['login_data']
    if text['code'] == 'SUCCESS':
        email = text['data']['email']
        nickname = text['data']['nickname']
        admin = text['data']['admin']
        if admin:
            print('관리자 계정이고')
            #관리자 계정이고
            request.session['email'] = email
            request.session['nickname'] = nickname
            request.session['admin_email'] = email
            request.session['admin'] = True
            try:
                info = User_Info.objects.get(email=email,admin=True,admin_email=email)
            except:
                info = None
            m_data = 'email={0}'.format(email)
            m_req = requests.get('https://tsnullp.herokuapp.com/seller/getStaff?'+m_data)
            m_text = m_req.json()
            if info == None:
                print('등록이 되지 않으면')
                #등록이 되지 않으면
                User_Info.objects.create(email=email, nickname=nickname,admin=True,admin_email=email)
                if m_text['code'] == 'SUCCESS':
                    print('직원 계정 등록')
                    #직원 계정 등록
                    for user in m_text['data']:
                        u_email = user['email']
                        u_nickname = user['nickname']
                        User_Info.objects.create(email=u_email, nickname=u_nickname,admin=False,admin_email=email)
                text['message'] = '로그인 성공'
                text['user_list'] = serializers.serialize("json", User_Info.objects.filter(admin_email=email))
                text['setting'] = model_to_dict(User_Info.objects.get(email=email))
                text['prohibition'] = serializers.serialize("json", Prohibition.objects.filter(admin_email=email))
                request.session['email'] = email
                request.session['nickname'] = nickname
                request.session['admin_email'] = email
                request.session['admin'] = True
                text['key'] = ''
                if Secret_Key.objects.filter(admin_email=email):
                    one = Secret_Key.objects.get(admin_email=email)
                    text['key'] = one.key
                return HttpResponse(json.dumps(text), content_type = "application/json")
            else:
                print('등록 되어있으면')
                #등록 되어있으면
                m_email = info.email
                m_email_list = []
                
                for i in User_Info.objects.filter(admin_email=m_email,admin=False):
                    try:
                        m_email_list.append(i.email)
                    except:
                        pass
                
                print('새로 작원 계정 등록')
                if m_text['code'] == 'SUCCESS':
                    for user in m_text['data']:
                        u_email = user['email']
                        u_nickname = user['nickname']
                        if u_email not in m_email_list:
                            User_Info.objects.create(email=u_email, nickname=u_nickname,admin_email=email,admin=False)
                text['message'] = '로그인 성고'
                text['user_list'] = serializers.serialize("json", User_Info.objects.filter(admin_email=m_email))
                text['setting'] = model_to_dict(User_Info.objects.get(email=m_email))
                text['prohibition'] = serializers.serialize("json", Prohibition.objects.filter(admin_email=m_email))
                request.session['email'] = m_email
                request.session['nickname'] = info.nickname
                request.session['admin_email'] = m_email
                request.session['admin'] = True
                text['key'] = ''
                if Secret_Key.objects.filter(admin_email=m_email):
                    one = Secret_Key.objects.get(admin_email=m_email)
                    text['key'] = one.key
                return HttpResponse(json.dumps(text), content_type = "application/json")
        else:
            print('직원 계정이고')
            #직원 계정이고
            try:
                info = User_Info.objects.get(email=email,admin=False)
            except:
                info = None
            if info != None:
                print('직원 계정이 등록 되어있으면 로그인 ok')
                #직원 계정이 등록 되어있으면 로그인 ok
                request.session['email'] = info.email
                request.session['nickname'] = info.nickname
                request.session['admin_email'] = info.admin_email
                request.session['admin'] = False
                text['message'] = '로그인 성공'
                text['user_list'] = serializers.serialize("json", User_Info.objects.filter(admin_email=info.admin_email))
                text['setting'] = model_to_dict(User_Info.objects.get(email=info.email,admin=False))
                text['prohibition'] = serializers.serialize("json", Prohibition.objects.filter(admin_email=info.admin_email))
                text['key'] = ''
                if Secret_Key.objects.filter(admin_email=info.admin_email):
                    one = Secret_Key.objects.get(admin_email=info.admin_email)
                    text['key'] = one.key
                
                return HttpResponse(json.dumps(text), content_type = "application/json")
            else:
                text['code'] = 'ERROR'
                text['message'] = '등록되지 않는 계정입니다'
                return HttpResponse(json.dumps(text), content_type = "application/json")
    

    
    
    
def get_options(sourcing_pr,existent_op_data,rate,tax):
    options = []
    for op in existent_op_data:
        option = {"key":"","image":"","value":[],"korValue":[],"price":"","productPrice":0,"salePrice":0,"stock":0,"margin":0,"weightPrice":0}
        deep_op = op["deep_op"]
        option["key"] = deep_op["ids"]
        
        option["price"] = str(deep_op["sale_price"])
        option["stock"] = int(deep_op["stock"])
        for i in op["op_list"]:
            if i["image"]:
                option["image"] = i["image"]
            if i["name"]:
                option["value"].append(i["name"])
            if i["korTypeName"]:
                option["korValue"].append(i["korTypeName"])
        option["value"] = " + ".join(option["value"])
        option["korValue"] = " + ".join(option["korValue"])
        
        option["margin"] = sourcing_pr["margin"]
        option["weightPrice"] = sourcing_pr["weightPrice"]
        option["productPrice"] = math.ceil(math.ceil((((rate*deep_op["origin_price"])/((100-sourcing_pr["margin"])*0.01))*tax)+sourcing_pr["weightPrice"])*0.1)*10
        sale_price = deep_op["sale_price"]
        option["salePrice"] =  math.ceil(math.ceil((((rate*sale_price)/((100-sourcing_pr["margin"])*0.01))*tax)+sourcing_pr["weightPrice"])*0.1)*10
        options.append(option)
    return options


def get_prop(ds):
    prop = []
    for key,val in ds.items():
        op = {"pid":"","name":"","korTypeName":"","values":[]}
        for i in val:
            op["pid"] = i["pid"]
            op["name"] = i["ctg_name"]
            op["korTypeName"] = i["ctg_korTypeName"]
            op["values"].append({"vid":i["vid"],"name":i["name"],
                                "korValueName":i["korTypeName"],"image":i["image"]})
        prop.append(op)
    return prop    

def get_existent_op_data(sourcing_op_ctg,sourcing_op_deep_ctg,ds):
    existent_op_data = []
    if sourcing_op_ctg:
        op_data = [ds[i] for i in ds.keys()]      
        select_data = {}
        for i in op_data:
            for j in i:
                if j["select"]:
                    key = "{0}:{1}".format(j["pid"], j["vid"])
                    select_data[key] = j
        for i in sourcing_op_deep_ctg:
            ids_list = [j.strip() for j in i["ids"].split(";")]
            top = len(ids_list)
            op_list = []
            for k in ids_list:
                try:
                    op_list.append(select_data[k])
                except:
                    break
            if top == len(op_list):
                existent_op_data.append({"deep_op":i,"op_list":op_list})
    else:
        existent_op_data = []
        for i in sourcing_op_deep_ctg:
            existent_op_data.append({"deep_op":i,"op_list":[]})
    return existent_op_data        
    
    
    
def seller_up_load(request):
    data = {
        "code": 200,
        "msg":"업로드 완료",
    }
    email = request.session["email"]
    admin_email = request.session["admin_email"]
    dt = json.loads(request.body.decode("utf-8"))
    
    deep_key = {"{0}-{1}".format(i["cannel_id"],i["product_id"]): i["num"] for i in dt}
    one_list = Sourcing.objects.filter(id__in = [i["pk"] for i in dt],admin_email=admin_email)
    up_one_list = []
    for one in one_list:
        if one.status == 1 or one.status == 3:
            up_one_list.append(one)


    rate = float(requests.get("https://tsnullp.herokuapp.com/seller/getExchangeRate").json()["data"]["exchange"])
    one = User_Info.objects.get(email=admin_email,admin_email=admin_email)
    tax = one.tax
    update_list = []
    for one in up_one_list:
        try:
            i = get_sourcing_data(one)
            sourcing_pr = i["sourcing_pr"][0]
            sourcing_op_ctg = i["sourcing_op_ctg"]
            sourcing_op_deep_ctg = i["sourcing_op_deep_ctg"]
            sourcing = i["sourcing"][0]
            main_img = i["main_img"]
            cont_img = i["cont_img"]
            ds = {}
            for i in sourcing_op_ctg:
                if i["select"]:
                    try:
                        ds[i["ctg_korTypeName"]].append(i)
                    except:
                        ds[i["ctg_korTypeName"]] = []
                        ds[i["ctg_korTypeName"]].append(i)
            prop = get_prop(ds)
            existent_op_data = get_existent_op_data(sourcing_op_ctg,sourcing_op_deep_ctg,ds)
            options = get_options(sourcing_pr,existent_op_data,rate,tax)
            attributes = []
            for i in prop:
                for j in i["values"]:
                    attributes.append({"attributeTypeName":i["korTypeName"],"attributeValueName":j["korValueName"]})
            update = {"email":"","naverID":"","exchange":0,"url":"","brand":"",
            "title":"","korTitle":"","mainImages":[],"content":[],"prop":"",
            "options":"","attributes":"","isClothes":"","isShoes":""}
            update["email"] = email
            update["naverID"] = deep_key["{0}-{1}".format(sourcing["cannel_id"], sourcing["product_id"])]
            update["exchange"] = rate
            update["url"] = "https://item.taobao.com/item.htm?id={0}".format(sourcing["item_id"])
            update["brand"] = "기타"
            update["title"] = sourcing_pr["title"]
            update["korTitle"] = sourcing["org_title"]
            update["mainImages"] = [i["src"] for i in main_img]
            update["content"] = [i["src"] for i in cont_img]
            update["prop"] = prop
            update["options"] = options
            update["attributes"] = attributes
            update["isClothes"] = "Y" if sourcing_pr["isClothes"] else "N"
            update["isShoes"] = "Y" if sourcing_pr["isShoes"] else "N"
            update_list.append(update)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            req = requests.post('https://tsnullp.herokuapp.com/seller/product',data=json.dumps(update),headers=headers)
            if req.status_code == 200:
                jdata = req.json()
                print(jdata)
                if jdata["code"] == "SUCCESS":
                    one.status = 2
                else:
                    one.status = 3
            one.save()
        except:
            data["msg"] = traceback.format_exc()

    data["data"] = update_list
    return HttpResponse(json.dumps(data), content_type = "application/json")   
    
    
    
    