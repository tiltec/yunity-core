from yunity.models import Category as CategoryModel

response = {
    "http_status": 200,
    "response": {
        "categories": [
            {"name": _.name, "parent": _.parent, "id": _.id}
            for _ in CategoryModel.objects.all()
        ],
    },
}
