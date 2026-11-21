import { Duration, RemovalPolicy } from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as logs from "aws-cdk-lib/aws-logs";
import type { Construct } from "constructs";
import * as path from "node:path";

export function createBackendApi(
  scope: Construct,
  allowedOrigin: string
): lambda.Function {
  const logGroup = new logs.LogGroup(scope, "BackendApiLogs", {
    retention: logs.RetentionDays.ONE_WEEK,
    removalPolicy: RemovalPolicy.RETAIN
  });

  return new lambda.Function(scope, "BackendApi", {
    runtime: lambda.Runtime.PYTHON_3_14,
    architecture: lambda.Architecture.X86_64,
    handler: "app.handler.handler",

    code: lambda.Code.fromAsset(
      path.join(__dirname, "../../../backend/build/lambda")
    ),

    memorySize: 512,
    timeout: Duration.seconds(10),
    reservedConcurrentExecutions: 2,

    logGroup,

    environment: {
      ALLOWED_ORIGINS: allowedOrigin
    }
  });
}
