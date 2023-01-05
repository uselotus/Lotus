// @ts-ignore
import React, { FC } from "react";
import "./PlanDetails.css";
import { FeatureType } from "../../../types/feature-type";
import { Typography } from "antd";

interface PlanFeaturesProps {
  features?: FeatureType[];
}

const PlanFeatures: FC<PlanFeaturesProps> = ({ features }) => {
  return (
    <div className="min-h-[200px] mt-4 min-w-[246px] p-8 cursor-pointer font-main rounded-sm bg-card  shadow-lg hover:shadow-neutral-400">
      <Typography.Title level={2}>Features</Typography.Title>
      <div className=" w-full h-[1.5px] mt-2 bg-card-divider mb-2" />
      <div className="grid gap-2 grid-cols-1 xl:grid-cols-2">
        {features && features.length > 0 ? (
          features.map((feature) => (
            <div className="pt-2 pb-4 bg-primary-50 mt-2  mb-2 p-4 min-h-[152px]">
              <div className="text-base text-card-text">
                <div>{feature.feature_name}</div>
              </div>
              <div className="text-card-grey">
                {feature.feature_description}
              </div>
            </div>
          ))
        ) : (
          <div className="text-card-grey">No features added</div>
        )}
      </div>
    </div>
  );
};
export default PlanFeatures;
