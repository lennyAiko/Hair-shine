# holds all repeated functions

class Actions():

    @staticmethod
    def verify(model, index):
        try:
            instance = model.objects.get(id=index)
            return instance
        except model.DoesNotExist:
            return False

    def create(data, serializer):
        serializer = serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return (serializer.data, 201)
    
    def get(serializer, model):
        query = model.objects.all()
        serializer = serializer(query, many=True)
        
        return (serializer.data, 200)
    
    def get_single(serializer, model, index):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        try:
            instance.views += 1
            instance.save()
        except:
            pass
        
        serializer = serializer(instance, many=False)
        return serializer.data, 200
    
    def delete(model, index):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        instance.delete()
        return {"message": "Successfully deleted"}, 204
    
    def update(serializer, model, index, data):
        instance = Actions.verify(model, index)
        if instance == False:
            return {"message": "Object not found"}, 404
        
        serializer = serializer(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data, 202
        
        return serializer.errors, 400
    
