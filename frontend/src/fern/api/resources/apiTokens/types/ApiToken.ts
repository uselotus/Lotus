/**
 * This file was auto-generated by Fern from our API Definition.
 */

export interface ApiToken {
  /** A free-form name for the API key. Need not be unique. 50 characters max. */
  name?: string;
  prefix: string;
  /** Once API key expires, clients cannot use it anymore. */
  expiryDate?: string;
  created: string;
}
