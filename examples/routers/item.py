from simpleapi import Router

router = Router()

@router.get("/item")
def item():
    return {"name": "test", "price": 69}