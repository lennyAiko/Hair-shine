# holds all repeated functions

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
            

    def create(data, serializer):
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return (serializer.data, 201)
    
    def get(serializer, model, query=None, spy=None, selection=None):
        
        if query == None:
            query = model.objects.all()
            serializer = serializer(query, many=True)

        else:
            if selection == 'products':
                result = Crawler.search_products(query, model, spy, serializer)
                serializer = serializer(result, many=True)

            if selection == 'categories':
                result = Crawler.search_categories(query, model, spy, serializer)
                serializer = serializer(result, many=True)

            if selection == 'sub_categories':
                result = Crawler.search_sub_categories(query, model, spy, serializer)
                serializer = serializer(result, many=True)
        
        return (serializer.data, 200)
    
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
    

def Filterer(model, serializer, param):
    query = model.objects.all().order_by(param)
    serializer = serializer(query, many=True)

    return serializer.data, 200

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
