import { App } from "aws-cdk-lib";
import { NumerviaStack } from "../lib/numervia-stack";

const app = new App();

new NumerviaStack(app, "NumerviaStack",
    {
        env: {
            region: "eu-west-1"
        }
    }
)