#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aaod01.aaod01_stack import Aaod01Stack


app = cdk.App()
Aaod01Stack(app, "Aaod01Stack",
            env=cdk.Environment(account='646297494209', region='us-west-2'),
            )

app.synth()
