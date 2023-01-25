/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../..";
import { LotusApi } from "../../../..";
import * as core from "../../../../core";

export const CustomerCreateRequest: core.serialization.ObjectSchema<
  serializers.CustomerCreateRequest.Raw,
  LotusApi.CustomerCreateRequest
> = core.serialization.object({
  customerName: core.serialization.property(
    "customer_name",
    core.serialization.string().optional()
  ),
  customerId: core.serialization.property(
    "customer_id",
    core.serialization.string()
  ),
  email: core.serialization.string(),
  paymentProvider: core.serialization.property(
    "payment_provider",
    core.serialization
      .lazy(async () => (await import("../../..")).PaymentProvider)
      .optional()
  ),
  paymentProviderId: core.serialization.property(
    "payment_provider_id",
    core.serialization.string().optional()
  ),
  metadata: core.serialization
    .record(core.serialization.string(), core.serialization.unknown())
    .optional(),
  defaultCurrencyCode: core.serialization.property(
    "default_currency_code",
    core.serialization.string().optional()
  ),
  address: core.serialization
    .lazyObject(async () => (await import("../../..")).Address)
    .optional(),
  taxRate: core.serialization.property(
    "tax_rate",
    core.serialization.number().optional()
  ),
});

export declare namespace CustomerCreateRequest {
  interface Raw {
    customer_name?: string | null;
    customer_id: string;
    email: string;
    payment_provider?: serializers.PaymentProvider.Raw | null;
    payment_provider_id?: string | null;
    metadata?: Record<string, unknown> | null;
    default_currency_code?: string | null;
    address?: serializers.Address.Raw | null;
    tax_rate?: number | null;
  }
}
