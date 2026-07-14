from dataclasses import dataclass
from typing import List

from app.models.customer import Customer
from app.models.device import Device
from app.models.plan import Plan
from app.models.router import Router
from app.models.router_account import RouterAccount
from app.models.subscription import Subscription


@dataclass(slots=True)
class RouterContext:

    customer: Customer

    subscription: Subscription

    plan: Plan

    router: Router

    router_account: RouterAccount

    plaintext_password: str

    devices: List[Device]