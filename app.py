#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aaod01.aaod01_stack import Aaod01Stack
from aaod01.aaod01_vpc_stack import Aaod01VpcStack

account='X'
region='us-west-2'

app = cdk.App()
Aaod01VpcStack(app, "Aaod01VpcStack",
            env=cdk.Environment(account=account, region=region),
            )
Aaod01Stack(app, "Aaod01Stack",
            env=cdk.Environment(account=account, region=region),
            )

app.synth()
