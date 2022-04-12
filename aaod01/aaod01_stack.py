from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct


class Aaod01Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_name="Aaod01")

        cluster = ecs.Cluster(self, "Cluster",
                              cluster_name="Aaod01",
                              vpc=vpc)

        container_instance_role = iam.Role(
            self, "ECSInstanceRole",
            role_name="Aaod01ECSInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonEC2ContainerServiceforEC2Role"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "/AmazonSSMManagedInstanceCore")
            ]
        )

        auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
                                                          auto_scaling_group_name="Aaod01",
                                                          vpc=vpc,
                                                          instance_type=ec2.InstanceType(
                                                              "t2.micro"),
                                                          role=container_instance_role,
                                                          machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
                                                          min_capacity=0,
                                                          max_capacity=10,
                                                          )

        cluster.add_asg_capacity_provider(ecs.AsgCapacityProvider(self, "AsgCapacityProvider", capacity_provider_name="Aaod01",
                                                                  auto_scaling_group=auto_scaling_group,
                                                                  enable_managed_scaling=True))

        task_role = iam.Role.from_role_name(
            self, "EcsTaskExecutionRole", role_name="ecsTaskExecutionRole")

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "FargateService01",
                                                           service_name="FargateService01",
                                                           cluster=cluster,
                                                           memory_limit_mib=1024,
                                                           desired_count=3,
                                                           cpu=512,
                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image=ecs.ContainerImage.from_registry(
                                                                   "amazon/amazon-ecs-sample")
                                                           )
                                                           )

        ecs_patterns.ApplicationLoadBalancedEc2Service(self, "EC2Service01",
                                                       service_name="EC2Service01",
                                                       cluster=cluster,
                                                       memory_limit_mib=1024,
                                                       desired_count=3,
                                                       cpu=512,
                                                       task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                           image=ecs.ContainerImage.from_registry(
                                                               "amazon/amazon-ecs-sample"),
                                                           task_role=task_role
                                                       )
                                                       )
