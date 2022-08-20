from simpleapi import Router, Request


def item_middleware(request: Request):
    request.extra["item_middleware"] = True


router = Router(middleware=[item_middleware])


@router.get("/test")
def test_router_get():
    """Tests that router get works"""
    return "test"


@router.post("/test")
def test_router_post():
    """Tests that router post works"""
    return "test"


@router.get("/{additional}/test")
def dynamic_router_test(request: Request):
    """Tests that dynamic routing works for a router"""
    return request.params["additional"]


@router.get("/router_middleware")
def router_middleware(request: Request):
    return {
        "global": request.extra["global_middleware"],
        "router": request.extra["item_middleware"],
    }
