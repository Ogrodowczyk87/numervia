import * as lambda from "aws-cdk-lib/aws-lambda";

export function createBackendUrl(
  backendApi: lambda.Function
): lambda.FunctionUrl {
  return backendApi.addFunctionUrl({
    authType: lambda.FunctionUrlAuthType.NONE
  });
}