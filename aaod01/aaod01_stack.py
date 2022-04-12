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
                    "AmazonSSMManagedInstanceCore")
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

        capacity_provider = ecs.AsgCapacityProvider(self, "AsgCapacityProvider", capacity_provider_name="Aaod01",
                                                    auto_scaling_group=auto_scaling_group,
                                                    enable_managed_scaling=True)

        cluster.add_asg_capacity_provider(capacity_provider)

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

        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")

        task_definition.add_container("web",
                                      image=ecs.ContainerImage.from_registry(
                                          "amazon/amazon-ecs-sample"),
                                      memory_reservation_mib=256,
                                      port_mappings=[
                                          ecs.PortMapping(container_port=80)]
                                      )

        ecs.Ec2Service(self, "EC2Service",
                       cluster=cluster,
                       task_definition=task_definition,
                       desired_count=3,
                       capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                           capacity_provider=capacity_provider.capacity_provider_name,
                           weight=1
                       )
                       ]
                       )
