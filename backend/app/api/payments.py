from fastapi import APIRouter, Request, HTTPException
import stripe
from ..core.config import settings

router = APIRouter()
stripe.api_key = settings.STRIPE_API_KEY

@router.post("/create-checkout-session")
async def create_checkout(payload: dict):
    # payload: {price_id}
    # Create a Checkout Session for test
    try:
        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": payload.get('price_id'), "quantity": 1}],
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get('stripe-signature')
    try:
        event = stripe.Event.construct_from(payload.decode(), stripe.api_key)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")
    # TODO: verify signature and handle event types
    return {"status": "received"}
