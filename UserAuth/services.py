import os
import stripe

stripe.api_key = os.environ.get('STRIPE_API_KEY')

def createNewCustomer(user):
    customer = stripe.Customer.create(
        name=f"{user.firstName} {user.lastName}",
        email=f"{user.email}"
    )

    return customer

def createCustomerPortal(user):
    portal = stripe.billing_portal.Session.create(
        customer = user.stripeCustomerID,
        configuration = 'test_eVa3ga9zE1AHdy0dQQ',
        return_url = 'http://localhost:3000/profile'
    )

    return portal.url
