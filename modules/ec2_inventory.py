def get_ec2_inventory(session, region):
    """
    Retrieve EC2 instances from the selected AWS region.
    """

    ec2 = session.client("ec2", region_name=region)

    inventory = []

    try:
        response = ec2.describe_instances()

        for reservation in response.get("Reservations", []):

            for instance in reservation.get("Instances", []):

                name = "N/A"

                # Get EC2 Name tag safely
                for tag in instance.get("Tags", []):
                    if tag.get("Key") == "Name":
                        name = tag.get("Value", "N/A")

                security_groups = []

                for sg in instance.get("SecurityGroups", []):
                    security_groups.append({
                        "name": sg.get("GroupName", "N/A"),
                        "id": sg.get("GroupId", "N/A")
                    })

                instance_data = {
                    "instance_id": instance.get("InstanceId", "N/A"),
                    "name": name,
                    "state": instance.get(
                        "State", {}
                    ).get(
                        "Name", "N/A"
                    ),

                    "instance_type": instance.get(
                        "InstanceType", "N/A"
                    ),

                    "availability_zone": instance.get(
                        "Placement", {}
                    ).get(
                        "AvailabilityZone", "N/A"
                    ),

                    "private_ip": instance.get(
                        "PrivateIpAddress", "N/A"
                    ),

                    "public_ip": instance.get(
                        "PublicIpAddress", "N/A"
                    ),

                    "vpc_id": instance.get(
                        "VpcId", "N/A"
                    ),

                    "subnet_id": instance.get(
                        "SubnetId", "N/A"
                    ),

                    "image_id": instance.get(
                        "ImageId", "N/A"
                    ),

                    "security_groups": security_groups,

                    "launch_time": str(
                        instance.get("LaunchTime", "N/A")
                    )
                }

                inventory.append(instance_data)

        return inventory

    except Exception as error:
        print(
            f"[ERROR] Could not retrieve EC2 instances: "
            f"{type(error).__name__}: {error}"
        )

        return []