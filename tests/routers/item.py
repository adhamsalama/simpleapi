from simpleapi import Router

router = Router()


@router.get("/test")
def test_router_get():
    """Tests that router get works"""
    return "test"


@router.post("/test")
def test_router_post():
    """Tests that router post works"""
    return "test"
