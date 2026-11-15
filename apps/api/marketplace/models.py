import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.JSONField(default=list)
    contact_verified = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=64, blank=True)
    security_epoch = models.PositiveIntegerField(default=1)


class Entity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Branch(Entity):
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    timezone = models.CharField(max_length=64, default="UTC")
    active = models.BooleanField(default=True)
    employees = models.ManyToManyField(User, related_name="branches")


class Organization(Entity):
    legal_name = models.CharField(max_length=200)
    jurisdiction = models.CharField(max_length=64)
    registration_number = models.CharField(max_length=100)
    status = models.CharField(max_length=32, default="pending")


class Membership(Entity):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    can_bid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "organization"], name="one_dealer_membership")
        ]


class Taxonomy(Entity):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    kind = models.CharField(max_length=16)


class Vehicle(Entity):
    make = models.ForeignKey(Taxonomy, on_delete=models.PROTECT, related_name="make_vehicles")
    model = models.ForeignKey(Taxonomy, on_delete=models.PROTECT, related_name="model_vehicles")
    year = models.PositiveSmallIntegerField()
    mileage = models.PositiveIntegerField()
    mileage_unit = models.CharField(max_length=2, default="km")
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    channel = models.CharField(max_length=20, blank=True)
    details = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(year__gte=1886, year__lte=2100), name="vehicle_year_range"
            )
        ]


class Lead(Entity):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.PROTECT)
    status = models.CharField(max_length=32, default="draft", db_index=True)
    contact = models.JSONField(default=dict)
    consent = models.JSONField(default=dict)
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="assigned_leads"
    )


class Slot(Entity):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity = models.PositiveSmallIntegerField(default=1)
    reserved = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(ends_at__gt=models.F("starts_at")), name="positive_slot_interval"
            ),
            models.CheckConstraint(
                condition=Q(reserved__lte=models.F("capacity")), name="slot_within_capacity"
            ),
        ]
        indexes = [models.Index(fields=["branch", "starts_at"])]


class Appointment(Entity):
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT)
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    status = models.CharField(max_length=32, default="confirmed", db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lead"],
                condition=Q(status__in=["confirmed", "checked_in"]),
                name="one_active_visit_per_lead",
            )
        ]


class Record(Entity):
    """Versioned operational aggregates; kind-specific guards live in domain services."""

    kind = models.CharField(max_length=64, db_index=True)
    status = models.CharField(max_length=32, default="draft", db_index=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="records")
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.PROTECT)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    data = models.JSONField(default=dict)
    prepared_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="prepared_records")
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="reviewed_records"
    )

    class Meta:
        indexes = [
            models.Index(fields=["kind", "owner", "status"]),
            models.Index(fields=["branch", "kind", "status"]),
        ]


class Inspection(Entity):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    inspector = models.ForeignKey(User, on_delete=models.PROTECT)
    template = models.ForeignKey(Record, on_delete=models.PROTECT)
    status = models.CharField(max_length=32, default="draft")


class Revision(Entity):
    inspection = models.ForeignKey(Inspection, on_delete=models.PROTECT)
    number = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="report_revisions")
    reviewer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    findings = models.JSONField(default=list)
    status = models.CharField(max_length=32, default="draft")
    checksum = models.CharField(max_length=64)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inspection", "number"], name="one_report_revision_number"
            )
        ]


class Auction(Entity):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    report = models.ForeignKey(Revision, on_delete=models.PROTECT)
    policy = models.ForeignKey(Record, on_delete=models.PROTECT)
    status = models.CharField(max_length=32, default="draft", db_index=True)
    starts_at = models.DateTimeField()
    closes_at = models.DateTimeField(db_index=True)
    currency = models.CharField(max_length=3)
    starting_minor = models.BigIntegerField()
    increment_minor = models.BigIntegerField()
    reserve_minor = models.BigIntegerField(null=True, blank=True)
    current_bid_minor = models.BigIntegerField(null=True, blank=True)
    sequence = models.PositiveIntegerField(default=0)
    safety_hold = models.BooleanField(default=False)
    offer_expires_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(starting_minor__gt=0, increment_minor__gt=0),
                name="positive_auction_prices",
            ),
            models.CheckConstraint(
                condition=Q(closes_at__gt=models.F("starts_at")), name="positive_auction_interval"
            ),
        ]


class Bid(Entity):
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)
    amount_minor = models.BigIntegerField()
    sequence = models.PositiveIntegerField()
    accepted_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["auction", "sequence"], name="one_bid_at_sequence"),
            models.CheckConstraint(condition=Q(amount_minor__gt=0), name="positive_bid_amount"),
        ]


class Result(Entity):
    auction = models.OneToOneField(Auction, on_delete=models.PROTECT)
    winner = models.ForeignKey(Bid, null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=32)
    seller_decision = models.CharField(max_length=16, blank=True)


class TransactionCase(Entity):
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.PROTECT)
    result = models.OneToOneField(Result, null=True, blank=True, on_delete=models.PROTECT)
    consumer_offer = models.OneToOneField(Record, null=True, blank=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sales")
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="purchases")
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=32, default="open")
    title_verified = models.BooleanField(default=False)
    handover_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(result__isnull=False, consumer_offer__isnull=True)
                    | Q(result__isnull=True, consumer_offer__isnull=False)
                ),
                name="exactly_one_transaction_origin",
            )
        ]


class Obligation(Entity):
    transaction = models.ForeignKey(TransactionCase, on_delete=models.PROTECT)
    amount_minor = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=32, default="outstanding")
    prepared_by = models.ForeignKey(User, on_delete=models.PROTECT)
    data = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(amount_minor__gt=0), name="positive_obligation")
        ]


class PaymentEvidence(Entity):
    obligation = models.ForeignKey(Obligation, on_delete=models.PROTECT)
    source_reference = models.CharField(max_length=200, unique=True)
    amount_minor = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    file = models.ForeignKey(Record, on_delete=models.PROTECT)
    prepared_by = models.ForeignKey(User, on_delete=models.PROTECT)
    verified_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="verified_evidence"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(amount_minor__gt=0), name="positive_evidence")
        ]


class CommandReceipt(models.Model):
    principal = models.ForeignKey(User, on_delete=models.PROTECT)
    operation = models.CharField(max_length=100)
    key = models.CharField(max_length=200)
    payload_hash = models.CharField(max_length=64)
    response = models.JSONField(null=True)
    status_code = models.PositiveSmallIntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["principal", "operation", "key"], name="one_intent_receipt"
            )
        ]


class Audit(models.Model):
    id = models.BigAutoField(primary_key=True)
    actor = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    action = models.CharField(max_length=100)
    object_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=64)
    outcome = models.CharField(max_length=32, default="committed")
    metadata = models.JSONField(default=dict)
    occurred_at = models.DateTimeField(auto_now_add=True)


class Outbox(Entity):
    event_type = models.CharField(max_length=100)
    aggregate_id = models.UUIDField()
    aggregate_version = models.PositiveIntegerField()
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, default="pending", db_index=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    available_at = models.DateTimeField()


class Notification(Entity):
    recipient = models.ForeignKey(User, on_delete=models.PROTECT)
    event = models.ForeignKey(Outbox, on_delete=models.PROTECT)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["recipient", "event"], name="one_event_notification")
        ]


class Challenge(Entity):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=40)
    secret_hash = models.CharField(max_length=256)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    consumed = models.BooleanField(default=False)
    session_key = models.CharField(max_length=100, blank=True)


class RateBucket(models.Model):
    key = models.CharField(max_length=200, primary_key=True)
    count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()
