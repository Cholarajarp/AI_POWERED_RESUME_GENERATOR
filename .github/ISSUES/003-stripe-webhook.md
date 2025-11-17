Title: Verify and handle Stripe webhooks securely

Description:
The webhook handler in `backend/app/api/payments.py` does not verify signatures or handle event types. Update to:

- Use `stripe.Webhook.construct_event` with `STRIPE_WEBHOOK_SECRET` to verify signature.
- Handle `checkout.session.completed` and `invoice.payment_succeeded` events to update user subscriptions/records.
- Add tests that simulate webhook payloads and signature verification (use Stripe CLI or fixtures).

Files to update:
- `backend/app/api/payments.py`

Priority: High
