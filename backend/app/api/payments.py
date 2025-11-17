from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import stripe
from ..core.config import settings

router = APIRouter()
stripe.api_key = settings.STRIPE_API_KEY

class CreateCheckoutSessionRequest(BaseModel):
    plan_type: str  # "basic", "pro", "enterprise"
    email: str

class CreateCheckoutSessionResponse(BaseModel):
    session_id: str
    session_url: str

STRIPE_PLANS = {
    "basic": {
        "name": "Basic Plan",
        "price": 990,  # $9.90/month
        "currency": "usd",
        "billing_period": "month",
        "features": [
            "5 resumes per month",
            "Basic AI templates",
            "PDF export"
        ]
    },
    "pro": {
        "name": "Pro Plan",
        "price": 1990,  # $19.90/month
        "currency": "usd",
        "billing_period": "month",
        "features": [
            "Unlimited resumes",
            "All AI templates",
            "Premium PDF templates",
            "Interview prep",
            "Priority support"
        ]
    },
    "enterprise": {
        "name": "Enterprise Plan",
        "price": 4990,  # $49.90/month
        "currency": "usd",
        "billing_period": "month",
        "features": [
            "Everything in Pro",
            "Team collaboration",
            "Custom templates",
            "API access",
            "Dedicated support"
        ]
    }
}

@router.post("/create-checkout-session", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    """Create a Stripe checkout session for subscription"""
    try:
        if request.plan_type not in STRIPE_PLANS:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        plan = STRIPE_PLANS[request.plan_type]
        
        session = stripe.checkout.Session.create(
            customer_email=request.email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": plan["currency"],
                        "product_data": {
                            "name": plan["name"],
                            "description": ", ".join(plan["features"][:2]) + "..."
                        },
                        "unit_amount": plan["price"],
                        "recurring": {
                            "interval": "month",
                            "interval_count": 1
                        }
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/payment/cancelled",
        )
        
        return {
            "session_id": session.id,
            "session_url": session.url
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

class RetrieveSessionRequest(BaseModel):
    session_id: str

@router.post("/retrieve-session")
async def retrieve_session(request: RetrieveSessionRequest):
    """Retrieve checkout session details"""
    try:
        session = stripe.checkout.Session.retrieve(request.session_id)
        return {
            "id": session.id,
            "payment_status": session.payment_status,
            "customer_email": session.customer_email,
            "subscription_id": session.subscription,
        }
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

class ManageSubscriptionRequest(BaseModel):
    action: str  # "cancel", "update_plan"
    subscription_id: str
    new_plan_type: str = None

@router.post("/manage-subscription")
async def manage_subscription(request: ManageSubscriptionRequest):
    """Manage user subscription (cancel or upgrade/downgrade plan)"""
    try:
        if request.action == "cancel":
            stripe.Subscription.delete(request.subscription_id)
            return {"status": "subscription_cancelled"}
        
        elif request.action == "update_plan":
            if not request.new_plan_type or request.new_plan_type not in STRIPE_PLANS:
                raise HTTPException(status_code=400, detail="Invalid plan type")
            
            subscription = stripe.Subscription.retrieve(request.subscription_id)
            new_plan = STRIPE_PLANS[request.new_plan_type]
            
            stripe.Subscription.modify(
                request.subscription_id,
                items=[{
                    "id": subscription["items"]["data"][0].id,
                    "price_data": {
                        "currency": new_plan["currency"],
                        "product_data": {
                            "name": new_plan["name"],
                        },
                        "unit_amount": new_plan["price"],
                        "recurring": {
                            "interval": "month"
                        }
                    }
                }]
            )
            
            return {"status": "subscription_updated"}
    
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/plans")
async def list_plans():
    """List available subscription plans"""
    return STRIPE_PLANS

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: Create or update user subscription in DB
        pass
    
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # TODO: Update user subscription status in DB
        pass
    
    return {"status": "success"}
