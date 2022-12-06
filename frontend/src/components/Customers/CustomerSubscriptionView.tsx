import React, { FC, useEffect, useState } from "react";
import { PlanType } from "../../types/plan-type";
import {
  Card,
  List,
  Form,
  Select,
  Button,
  Dropdown,
  Menu,
  Tag,
  Cascader,
} from "antd";
import type { DefaultOptionType } from "antd/es/cascader";
import {
  CreateSubscriptionType,
  TurnSubscriptionAutoRenewOffType,
  ChangeSubscriptionPlanType,
  CancelSubscriptionType,
} from "../../types/subscription-type";
//import the Customer type from the api.ts file
import dayjs from "dayjs";

import {
  CustomerDetailSubscription,
  DetailPlan,
} from "../../types/customer-type";
import DraftInvoice from "./DraftInvoice";

interface Props {
  customer_id: string;
  subscription: CustomerDetailSubscription;
  plans: PlanType[] | undefined;
  onAutoRenewOff: (
    params: object,
    props: TurnSubscriptionAutoRenewOffType
  ) => void;
  onCancel: (subscription_id: string, props: CancelSubscriptionType) => void;
  onPlanChange: (
    subscription_id: string,
    props: ChangeSubscriptionPlanType
  ) => void;
  onCreate: (props: CreateSubscriptionType) => void;
}

const filter = (inputValue: string, path: DefaultOptionType[]) =>
  (path[0].label as string).toLowerCase().indexOf(inputValue.toLowerCase()) >
  -1;

const displayRender = (labels: string[]) => labels[labels.length - 1];

interface PlanOption {
  value: string;
  label: string;
  children?: ChangeOption[];
  disabled?: boolean;
}

interface ChangeOption {
  value:
    | "change_subscription_plan"
    | "end_current_subscription_and_bill"
    | "end_current_subscription_dont_bill";
  label: string;
  disabled?: boolean;
}

