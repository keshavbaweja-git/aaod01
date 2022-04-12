from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class Aaod01VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ec2.Vpc(self, "VPC",
                      vpc_name="Aaod01",
                      cidr="10.0.0.0/16")
