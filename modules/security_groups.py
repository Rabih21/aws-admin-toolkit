def get_sg_info(session, region):
    """
    Retrieve Security Groups from the selected AWS region
    and check their severity.
    """

    ec2 = session.client("ec2", region_name=region)
    findings = []

    try:
        response = ec2.describe_security_groups()

        for group in response.get("SecurityGroups", []):

            group_id = group.get("GroupId", "N/A")
            group_name = group.get("GroupName", "N/A")
            vpc_id = group.get("VpcId", "N/A")
            description = group.get("Description", "N/A")

            # Every inbound rule
            for rule in group.get("IpPermissions", []):

                protocol = rule.get("IpProtocol", "N/A")
                from_port = rule.get("FromPort", "N/A")
                to_port = rule.get("ToPort", "N/A")

                # IPv4 rules
                for ip_range in rule.get("IpRanges", []):

                    source = ip_range.get("CidrIp", "N/A")

                    if source == "0.0.0.0/0":

                        severity, service, message, recommendation = classify_rule(
                            protocol,
                            from_port,
                            to_port
                        )

                        findings.append({
                            "security_group_id": group_id,
                            "security_group_name": group_name,
                            "vpc_id": vpc_id,
                            "description": description,
                            "protocol": protocol,
                            "from_port": from_port,
                            "to_port": to_port,
                            "source": source,
                            "severity": severity,
                            "service": service,
                            "message": message,
                            "recommendation": recommendation
                        })

                # IPv6 rules
                for ip_range in rule.get("Ipv6Ranges", []):

                    source = ip_range.get("CidrIpv6", "N/A")

                    if source == "::/0":

                        severity, service, message, recommendation = classify_rule(
                            protocol,
                            from_port,
                            to_port
                        )

                        findings.append({
                            "security_group_id": group_id,
                            "security_group_name": group_name,
                            "vpc_id": vpc_id,
                            "description": description,
                            "protocol": protocol,
                            "from_port": from_port,
                            "to_port": to_port,
                            "source": source,
                            "severity": severity,
                            "service": service,
                            "message": message,
                            "recommendation": recommendation
                        })

        return findings

    except Exception as error:
        print(
            f"[ERROR] Could not retrieve Security Groups: "
            f"{type(error).__name__}: {error}"
        )

        return []

def classify_rule(protocol, from_port, to_port):

    # All traffic
    if protocol == "-1":
        return (
            "CRITICAL",
            "ALL TRAFFIC",
            "All traffic is publicly accessible.",
            "Restrict access to trusted IP addresses or Security Groups."
        )

    dangerous_ports = {
        22: (
            "SSH",
            "SSH is publicly accessible.",
            "Restrict SSH access to trusted administrator IP addresses."
        ),

        3389: (
            "RDP",
            "RDP is publicly accessible.",
            "Restrict RDP access to trusted administrator IP addresses."
        ),

        3306: (
            "MySQL",
            "MySQL is publicly accessible.",
            "Allow database access only from trusted application resources."
        ),

        5432: (
            "PostgreSQL",
            "PostgreSQL is publicly accessible.",
            "Allow database access only from trusted application resources."
        ),

        1433: (
            "Microsoft SQL Server",
            "Microsoft SQL Server is publicly accessible.",
            "Restrict database access to trusted resources."
        ),

        6379: (
            "Redis",
            "Redis is publicly accessible.",
            "Restrict Redis access to private trusted resources."
        )
    }

    # Check if a dangerous port exists within the rule range
    if isinstance(from_port, int) and isinstance(to_port, int):

        for port, details in dangerous_ports.items():

            if from_port <= port <= to_port:

                service, message, recommendation = details

                return (
                    "CRITICAL",
                    service,
                    message,
                    recommendation
                )

    # HTTP
    if from_port == 80 and to_port == 80:
        return (
            "INFO",
            "HTTP",
            "HTTP is publicly accessible.",
            "This may be expected for a public web server."
        )

    # HTTPS
    if from_port == 443 and to_port == 443:
        return (
            "INFO",
            "HTTPS",
            "HTTPS is publicly accessible.",
            "This may be expected for a public web application."
        )

    # Everything else publicly accessible
    return (
        "WARNING",
        "Other",
        f"Port range {from_port}-{to_port} is publicly accessible.",
        "Review whether public access is required."
    )