from aws_utils.session import get_aws_session
from modules.ec2_inventory import get_ec2_inventory


def print_header():
    print("=" * 60)
    print("              AWS ADMIN UTILITY TOOLKIT")
    print("=" * 60)


def show_ec2_inventory(aws_info):

    session = aws_info["session"]
    region = aws_info["region"]

    print()
    print("=" * 60)
    print("EC2 INVENTORY REPORT")
    print("=" * 60)

    inventory = get_ec2_inventory(session, region)

    if not inventory:
        print("No EC2 instances found.")
        return

    for instance in inventory:

        print()
        print("-" * 60)

        print(f"Name:              {instance['name']}")
        print(f"Instance ID:       {instance['instance_id']}")
        print(f"State:             {instance['state']}")
        print(f"Instance Type:     {instance['instance_type']}")
        print(f"Availability Zone: {instance['availability_zone']}")

        print()
        print("NETWORK")

        print(f"Private IP:        {instance['private_ip']}")
        print(f"Public IP:         {instance['public_ip']}")
        print(f"VPC ID:            {instance['vpc_id']}")
        print(f"Subnet ID:         {instance['subnet_id']}")

        print()
        print("INSTANCE")

        print(f"AMI ID:            {instance['image_id']}")
        print(f"Launch Time:       {instance['launch_time']}")

        print()
        print("SECURITY GROUPS")

        if instance["security_groups"]:

            for sg in instance["security_groups"]:
                print(
                    f"  - {sg['name']} "
                    f"({sg['id']})"
                )

        else:
            print("  None")

    print()
    print("=" * 60)

    print(
        f"Total EC2 Instances: "
        f"{len(inventory)}"
    )

    print("=" * 60)


def main():

    print_header()

    print()
    print("Connecting to AWS...")

    aws_info = get_aws_session()

    if aws_info is None:
        return

    print()
    print("[SUCCESS] Connected to AWS")

    print(f"Account ID: {aws_info['account_id']}")
    print(f"Identity:   {aws_info['arn']}")
    print(f"Region:     {aws_info['region']}")

    while True:

        print()
        print("=" * 60)

        print("[1] EC2 Inventory Reporter")
        print("[2] Security Group Exposure Scanner")
        print("[3] Unused EBS Volume Detector")
        print("[0] Exit")

        print("=" * 60)

        choice = input("Select an option: ")

        if choice == "1":

            show_ec2_inventory(aws_info)

        elif choice == "2":

            print()
            print("Security Group Scanner coming next.")

        elif choice == "3":

            print()
            print("Unused EBS Detector coming next.")

        elif choice == "0":

            print()
            print("Goodbye.")
            break

        else:

            print()
            print("Invalid option.")


if __name__ == "__main__":
    main()