import React, { FC, useState, useEffect, useRef } from "react";

import {
  ProTable,
  ProFormInstance,
  ProColumns,
} from "@ant-design/pro-components";
import { Button, Tag, Tooltip } from "antd";
import { useNavigate } from "react-router-dom";
import { MetricType } from "../types/metric-type";
import { Metrics } from "../api/api";

const colorMap = new Map<string, string>([
  ["count", "green"],
  ["sum", "blue"],
  ["max", "pink"],
]);

interface Props {
  metricArray: MetricType[];
}

const MetricTable: FC<Props> = ({ metricArray }) => {
  const navigate = useNavigate();
  const formRef = useRef<ProFormInstance>();

  const columns: ProColumns<MetricType>[] = [
    {
      title: "Metric Name",
      width: 150,
      dataIndex: "billable_metric_name",
      align: "left",
    },
    {
      title: "Type",
      width: 100,
      dataIndex: "metric_type",
      align: "left",
    },
    {
      title: "Event Name",
      width: 120,
      dataIndex: "event_name",
      align: "left",
    },
    {
      title: "Aggregation Type",
      width: 120,
      dataIndex: "aggregation_type",
      render: (_, record) => (
        <Tag color={colorMap.get(record.aggregation_type)}>
          {record.aggregation_type}
        </Tag>
      ),
    },
    {
      title: "Property Name",
      width: 120,
      dataIndex: "property_name",
      align: "left",
    },
    // {
    //   title: "Actions",
    //   align: "right",
    //   valueType: "option",
    //   render: (_, record) => [
    //     <a
    //       key="delete"
    //       onClick={() => {
    //         const tableDataSource = formRef.current?.getFieldValue(
    //           "table"
    //         ) as MetricType[];
    //         formRef.current?.setFieldsValue({
    //           table: tableDataSource.filter((item) => item.id !== record?.id),
    //         });
    //       }}
    //     >
    //       <DeleteOutlined />
    //     </a>,
    //   ],
    // },
  ];

  const handleDelete = (id: number) => {
    Metrics.deleteMetric(id).then((res) => {});
  };

  return (
    <ProTable<MetricType>
      columns={columns}
      dataSource={metricArray}
      toolBarRender={false}
      rowKey="customer_id"
      formRef={formRef}
      search={false}
      className="w-full"
      pagination={{
        showTotal: (total, range) => (
          <div>{`${range[0]}-${range[1]} of ${total} total items`}</div>
        ),
      }}
      options={false}
    />
  );
};

export default MetricTable;
