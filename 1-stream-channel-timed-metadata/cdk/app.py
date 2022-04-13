from constructs import Construct
import aws_cdk as _cdk
import os
from aws_cdk import (
    App, Stack,
    aws_ivs as ivs
)


class IvsChannel(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
                
        ivs_channel = ivs.CfnChannel(self, "{}-channel".format(id),
            authorized=False,
            latency_mode="LOW",
            name="demo-ivs-metadata",
            recording_configuration_arn="",
            type="STANDARD"
        )
        
        ivs_stream_key = ivs.CfnStreamKey(self, "{}-streamkey".format(id),
            channel_arn=ivs_channel.attr_arn,
        )        

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


app = App()

env = _cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-east-1")
IvsChannel(app, "demo1-ivs-metadata", env=env)
app.synth()
