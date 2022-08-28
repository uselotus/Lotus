import json

import pytest
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from metering_billing.models import User
from model_bakery import baker
from rest_framework import status


@pytest.fixture
def customer_test_common_setup(generate_org_and_api_key, add_customers_to_org, add_users_to_org, api_client_with_api_key_auth):
    def do_customer_test_common_setup(*, num_customers, has_org_api_key, user_in_org, user_org_and_api_key_org_different):
        #set up organizations and api keys
        org, key = generate_org_and_api_key()
        org2, key2 = generate_org_and_api_key()
        return_dict = {
            "org":org,
            "key":key,
            "org2":org2,
            "key2":key2,
        }
        #set up the client with the appropriate api key spec
        if has_org_api_key:
            client = api_client_with_api_key_auth(key)
        else:
            client = api_client_with_api_key_auth("bogus-key")
        return_dict["client"] = client

        #set up the user with the appropriate org spec
        if user_in_org:
            if not user_org_and_api_key_org_different:
                user, = add_users_to_org(org, n=1)
            else:
                user, = add_users_to_org(org2, n=1)
        else:
            user, = baker.make(User, _quantity=1)
        return_dict["user"] = user

        #set up number of customers
        if num_customers > 0:
            add_customers_to_org(org, n=num_customers)
            add_customers_to_org(org2, n=num_customers)
        
        #authenticare user
        client.force_authenticate(user=user)

        return return_dict
    return do_customer_test_common_setup

@pytest.mark.django_db
class TestGetCustomers():
    """Testing the GET of Customer endpoint:
    GET: Return list of customers associated with the organization with API key.
        partitions:
        has_org_api_key: true, false
        user_in_org: true, false
        num_customers: 0, >0
        user_org_and_api_key_org_different: true, false
    """

    def test_user_in_org_valid_org_api_key_can_access_customers_empty(self, customer_test_common_setup):
        #covers num customers = 0, has_org_api_key=true, user_in_org=true, user_org_and_api_key_org_different=false
        num_customers = 0
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]

        payload = {}
        response = client.get(reverse("customer"), payload)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == num_customers

    def test_user_in_org_valid_org_api_key_can_access_customers_multiple(self, customer_test_common_setup):
        #covers num customers > 0
        num_customers = 5
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]

        payload = {}
        response = client.get(reverse("customer"), payload)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == num_customers

    def test_user_not_in_org_but_valid_org_api_key_reject_access(self, customer_test_common_setup):
        #covers user_in_org = false
        num_customers = 1
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=False,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]

        payload = {}
        response = client.get(reverse("customer"), payload)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_in_org_but_invalid_org_api_key_reject_access(self, customer_test_common_setup):
        #covers has_org_api_key = false
        num_customers = 2
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=False,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]

        payload = {}
        response = client.get(reverse("customer"), payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_org_and_api_key_different_reject_access(self, customer_test_common_setup):
        #covers user_org_and_api_key_org_different = true
        num_customers = 3
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=True,
        )
        client = return_dict["client"]

        payload = {}
        response = client.get(reverse("customer"), payload)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.fixture
def insert_customer_payload():
    payload = {
        "name":"test_customer",
        "customer_id":"test_customer_id",
        "billing_id":"test_billing_id",
        "balance":30,
        "currency":"USD",
        "payment_provider_id":"test_payment_provider_id",
        "properties": {}
    }
    return payload

@pytest.mark.django_db
class TestInsertCustomer():
    """Testing the POST of Customer endpoint:
    POST: Return list of customers associated with the organization with API key / user.
    partitions:
        has_org_api_key: true, false
        user_in_org: true, false
        user_org_and_api_key_org_different: true, false
        num_customers_before_insert = 0, >0
    """

    def test_user_in_org_valid_org_api_key_can_create_customer_empty_before(self, customer_test_common_setup, insert_customer_payload, get_customers_in_org):
        #covers num_customers_before_insert = 0, has_org_api_key=true, user_in_org=true, user_org_and_api_key_org_different=false
        num_customers = 0
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]
        org = return_dict["org"]

        response = client.post(
            reverse("customer"),
            data=json.dumps(insert_customer_payload, cls=DjangoJSONEncoder),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) > 0 #check that the response is not empty
        assert len(get_customers_in_org(org)) == 1

    def test_user_in_org_valid_org_api_key_can_create_customer_nonempty_before(self, customer_test_common_setup, insert_customer_payload, get_customers_in_org):
        #covers num_customers_before_insert = 0, has_org_api_key=true, user_in_org=true, user_org_and_api_key_org_different=false, authenticated=true
        num_customers = 5
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]
        org = return_dict["org"]

        response = client.post(
            reverse("customer"),
            data=json.dumps(insert_customer_payload, cls=DjangoJSONEncoder),
            content_type="application/json",
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) > 0
        assert len(get_customers_in_org(org)) == num_customers+1

    def test_user_not_in_org_but_valid_org_api_key_reject_insert(self, customer_test_common_setup, insert_customer_payload, get_customers_in_org):
        #covers user_in_org = false
        num_customers = 0
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=False,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]
        org = return_dict["org"]

        response = client.post(
            reverse("customer"),
            data=json.dumps(insert_customer_payload, cls=DjangoJSONEncoder),
            content_type="application/json",
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert len(get_customers_in_org(org)) == num_customers

    def test_user_in_org_but_invalid_org_api_key_reject_access(self, customer_test_common_setup, insert_customer_payload, get_customers_in_org):
        #covers has_org_api_key = false
        num_customers = 5
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=False,
            user_in_org=True,
            user_org_and_api_key_org_different=False,
        )
        client = return_dict["client"]
        org = return_dict["org"]

        response = client.post(
            reverse("customer"),
            data=json.dumps(insert_customer_payload, cls=DjangoJSONEncoder),
            content_type="application/json",
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert len(get_customers_in_org(org)) == num_customers

    def test_user_org_and_api_key_different_reject_access(self, customer_test_common_setup, insert_customer_payload, get_customers_in_org):
        #covers user_org_and_api_key_org_different = True
        num_customers = 3
        return_dict = customer_test_common_setup(
            num_customers=num_customers,
            has_org_api_key=True,
            user_in_org=True,
            user_org_and_api_key_org_different=True,
        )
        client = return_dict["client"]
        org = return_dict["org"]
        org2 = return_dict["org2"]

        response = client.post(
            reverse("customer"),
            data=json.dumps(insert_customer_payload, cls=DjangoJSONEncoder),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(get_customers_in_org(org)) == num_customers
        assert len(get_customers_in_org(org2)) == num_customers
