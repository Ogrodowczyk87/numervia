import { Duration } from "aws-cdk-lib";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import type { Construct } from "constructs";

export function createFrontendCachePolicy(
  scope: Construct
): cloudfront.CachePolicy {
  return new cloudfront.CachePolicy(scope, "FrontendCachePolicy", {
    comment: "Respect cache headers set on frontend files",

    minTtl: Duration.seconds(0),
    defaultTtl: Duration.seconds(0),
    maxTtl: Duration.days(365),

    cookieBehavior: cloudfront.CacheCookieBehavior.none(),
    headerBehavior: cloudfront.CacheHeaderBehavior.none(),
    queryStringBehavior: cloudfront.CacheQueryStringBehavior.none(),

    enableAcceptEncodingGzip: true,
    enableAcceptEncodingBrotli: true
  });
}