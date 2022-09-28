from django.shortcuts import render, redirect
from account.models import *
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.db.models import Count, Subquery
import time


def landing(request):
    page = request.GET.get('page', '1')
    products = Products.objects.order_by('-id')
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)
    context = {'products': page_obj}
    return render(request, 'shops/landing.html', context)


def product_register(request):
    if request.method == "POST":
        form = ProductRegisterForm(request.POST)
        if form.is_valid():
            Products.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                seller=CustomSeller.objects.get(CustomUser=request.user),
                image=request.FILES['image'],
            )
            return redirect('/')
    else:
        form = ProductRegisterForm()
    return render(request, 'shops/productRegister.html', {'form': form})


def product_detail(request, pk):
    product = Products.objects.get(id=pk)
    # 1-1 역방향 참조(python에서 조인하기 때문에 query로 확인 불가)
    # review_and_comment = Review.objects.prefetch_related('reviewtoreview_set')
    #                          .filter(product_id=product)
    review_and_comments = Review.objects.raw(
        f"""
        SELECT * 
            ,shops_reviewtoreview.content AS rcontent
            ,shops_reviewtoreview.user_id AS ruser_id
            , shops_reviewtoreview.id AS rid 
        FROM 'shops_review' 
        LEFT JOIN 'shops_reviewtoreview' 
        ON 'shops_review'.id = 'shops_reviewtoreview'.review_id 
        WHERE product_id = {pk}
        """
    )

    user = CustomUser.objects.all()

    review_and_comment_list = []
    id = 0
    for review_and_comment in review_and_comments:
        if review_and_comment.review_id is None:
            if review_and_comment.user.activate is True:
                review_dict = {'review': dict(id=review_and_comment.id, title=review_and_comment.title,
                                              user=user[review_and_comment.user_id - 1],
                                              content=review_and_comment.content,
                                              starRating=review_and_comment.starRating)}
            else:
                review_dict['review'] = dict(id='block', title='차단된 제목입니다.',
                                             user='차단된 유저입니다.', content='차단된 내용입니다.',
                                             starRating='차단된 별점입니다.')
        elif review_and_comment.review_id != id:
            review_dict = {}
            if review_and_comment.user.activate is True:
                review_dict['review'] = {'id': review_and_comment.id, 'title': review_and_comment.title,
                                         'user': user[review_and_comment.user_id - 1],
                                         'content': review_and_comment.content,
                                         'starRating': review_and_comment.starRating}
            else:
                review_dict['review'] = dict(id='block', title='차단된 제목입니다.',
                                             user='차단된 유저입니다.', content='차단된 내용입니다.',
                                             starRating='차단된 별점입니다.')
            if user[review_and_comment.ruser_id - 1].activate is True:
                review_dict['reviewToReview'] = [
                    {'id': review_and_comment.rid, 'user': user[review_and_comment.ruser_id - 1],
                     'content': review_and_comment.rcontent}]
            else:
                review_dict['reviewToReview'] = [
                    {'id': review_and_comment.rid, 'user': '차단된 유저입니다.',
                     'content': '차단된 내용입니다.'}]
            id = review_and_comment.review_id
        else:
            review_dict = review_and_comment_list.pop()
            if user[review_and_comment.ruser_id - 1].activate is True:
                review_dict['reviewToReview'].append(
                    {'id': review_and_comment.rid, 'user': user[review_and_comment.user_id - 1],
                     'content': review_and_comment.rcontent})
            else:
                review_dict['reviewToReview'].append(
                    {'id': review_and_comment.rid, 'user': '차단된 유저입니다.',
                     'content': '차단된 내용입니다.'})
        review_and_comment_list.append(review_dict)

    page = request.GET.get('page', '1')
    paginator = Paginator(review_and_comment_list, 10)
    page_obj = paginator.get_page(page)
    if request.method == "POST":
        PurchaseHistory.objects.create(
            product=product,
            user=request.user
        )
        return redirect('/')
    return render(request, 'shops/productDetail.html', {'product': product, 'reviews': page_obj})


def review(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == "POST":
        Review.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            starRating=request.POST['starRating'],
            user=request.user,
            product=product,
        )
        return redirect('productDetail', pk)
    return render(request, 'shops/productDetail.html')


def review_to_review(request, pk, pk2):
    comment = Review.objects.get(id=pk2)
    if request.method == "POST":
        ReviewToReview.objects.create(
            content=request.POST['contentreview'],
            user=request.user,
            review=comment,
        )
        return redirect('productDetail', pk)
    return render(request, 'shops/productDetail.html')


