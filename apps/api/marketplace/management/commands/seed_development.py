import json
import os
from datetime import timedelta
from uuid import uuid4
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
import pyotp
from marketplace.models import (
    Auction,
    Branch,
    Inspection,
    Lead,
    Membership,
    Organization,
    Record,
    Revision,
    Slot,
    Taxonomy,
    User,
    Vehicle,
)


class Command(BaseCommand):
    help = "Create explicitly fictional, development-only records. Never runs automatically in production."

    @transaction.atomic
    def handle(self, **options):
        if not settings.DEVELOPMENT:
            raise CommandError("Development fixtures are forbidden in this environment")
        password = os.environ.get("SEED_PASSWORD", "Development-only-2026!")
        accounts = {
            "seller": ["ROLE-002", "ROLE-003"],
            "dealer": ["ROLE-004", "ROLE-005"],
            "branch": ["ROLE-006"],
            "inspector": ["ROLE-007"],
            "reviewer": ["ROLE-008"],
            "pricing": ["ROLE-009"],
            "auction": ["ROLE-010"],
            "support": ["ROLE-011"],
            "legal": ["ROLE-012"],
            "finance": ["ROLE-013"],
            "approver": ["ROLE-014"],
            "editor": ["ROLE-015"],
            "publisher": ["ROLE-015"],
            "admin": ["ROLE-016"],
            "analyst": ["ROLE-017"],
            "risk": ["ROLE-019"],
            "logistics": ["ROLE-020"],
            "inventory": ["ROLE-021"],
            "claims": ["ROLE-022"],
            "privacy": ["ROLE-023"],
            "credit": ["ROLE-024"],
            "growth": ["ROLE-025"],
            "policy": ["ROLE-026"],
        }
        users = {}
        credentials = []
        for name, roles in accounts.items():
            email = name + "@example.test"
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": "Development " + name.title(),
                    "roles": roles,
                    "contact_verified": True,
                },
            )
            if created:
                user.set_password(password)
                if name not in ["seller", "dealer"]:
                    user.totp_secret = pyotp.random_base32()
                user.save()
            users[name] = user
            credentials.append(
                {"username": email, "password": password, "totp_secret": user.totp_secret}
            )
        branch, _ = Branch.objects.get_or_create(
            slug="riverside-studio",
            defaults={
                "name": "Riverside Studio",
                "city": "Development City",
                "address": "100 Example Avenue — fictional development location",
                "timezone": "Europe/London",
            },
        )
        for name, user in users.items():
            if name not in ["seller", "dealer"]:
                branch.employees.add(user)
        org, _ = Organization.objects.get_or_create(
            registration_number="DEV-001",
            defaults={
                "legal_name": "Example Motors (development)",
                "jurisdiction": "EXAMPLE",
                "status": "active",
            },
        )
        Membership.objects.get_or_create(
            user=users["dealer"], organization=org, defaults={"can_bid": True}
        )
        policy, _ = Record.objects.get_or_create(
            kind="Policy",
            data__seed_key="auction-v1",
            defaults={
                "owner": users["admin"],
                "prepared_by": users["admin"],
                "reviewed_by": users["policy"],
                "status": "approved",
                "data": {
                    "seed_key": "auction-v1",
                    "type": "auction",
                    "content": {
                        "currency": "EUR",
                        "starting_minor": 1000000,
                        "increment_minor": 10000,
                        "reserve_minor": None,
                        "seller_response_hours": 24,
                    },
                },
            },
        )
        points = [
            {
                "id": str(uuid4()),
                "code": code,
                "section": section,
                "label": label,
                "required": True,
                "allowed_results": ["pass", "defect", "not_applicable", "unknown"],
                "evidence_required_on_defect": True,
                "guidance": "Record actual observed condition; explain anything not inspected.",
            }
            for code, section, label in [
                ("IDENTITY", "Identity", "Vehicle identity matches supplied records"),
                ("BODY", "Exterior", "Body and paint condition"),
                ("BRAKES", "Mechanical", "Brake system condition"),
                ("ENGINE", "Mechanical", "Powertrain condition"),
                ("CABIN", "Interior", "Cabin and safety equipment"),
            ]
        ]
        template, _ = Record.objects.get_or_create(
            kind="InspectionTemplate",
            data__seed_key="checklist-v1",
            defaults={
                "owner": users["reviewer"],
                "prepared_by": users["reviewer"],
                "status": "approved",
                "data": {"seed_key": "checklist-v1", "jurisdiction": "EXAMPLE", "points": points},
            },
        )
        makes = [
            ("Volvo", "XC60", 2022, 42500, 3290000, "SUV", "hybrid"),
            ("BMW", "320i", 2021, 58000, 2890000, "Saloon", "petrol"),
            ("Mercedes-Benz", "C200", 2022, 31000, 3590000, "Saloon", "petrol"),
            ("Audi", "Q5", 2020, 62500, 2690000, "SUV", "diesel"),
            ("Volkswagen", "Golf", 2023, 17000, 2390000, "Hatchback", "petrol"),
            ("Toyota", "RAV4", 2022, 35500, 3090000, "SUV", "hybrid"),
        ]
        vehicles = []
        for idx, (make_name, model_name, year, mileage, price, body, fuel) in enumerate(makes):
            make, _ = Taxonomy.objects.get_or_create(name=make_name, kind="make")
            model, _ = Taxonomy.objects.get_or_create(name=model_name, kind="model", parent=make)
            v, _ = Vehicle.objects.get_or_create(
                owner=users["seller"],
                make=make,
                model=model,
                year=year,
                defaults={
                    "mileage": mileage,
                    "details": {
                        "body_type": body,
                        "transmission": "automatic",
                        "fuel_type": fuel,
                        "media": [
                            {
                                "url": f"/vehicles/car-{idx % 3}.svg",
                                "alt": f"Representative illustration for development {make_name} {model_name}; not an actual vehicle photograph",
                                "width": 960,
                                "height": 600,
                            }
                        ],
                    },
                },
            )
            vehicles.append(v)
            Record.objects.get_or_create(
                kind="VehicleListing",
                vehicle=v,
                defaults={
                    "owner": users["inventory"],
                    "prepared_by": users["inventory"],
                    "branch": branch,
                    "status": "available",
                    "data": {
                        "title": f"{year} {make_name} {model_name}",
                        "slug": f"{make_name.lower()}-{model_name.lower()}-{year}".replace(
                            " ", "-"
                        ),
                        "asking_minor": price,
                        "currency": "EUR",
                        "region_name": "Development City",
                        "condition_summary": "Fictional development listing. Illustrative artwork; arrange inspection before any decision.",
                        "published_at": timezone.now().isoformat().replace("+00:00", "Z"),
                    },
                },
            )
        lead, _ = Lead.objects.get_or_create(
            vehicle=vehicles[0],
            defaults={
                "owner": users["seller"],
                "assigned_to": users["support"],
                "status": "eligible",
                "contact": {"email": users["seller"].email},
                "consent": {"notice_version": "development-v1"},
            },
        )
        base = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(
            days=1
        )
        for day in range(5):
            for hour in [0, 1, 2, 4, 5]:
                start = base + timedelta(days=day, hours=hour)
                Slot.objects.get_or_create(
                    branch=branch,
                    starts_at=start,
                    defaults={"ends_at": start + timedelta(minutes=45), "capacity": 2},
                )
        # Separate auction vehicle: never simultaneously advertised as consumer-available.
        make, model = vehicles[0].make, vehicles[0].model
        av, _ = Vehicle.objects.get_or_create(
            owner=users["seller"],
            make=make,
            model=model,
            year=2024,
            defaults={"mileage": 12000, "channel": "auction", "details": vehicles[0].details},
        )
        i, _ = Inspection.objects.get_or_create(
            vehicle=av,
            defaults={
                "branch": branch,
                "inspector": users["inspector"],
                "template": template,
                "status": "published",
            },
        )
        findings = [{"point_id": p["id"], "result": "pass"} for p in template.data["points"]]
        rev, _ = Revision.objects.get_or_create(
            inspection=i,
            number=1,
            defaults={
                "author": users["inspector"],
                "reviewer": users["reviewer"],
                "status": "published",
                "findings": findings,
                "checksum": "a" * 64,
                "published_at": timezone.now(),
            },
        )
        Auction.objects.get_or_create(
            vehicle=av,
            defaults={
                "report": rev,
                "policy": policy,
                "status": "open",
                "starts_at": timezone.now() - timedelta(hours=1),
                "closes_at": timezone.now() + timedelta(hours=12),
                "offer_expires_at": timezone.now() + timedelta(hours=36),
                "currency": "EUR",
                "starting_minor": 1000000,
                "increment_minor": 10000,
            },
        )
        for slug, title, text in [
            (
                "how-it-works",
                "A clearer road to your next car",
                "An inspection, a transparent offer and a team to guide each step. Development installation: all marketplace examples are fictional.",
            ),
            (
                "selling-guide",
                "Your guide to selling with confidence",
                "Prepare your vehicle records, choose an inspection appointment, and review each offer before accepting. A winning auction bid is separate from a completed sale.",
            ),
        ]:
            Record.objects.get_or_create(
                kind="Content",
                data__content__slug=slug,
                defaults={
                    "owner": users["editor"],
                    "prepared_by": users["editor"],
                    "reviewed_by": users["publisher"],
                    "status": "published",
                    "data": {
                        "revision_id": str(uuid4()),
                        "published_at": timezone.now().isoformat().replace("+00:00", "Z"),
                        "content": {
                            "slug": slug,
                            "title": title,
                            "blocks": [{"kind": "paragraph", "text": text}],
                            "canonical_path": "/journal/" + slug,
                            "source_urls": [],
                            "review_at": (timezone.now() + timedelta(days=90))
                            .isoformat()
                            .replace("+00:00", "Z"),
                            "indexable": True,
                        },
                    },
                },
            )
        out = settings.BASE_DIR / ".local" / "development-accounts.json"
        out.write_text(json.dumps(credentials, indent=2))
        out.chmod(0o600)
        self.stdout.write(f"Development fixtures ready; credentials stored privately in {out}")