const SubscriptionView: FC<Props> = ({
  customer_id,
  subscription,
  plans,
  onCancel,
  onAutoRenewOff,
  onPlanChange,
  onCreate,
}) => {
  const [selectedPlan, setSelectedPlan] = useState<string>();
  const [form] = Form.useForm();

  const [idtoPlan, setIDtoPlan] = useState<{ [key: string]: PlanType }>({});
  const [planList, setPlanList] =
    useState<{ label: string; value: string }[]>();

  const [subscriptionPlans, setSubscriptionPlans] = useState<DetailPlan[]>(
    subscription?.plans || []
  );

  const selectPlan = (plan_id: string) => {
    setSelectedPlan(plan_id);
  };

  const cancelAndBill = () => {
    onCancel(subscription.subscription_id, {
      bill_usage: true,
      flat_fee_behavior: "charge_full",
      invoicing_behavior_on_cancel: "bill_now",
    });
  };

  const cancelAndDontBill = () => {
    // onCancel(subscriptions[0].subscription_id, {
    //   bill_usage: false,
    //   flat_fee_behavior: "refund",
    //   invoicing_behavior
    // });
  };

  const turnAutoRenewOff = () => {
    // onAutoRenewOff(subscriptions[0].plan_version, {
    //   turn_off_auto_renew: true,
    // });
  };

  useEffect(() => {
    if (plans !== undefined) {
      const planMap = plans.reduce((acc, plan) => {
        acc[plan.plan_id] = plan;
        return acc;
      }, {} as { [key: number]: PlanType });
      setIDtoPlan(planMap);
      const newplanList: { label: string; value: string }[] = plans.reduce(
        (acc, plan) => {
          if (
            plan.target_customer === null ||
            plan.target_customer?.customer_id === customer_id
          ) {
            acc.push({ label: plan.plan_name, value: plan.plan_id });
          }
          return acc;
        },
        [] as { label: string; value: string }[]
      );
      setPlanList(newplanList);
    }
  }, [plans]);

  const cancelMenu = (
    <Menu
      items={[
        {
          label: <div onClick={() => cancelAndBill()}>Cancel and Bill Now</div>,
          key: "0",
        },
        {
          label: (
            <div onClick={() => cancelAndDontBill()}>Cancel And Refund</div>
          ),
          key: "1",
        },
        {
          label: <div onClick={() => turnAutoRenewOff()}>Cancel Renewal</div>,
          key: "2",
        },
      ]}
    />
  );

  const plansWithSwitchOptions = planList?.reduce((acc, plan) => {
    // if (plan.label !== subscriptions[0]?.billing_plan_name) {
    //   acc.push({
    //     label: plan.label,
    //     value: plan.value,
    //   } as PlanOption);
    // }
    return acc;
  }, [] as PlanOption[]);

  const onChange = (value: string[], selectedOptions: PlanOption[]) => {
    // onPlanChange(subscriptions[0].subscription_id, {
    //   replace_plan_id: selectedOptions[0].value,
    // });
  };

  const switchMenu = (
    <Cascader
      options={plansWithSwitchOptions}
      onChange={onChange}
      expandTrigger="hover"
      placeholder="Please select"
      showSearch={{ filter }}
      displayRender={displayRender}
      changeOnSelect
    />
  );

  const handleAttachPlanSubmit = () => {
    if (selectedPlan) {
      let plan = idtoPlan[selectedPlan];
      let props: CreateSubscriptionType = {
        customer_id: customer_id,
        plan_id: plan.plan_id,
        start_date: new Date().toISOString(),
        status: "active",
      };
      onCreate(props);
    }
    form.resetFields();
  };
  if (subscription === null) {
    return (
      <div className="flex flex-col items-center justify-center">
        <h2 className="mb-2 pb-4 pt-4 font-bold text-main">No Subscription</h2>
        <p className="font-bold">Please attach a Plan</p>
        <div className=" h-3/6">
          <Form
            onFinish={handleAttachPlanSubmit}
            form={form}
            name="create_subscription"
          >
            <Form.Item name="plan">
              <Select
                showSearch
                placeholder="Select a plan"
                onChange={selectPlan}
                options={planList}
                optionLabelProp="label"
              >
                {" "}
              </Select>
            </Form.Item>
            <Form.Item>
              <Button htmlType="submit">
                {" "}
                Attach Plan and Start Subscription
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>
    );
  }
  return (
    <div className="mt-auto">
      <h2 className="mb-2 pb-4 pt-4 font-bold text-main">Active Plans</h2>
      <div className="flex flex-col justify-center">
        <List>
          {subscriptionPlans.map((subPlan) => (
            <List.Item>
              <Card className=" bg-grey3 w-full">
                <div className="grid grid-cols-2 items-stretch">
                  <h2 className="font-main font-bold">
                    {subPlan.plan_detail.created_by}
                  </h2>
                  <div className="grid grid-cols-2 justify-center space-y-3">
                    <p>
                      {/* <b>Subscription Plan Filters: </b>{" "}
                      {subPlan.subscription_filters?.map((filter) => (
                        <span>
                          {filter.} : {filter.filter_value}
                        </span>
                      ))} */}
                    </p>
                    <p>
                      <b>Start Date:</b>{" "}
                      {dayjs(subPlan.start_date).format("YYYY/MM/DD HH:mm")}{" "}
                    </p>

                    <p>
                      <b>Renews:</b>{" "}
                      {subPlan.auto_renew ? (
                        <Tag color="green">Yes</Tag>
                      ) : (
                        <Tag color="red">No</Tag>
                      )}
                    </p>
                    <p>
                      <b>End Date:</b>{" "}
                      {dayjs(subPlan.end_date).format("YYYY/MM/DD HH:mm")}{" "}
                    </p>
                  </div>
                </div>
              </Card>
            </List.Item>
          ))}
        </List>
        <div className="grid grid-cols-2 w-full space-x-5 my-6">
          <Dropdown overlay={switchMenu} trigger={["click"]}>
            <Button>Switch Plan</Button>
          </Dropdown>
          <Dropdown overlay={cancelMenu} trigger={["click"]}>
            <Button>Cancel Subscription</Button>
          </Dropdown>
        </div>
        <DraftInvoice customer_id={customer_id} />
      </div>
    </div>
  );
};

export default SubscriptionView;
