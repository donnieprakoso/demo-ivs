from constructs import Construct
import aws_cdk as _cdk
import os
from aws_cdk import (
    App, Stack,
    aws_ivs as ivs,
    aws_secretsmanager as secrets_manager,
    aws_apigateway as _ag,
    aws_lambda as _lambda,

)


class IvsChannel(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create secrets into AWS Secrets Manager so we can store the private key later

        private_key_secret = secrets_manager.Secret(self, "{}-secret-private-key".format(id),
                                                    secret_name="{}-secret-private-key".format(
                                                        id)
                                                    )
        # Register public key pair file into Amazon IVS
        public_key_pair_file = self.node.try_get_context(
            "publicKeyPair")

        public_key_pair_string = ""
        with open(public_key_pair_file, 'r') as f:
            public_key_pair_string = f.read()

        playback_key = ivs.CfnPlaybackKeyPair(
            self, "{}-keypair".format(id), name="{}-keypair".format(id), public_key_material=public_key_pair_string)
        ivs_channel = ivs.CfnChannel(self, "{}-channel".format(id),
                                     authorized=True,
                                     latency_mode="LOW",
                                     name=id,
                                     recording_configuration_arn="",
                                     type="STANDARD"
                                     )

        ivs_stream_key = ivs.CfnStreamKey(self, "{}-streamkey".format(id),
                                          channel_arn=ivs_channel.attr_arn,
                                          )

        # Define Lambda function
        fnLambda_signRequests = _lambda.Function(
            self,
            "{}-function-signrequest".format(id),
            code=_lambda.AssetCode("../lambda-functions/sign-requests"),
            handler="app.handler",
            timeout=_cdk.Duration.minutes(2),
            runtime=_lambda.Runtime.PYTHON_3_8)
        fnLambda_signRequests.add_environment(
            "SECRET_PRIVATE_KEY", private_key_secret.secret_arn)
        fnLambda_signRequests.add_environment(
            "IVS_CHANNEL_ARN", ivs_channel.attr_arn)

        private_key_secret.grant_read(fnLambda_signRequests)

        # Integrate with API Gateway
        api = _ag.RestApi(
            self,
            id="{}-api-gateway".format(id),
            default_cors_preflight_options=_ag.CorsOptions(
                allow_methods=['ANY'],
                allow_origins=['*'],
                allow_headers=['Access-Control-Allow-Origin',
                               'Access-Control-Allow-Headers', 'Content-Type']
            )
        )
        int_signRequests = _ag.LambdaIntegration(fnLambda_signRequests)

        res_data = api.root.add_resource('sign')
        res_data.add_method('GET', int_signRequests)

        # Outputs
        _cdk.CfnOutput(self,
                       "{}-output-secretmanager-arn".format(id),
                       value=private_key_secret.secret_arn,
                       export_name="{}-secretmanager-arn".format(id))

        _cdk.CfnOutput(self,
                       "{}-output-channel-arn".format(id),
                       value=ivs_channel.attr_arn,
                       export_name="{}-channel-arn".format(id))

        _cdk.CfnOutput(self,
                       "{}-output-channel-ingest".format(id),
                       value=ivs_channel.attr_ingest_endpoint,
                       export_name="{}-channel-ingest".format(id))

        _cdk.CfnOutput(self,
                       "{}-output-channel-playback".format(id),
                       value=ivs_channel.attr_playback_url,
                       export_name="{}-channel-playback".format(id))

        _cdk.CfnOutput(self,
                       "{}-output-stream-key".format(id),
                       value=ivs_stream_key.attr_value,
                       export_name="{}-stream-key".format(id))

        _cdk.CfnOutput(self,
                       "{}-output-api-gateway".format(id),
                       value=api.url,
                       export_name="{}-api-gateway".format(id))


app = App()

env = _cdk.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1")
IvsChannel(app, "demo2-private-channel", env=env)
app.synth()
