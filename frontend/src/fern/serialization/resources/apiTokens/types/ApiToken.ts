/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../..";
import { LotusApi } from "../../../..";
import * as core from "../../../../core";

export const ApiToken: core.serialization.ObjectSchema<
  serializers.ApiToken.Raw,
  LotusApi.ApiToken
> = core.serialization.object({
  name: core.serialization.string().optional(),
  prefix: core.serialization.string(),
  expiryDate: core.serialization.property(
    "expiry_date",
    core.serialization.string().optional()
  ),
  created: core.serialization.string(),
});

export declare namespace ApiToken {
  interface Raw {
    name?: string | null;
    prefix: string;
    expiry_date?: string | null;
    created: string;
  }
}
