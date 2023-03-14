/* eslint-disable camelcase */
import React, { useState } from "react";
import { Tabs, Button, Modal } from "antd";
import {
  useMutation,
  useQueryClient,
  useQuery,
  UseQueryResult,
} from "react-query";
import dayjs from "dayjs";
import { toast } from "react-toastify";
import { useNavigate, useParams } from "react-router-dom";
import { PlanType } from "../../types/plan-type";
import {
  CreateSubscriptionType,
  TurnSubscriptionAutoRenewOffType,
  ChangeSubscriptionPlanType,
  CancelSubscriptionBody,
  CancelSubscriptionQueryParams,
} from "../../types/subscription-type";
import LoadingSpinner from "../LoadingSpinner";
import { Customer, Plan, PricingUnits } from "../../api/api";
import SubscriptionView from "./CustomerSubscriptionView";
import { CustomerType } from "../../types/customer-type";
import "./CustomerDetail.css";
import CustomerInvoiceView from "./CustomerInvoices";
import CustomerBalancedAdjustments from "./CustomerBalancedAdjustments";
import { CustomerCostType } from "../../types/revenue-type";
import CustomerInfoView from "./CustomerInfo";

import { CurrencyType } from "../../types/pricing-unit-type";
import { PageLayout } from "../base/PageLayout";
import { QueryErrors } from "../../types/error-response-types";
import { DeleteOutlined } from "@ant-design/icons";

