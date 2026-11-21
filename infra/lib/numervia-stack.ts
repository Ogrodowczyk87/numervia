import {
  CfnOutput,
  RemovalPolicy,
  Stack,
  type StackProps
} from "aws-cdk-lib";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
import * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";
import * as path from "node:path";
import { createFrontendCachePolicy } from "./frontend-cache";
import { createBackendApi } from "./backend-api";
import { createBackendUrl } from "./backend-url";
import { createContentStateBucket } from "./content-state";
import { grantContentStateRead } from "./content-state-access";

export class NumerviaStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const contentStateBucket = createContentStateBucket(this);

    const frontendBucket = new s3.Bucket(this, "FrontendBucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
      encryption: s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
      removalPolicy: RemovalPolicy.RETAIN
    });

    const routeRewrite = new cloudfront.Function(this, "FrontendRoutes", {
      runtime: cloudfront.FunctionRuntime.JS_2_0,
      code: cloudfront.FunctionCode.fromFile({
        filePath: path.join(__dirname, "../../functions/frontend-routes.js")
      })
    });

    const frontendCachePolicy = createFrontendCachePolicy(this);

    const distribution = new cloudfront.Distribution(
      this,
      "FrontendDistribution",
      {
        defaultRootObject: "index.html",
        priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(
            frontendBucket
          ),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD,
          compress: true,
          cachePolicy: frontendCachePolicy,
          functionAssociations: [
            {
              function: routeRewrite,
              eventType: cloudfront.FunctionEventType.VIEWER_REQUEST
            }
          ]
        }
      }
    );

    const backendApi = createBackendApi(
      this,
      `https://${distribution.distributionDomainName}`
    );

    grantContentStateRead(contentStateBucket, backendApi);

    const backendUrl = createBackendUrl(backendApi);

    new CfnOutput(this, "BackendUrl", {
      value: backendUrl.url
    });

    new CfnOutput(this, "FrontendUrl", {
      value: `https://${distribution.distributionDomainName}`
    });
  }
}
