import boto3
from moto import mock_ec2


@mock_ec2
def test_elastic_network_interfaces_get_by_vpc_id():
    ec2_resource = boto3.resource("ec2", region_name="us-east-1")
    ec2_client = boto3.client("ec2", region_name="us-east-1")

    vpc = ec2_resource.create_vpc(CidrBlock="10.0.0.0/16")
    subnet = ec2_resource.create_subnet(
        VpcId=vpc.id,
        CidrBlock="10.0.0.0/24",
        AvailabilityZone="us-east-1a"
    )
    ec2_net_interface1 = ec2_resource.create_network_interface(
        SubnetId=subnet.id,
        PrivateIpAddress="10.0.10.5"
    )

    # The status of the new interface should be "available
    waiter = ec2_client.get_waiter("network_interface_available")
    waiter.wait(NetworkInterfaceIds=[ec2_net_interface1.id])