type CustomerDetailsParams = {
  customerId: string;
};
function CustomerDetail() {
  const { customerId: customer_id } = useParams<CustomerDetailsParams>();

  const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);

  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [startDate, setStartDate] = useState<string>(
    dayjs().subtract(1, "month").format("YYYY-MM-DD")
  );
  const [endDate, setEndDate] = useState<string>(dayjs().format("YYYY-MM-DD"));
  const { data: plans }: UseQueryResult<PlanType[]> = useQuery<PlanType[]>(
    ["plan_list"],
    () =>
      Plan.getPlans({
        version_custom_type: "public_only",
        version_status: "active",
      }).then((res) => res)
  );

  const { data: pricingUnits }: UseQueryResult<CurrencyType[]> = useQuery<
    CurrencyType[]
  >(["pricing_unit_list"], () => PricingUnits.list().then((res) => res));
  const { data, refetch }: UseQueryResult<CustomerType> =
    useQuery<CustomerType>(["customer_detail", customer_id], () =>
      Customer.getCustomerDetail(customer_id as string).then((res) => res)
    );

  const { data: cost_analysis } = useQuery<CustomerCostType>(
    ["customer_cost_analysis", customer_id, startDate, endDate],
    () => Customer.getCost(customer_id as string, startDate, endDate),
    {
      enabled: true,
      placeholderData: {
        per_day: [],
        total_revenue: 0,
        total_cost: 0,
        margin: 0,
      },
    }
  );

  const deleteCustomerMutation = useMutation(
    (id: string) => Customer.deleteCustomer(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["customer_list"]);
        navigate("/customers");
        toast.success("Customer deleted successfully");
      },
      onError: (error: QueryErrors) => {
        toast.error(error.response.data.title);
      },
    }
  );

  const createSubscriptionMutation = useMutation(
    (post: CreateSubscriptionType) => Customer.createSubscription(post),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["customer_list"]);
        queryClient.invalidateQueries(["customer_detail", customer_id]);
        queryClient.invalidateQueries(["balance_adjustments", customer_id]);
        queryClient.invalidateQueries(["draft_invoice", customer_id]);
        refetch();
        toast.success("Subscription created successfully");
      },
      onError: (error: QueryErrors) => {
        toast.error(error.response.data.title);
      },
    }
  );

  const cancelSubscriptionMutation = useMutation(
    (obj: { post: CancelSubscriptionBody; subscription_id: string }) =>
      Customer.cancelSubscription(obj.subscription_id, obj.post),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["customer_list"]);
        queryClient.invalidateQueries(["customer_detail", customer_id]);
        queryClient.invalidateQueries(["balance_adjustments", customer_id]);
        queryClient.invalidateQueries(["draft_invoice", customer_id]);
        refetch();
        toast.success("Subscription cancelled successfully");
      },
      onError: (error: QueryErrors) => {
        toast.error(error.response.data.title);
      },
    }
  );

  const changeSubscriptionPlanMutation = useMutation(
    (obj: { params: object; post: ChangeSubscriptionPlanType }) =>
      Customer.changeSubscriptionPlan(obj.post, obj.params),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["customer_list"]);
        queryClient.invalidateQueries(["customer_detail", customer_id]);
        queryClient.invalidateQueries(["balance_adjustments", customer_id]);
        queryClient.invalidateQueries(["draft_invoice", customer_id]);
        refetch();
        toast.success("Subscription switched successfully");
      },
      onError: (error: QueryErrors) => {
        toast.error(error.response.data.title);
      },
    }
  );

  const turnSubscriptionAutoRenewOffMutation = useMutation(
    (obj: { params: object; post: TurnSubscriptionAutoRenewOffType }) =>
      Customer.turnSubscriptionAutoRenewOff(obj.post, obj.params),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["customer_list"]);
        refetch();
        toast.success("Subscription auto renew turned off");
      },
      onError: (error: QueryErrors) => {
        toast.error(error.response.data.title);
      },
    }
  );

  const cancelSubscription = (
    props: CancelSubscriptionBody,
    subscription_id: string
  ) => {
    cancelSubscriptionMutation.mutate({
      post: props,
      subscription_id,
    });
  };

  const changeSubscriptionPlan = (
    params: object,
    props: ChangeSubscriptionPlanType
  ) => {
    changeSubscriptionPlanMutation.mutate({
      params,
      post: props,
    });
  };

  const turnSubscriptionAutoRenewOff = (
    params: object,
    props: TurnSubscriptionAutoRenewOffType
  ) => {
    turnSubscriptionAutoRenewOffMutation.mutate({
      params,
      post: props,
    });
  };

  const refetchGraphData = (start_date: string, end_date: string) => {
    setStartDate(start_date);
    setEndDate(end_date);
    queryClient.invalidateQueries(["customer_cost_analysis", customer_id]);
  };

  const createSubscription = (props: CreateSubscriptionType) => {
    createSubscriptionMutation.mutate(props);
  };

  return (
    <PageLayout
      title={data?.customer_name}
      className="text-[24px] font-alliance "
      hasBackButton
      aboveTitle
      mx={false}
      extra={[
        <Button
          onClick={() => setShowDeleteModal(true)}
          type="primary"
          size="large"
          key="create-plan"
          className="hover:!bg-primary-700"
          style={{ background: "#C3986B", borderColor: "#C3986B" }}
        >
          <div className="flex items-center  justify-between text-white">
            <div>
              <DeleteOutlined className="!text-white w-12 h-12 cursor-pointer" />
              Delete Customer
            </div>
          </div>
        </Button>,
      ]}
      backButton={
        <div>
          <Button
            onClick={() => navigate(-1)}
            type="primary"
            size="large"
            key="create-custom-plan"
            style={{
              background: "#F5F5F5",
              borderColor: "#F5F5F5",
            }}
          >
            <div className="flex items-center justify-between text-black">
              <div>&larr; Go back</div>
            </div>
          </Button>
        </div>
      }
    >
      {plans === undefined ? (
        <div className="min-h-[60%]">
          <LoadingSpinner />
        </div>
      ) : (
        <Tabs defaultActiveKey="details" size="large">
          <Tabs.TabPane tab="Details" key="details">
            {data !== undefined &&
            cost_analysis !== undefined &&
            pricingUnits !== undefined ? (
              <CustomerInfoView
                data={data}
                cost_data={cost_analysis}
                refetch={refetch}
                pricingUnits={pricingUnits}
                onDateChange={refetchGraphData}
              />
            ) : (
              <div className="min-h-[60%]">
                <LoadingSpinner />
              </div>
            )}
          </Tabs.TabPane>
          <Tabs.TabPane tab="Subscriptions" key="subscriptions">
            {data !== undefined ? (
              <div key={customer_id}>
                <SubscriptionView
                  customer_id={customer_id as string}
                  subscriptions={data.subscriptions}
                  plans={plans}
                  onCreate={createSubscription}
                  onCancel={cancelSubscription}
                  onPlanChange={changeSubscriptionPlan}
                  onAutoRenewOff={turnSubscriptionAutoRenewOff}
                />
              </div>
            ) : (
              <div className="h-192" />
            )}
          </Tabs.TabPane>
          <Tabs.TabPane tab="Invoices" key="invoices">
            <CustomerInvoiceView
              invoices={data?.invoices}
              paymentMethod={data?.payment_provider}
            />
          </Tabs.TabPane>
          <Tabs.TabPane tab="Credits" key="credits">
            <CustomerBalancedAdjustments customerId={customer_id as string} />
          </Tabs.TabPane>
        </Tabs>
      )}
      {showDeleteModal && (
        <Modal
          title="Delete Customer"
          visible={showDeleteModal}
          onCancel={() => setShowDeleteModal(false)}
          footer={[
            <Button
              key="back"
              onClick={() => setShowDeleteModal(false)}
              style={{ background: "#F5F5F5", borderColor: "#F5F5F5" }}
            >
              Cancel
            </Button>,
            <Button
              key="submit"
              type="primary"
              onClick={() => {
                if (customer_id) {
                  setShowDeleteModal(false);
                  deleteCustomerMutation.mutate(customer_id);
                }
              }}
              style={{ background: "#C3986B", borderColor: "#C3986B" }}
            >
              Confirm Delete
            </Button>,
          ]}
        >
          <p>
            Are you sure you want to delete this customer? This action cannot be
            undone and will cancel all of the customer&apos;s current
            subscriptions without billing.
          </p>
        </Modal>
      )}
    </PageLayout>
  );
}

export default CustomerDetail;
