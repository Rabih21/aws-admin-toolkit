from datetime import date
from decimal import Decimal


def get_billing_report(session):
    """
    Retrieve the current month's AWS costs and group them
    by AWS service.

    Returns:
        {
            "start_date": str,
            "end_date": str,
            "total_cost": float,
            "currency": str,
            "services": [...]
        }
    """

    # AWS Cost Explorer uses the us-east-1 endpoint.
    cost_explorer = session.client(
        "ce",
        region_name="us-east-1"
    )

    today = date.today()

    # First day of the current month.
    start_date = today.replace(day=1)

    # Cost Explorer End date is exclusive.
    end_date = today

    try:

        response = cost_explorer.get_cost_and_usage(
            TimePeriod={
                "Start": start_date.isoformat(),
                "End": end_date.isoformat()
            },

            Granularity="MONTHLY",

            Metrics=[
                "UnblendedCost"
            ],

            GroupBy=[
                {
                    "Type": "DIMENSION",
                    "Key": "SERVICE"
                }
            ]
        )

        services = []

        total_cost = Decimal("0")
        currency = "USD"

        for result in response.get("ResultsByTime", []):

            for group in result.get("Groups", []):

                keys = group.get("Keys", [])

                if keys:
                    service_name = keys[0]
                else:
                    service_name = "Unknown"

                cost_data = (
                    group
                    .get("Metrics", {})
                    .get("UnblendedCost", {})
                )

                amount = Decimal(
                    cost_data.get("Amount", "0")
                )

                unit = cost_data.get(
                    "Unit",
                    "USD"
                )

                total_cost += amount
                currency = unit

                services.append({
                    "service": service_name,
                    "cost": float(amount),
                    "currency": unit
                })

        # Highest cost first.
        services.sort(
            key=lambda service: service["cost"],
            reverse=True
        )

        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_cost": float(total_cost),
            "currency": currency,
            "services": services
        }

    except Exception as error:

        print(
            f"[ERROR] Could not retrieve AWS billing data: "
            f"{type(error).__name__}: {error}"
        )

        return None

def show_billing_report(report):
    """
    Display the AWS billing report.
    """

    print()
    print("=" * 70)
    print("AWS BILLING & COST REPORT")
    print("=" * 70)

    if not report:
        print()
        print("No billing data could be retrieved.")
        return

    print()
    print(
        f"Billing Period: "
        f"{report['start_date']} to {report['end_date']}"
    )

    print(
        f"Month-to-Date Cost: "
        f"{report['currency']} "
        f"{report['total_cost']:.2f}"
    )

    print()
    print("-" * 70)
    print("COST BY AWS SERVICE")
    print("-" * 70)

    services = report.get("services", [])

    if not services:
        print()
        print("No AWS service costs were found.")
        return

    print()
    print(
        f"{'AWS Service':<48}"
        f"{'Cost':>15}"
    )

    print("-" * 70)

    for service in services:

        service_name = service["service"]

        # Prevent extremely long AWS service names
        # from breaking the console layout.
        if len(service_name) > 46:
            service_name = service_name[:43] + "..."

        print(
            f"{service_name:<48}"
            f"{service['cost']:>10.2f} "
            f"{service['currency']}"
        )

    print("-" * 70)

    print(
        f"{'TOTAL':<48}"
        f"{report['total_cost']:>10.2f} "
        f"{report['currency']}"
    )

    print()

    highest_cost_service = services[0]

    print(
        f"Top Cost Service: "
        f"{highest_cost_service['service']} "
        f"({highest_cost_service['cost']:.2f} "
        f"{highest_cost_service['currency']})"
    )

    print()