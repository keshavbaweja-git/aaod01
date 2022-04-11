from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2
)
from constructs import Construct


class Aaod01Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC",
                      cidr="10.0.0.0/16")

        cluster = ecs.Cluster(self, "Cluster",
                              vpc=vpc)

        auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
                                                          vpc=vpc,
                                                          instance_type=ec2.InstanceType(
                                                              "t2.micro"),
                                                          machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
                                                          min_capacity=0,
                                                          max_capacity=10
                                                          )

        cluster.add_asg_capacity_provider(ecs.AsgCapacityProvider(self, "AsgCapacityProvider",
                                                                  auto_scaling_group=auto_scaling_group,
                                                                  enable_managed_scaling=True))

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service01",
                                                           cluster=cluster,
                                                           memory_limit_mib=1024,
                                                           desired_count=3,
                                                           cpu=512,
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=ecs.ContainerImage.from_registry(
                                                                   "amazon/amazon-ecs-sample")
                                                           )
                                                           )