def cert(request):
    pc = Products.objects.all().count()
    if not request.user.is_authenticated:
        cookie_list = []
        for i in range(1, pc + 1):
            product_key = "product_" + str(i)
            cookies = request.COOKIES.get(product_key)
            if cookies is not None:
                product = Products.objects.get(id=cookies)
                cookie_list.append(product)
        return render(request, 'shops/cert.html', {'certs': cookie_list})
    else:
        for i in range(1, pc + 1):
            product_key = "product_" + str(i)
            cookies = request.COOKIES.get(product_key)
            if cookies is not None:
                product = Products.objects.get(id=cookies)
                Cert.objects.create(
                    product=product,
                    user=request.user,
                    quantity=1
                )
        certs = Cert.objects.all()
        response = render(request, 'shops/cert.html', {'certs': certs})
        for i in range(1, pc + 1):
            product_key = "product_" + str(i)
            response.delete_cookie(product_key, path="/")
        return response


def add_cert(request, pk):
    product = Products.objects.get(id=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            Cert.objects.create(
                user=request.user,
                product=product,
                quantity=1,
            )
            return redirect('/')
    else:
        response = redirect('/')
        product_key = "product_" + str(product.id)
        product_value = product.id
        response.set_cookie(product_key, product_value, max_age=604800)
        return response
    return render(request, 'shops/productDetail.html')


def buy_cert(request):
    if request.user.is_authenticated:
        certs = Cert.objects.filter(user=request.user)
        for cert_product in certs:
            if request.POST.get(str(cert_product.product.id)) == "on":
                PurchaseHistory.objects.create(
                    user=request.user,
                    product=cert_product.product,
                )
                cert_product.delete()

    return redirect('/cert')


def report_review(request, pk, pk2, pk3):
    if request.user.is_authenticated:
        if request.method == "POST":
            reviews = Review.objects.get(id=pk3)
            Report.objects.create(
                report_user=request.user,
                reported_user=CustomUser.objects.get(username=pk),
                product=Products.objects.get(id=pk2),
                review=reviews,
                content=reviews.content,
            )
            return redirect('/product/' + str(pk2))
    return render(request, 'shops/productDetail.html')


def report_review_to_review(request, pk, pk2, pk3):
    if request.user.is_authenticated:
        if request.method == "POST":
            reviewable = ReviewToReview.objects.get(id=pk3)
            Report.objects.create(
                report_user=request.user,
                reported_user=CustomUser.objects.get(username=pk),
                product=Products.objects.get(id=pk2),
                reviewtoreview=reviewable,
                content=reviewable.content,
            )
            return redirect('/product/' + str(pk2))
    return render(request, 'shops/productDetail.html')


def seller(request):
    if request.user.is_authenticated:
        user = CustomSeller.objects.get(CustomUser_id=request.user.id)
        custom_user = CustomUser.objects.all()

        product_and_purchases = PurchaseHistory.objects.raw(
            f"""
                SELECT *,'shops_purchasehistory'.id as pid
                FROM 'shops_purchasehistory'
                LEFT JOIN 'shops_products'
                ON 'shops_purchasehistory'.product_id = 'shops_products'.id
                ,(SELECT product_id,count(product_id) AS num
                FROM 'shops_purchasehistory'
                GROUP BY product_id
                HAVING count(*)) AS A
                WHERE 'shops_products'.seller_id= {user.id} and
                'shops_purchasehistory'.product_id=A.product_id
                and 'shops_purchasehistory'.Delivery=0
                ORDER BY product_id;
                """
        )
        remaining_purchases = PurchaseHistory.objects.raw(
            f"""
            SELECT id,product_id,count(product_id) AS num
            FROM 'shops_purchasehistory'
            WHERE 'shops_purchasehistory'.Delivery=False and 
            (SELECT id From 'shops_products' WHERE 'shops_products'.seller_id= {user.id})
            GROUP BY product_id
            HAVING count(*)>=1
            ORDER BY product_id
            """
        )
        # product_and_purchase_list = Products.objects.prefetch_related('purchasehistory_set').filter(
        #     seller_id=user.id).order_by('id').annotate(count=Count('purchasehistory'))

        remaining_purchase_list = []
        for remainingPurchase in remaining_purchases:
            remaining_purchase_list.append(remainingPurchase.num)
        product_and_purchase_list = []
        id = 0
        for product_and_purchase in product_and_purchases:
            if id != product_and_purchase.product_id:
                product_dict = {'product': dict(name=product_and_purchase.name,
                                                price=product_and_purchase.price,
                                                count=product_and_purchase.num,
                                                remain_count=remaining_purchase_list.pop(0)),
                                'Purchase': [dict(id=product_and_purchase.pid,
                                                  user=custom_user[product_and_purchase.user_id - 1])]}
                id = product_and_purchase.product_id
            else:
                product_dict = product_and_purchase_list.pop()
                product_dict['Purchase'].append(dict(id=product_and_purchase.pid,
                                                     user=custom_user[product_and_purchase.user_id - 1]))
            product_and_purchase_list.append(product_dict)

    return render(request, 'shops/seller.html', {'productAndPurchases': product_and_purchase_list})


def delivery(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            purchase_and_history = PurchaseHistory.objects.get(id=pk)
            purchase_and_history.Delivery = True
            purchase_and_history.save()
            return redirect('/seller/')
