import * as iam from "aws-cdk-lib/aws-iam";
import type * as lambda from "aws-cdk-lib/aws-lambda";
import type * as s3 from "aws-cdk-lib/aws-s3";

export const NEWS_STATE_KEY = "news/state.json";
export const VIDEOS_STATE_KEY = "videos/state.json";

export function grantContentStateRead(
  bucket: s3.IBucket,
  backendApi: lambda.Function
): void {
  backendApi.addToRolePolicy(new iam.PolicyStatement({
    actions: ["s3:GetObject"],
    resources: [
      bucket.arnForObjects(NEWS_STATE_KEY),
      bucket.arnForObjects(VIDEOS_STATE_KEY)
    ]
  }));
}
