# holds all repeated functions

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class Actions():

    @staticmethod
    def verify(model, index):
        try:
            instance = model.objects.get(id=index)
            return instance
        except model.DoesNotExist:
            return False
    
    @staticmethod
    def product_rating(instance, comments):
        instance.views += 1
        instance.save()

        query = comments.objects.filter(product=instance.id)
        rating = 0
        count = 0
        for i in query:
            rating += i.rate
            count += 1
        if count > 0:
            rating = rating / count
        return int(rating)
    
    @staticmethod
    def my_paginator(query, req, serializer):
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(query, req)

        serializer = serializer(page, many=True)

        return paginator.get_paginated_response(serializer.data).data
            

    def create(data, serializer):
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return (serializer.data, 201)
    
    def get(serializer, model, query=None, spy=None, selection=None, req=None):
        
        if query == None:
            query = model.objects.all().order_by('date_added')

            data = Actions.my_paginator(query, req, serializer)

        else:
            if selection == 'products':
                result = Crawler.search_products(query, model, spy, serializer)
                data = Actions.my_paginator(result, req, serializer)

            # if selection == 'categories':
            #     result = Crawler.search_categories(query, model, spy, serializer)
            #     serializer = serializer(result, many=True)
            #     # data = serializer.data

            # if selection == 'sub_categories':
            #     result = Crawler.search_sub_categories(query, model, spy, serializer)
            #     serializer = serializer(result, many=True)
            #     # data = serializer.data
        
        return (data, 200)
    
    def get_single(serializer, model, index):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        serializer = serializer(instance, many=False)
        return serializer.data, 200

    def get_single_product(serializer, model, index, comments=None):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        rating = Actions.product_rating(instance, comments)
        serializer = serializer(instance, many=False)
        data = serializer.data
        data['rating'] = rating
        data['product_img'] = f'http://hairshine.pythonanywhere.com{data["product_img"]}'

        return data, 200
        
    
    def delete(model, index):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        instance.delete()
        return {"message": "Successfully deleted"}, 204
    
    def update(serializer, model, index, data, item=False):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        if item:
            data = {
                "quantity": data['quantity'],
                "amount": data['quantity'] * instance.product.actual_price
            }
        
        serializer = serializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data, 202
        
        return serializer.errors, 400
    
    def bulk(model, data, cart, second_model):
        bulk_list = []
        for _ in data:
            bulk_list.append(
                model(
                    product=second_model.objects.get(id=_['id']),
                    quantity=_['quantity'],
                    amount=_['amount'],
                    cart=cart
                )
            )
        try:
            msg = model.objects.bulk_create(bulk_list)
            data = "Successful"
            status = 200
        except:
            data = "Error adding items"
            staus = 400
        return data, status


    

def Filterer(model, serializer, param, req=None):
    query = model.objects.all().order_by(param)
    data = Actions.my_paginator(query, req, serializer)

    return data, 200

class Crawler():

    def search_products(query, model, spy, serializer):

        result = model.objects.filter(spy(name__icontains=query) | spy(first_description__icontains=query) | spy(second_description__icontains=query))
        return result
    
    def search_categories(query, model, spy, serializer):

        result = model.objects.filter(spy(name__icontains=query))
        return result
    
    def search_sub_categories(query, model, spy, serializer):

        result = model.objects.filter(spy(name__icontains=query))
        return result
