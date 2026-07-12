from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.customer import (
    CustomerCreate,
    CustomerListItem,
    CustomerResponse,
    CustomerUpdate,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
)

from app.schemas.types import (
    PhoneNumber,
)

from app.services.customer_service import (
    CustomerService,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/register",
    response_model=CustomerResponse,
)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_CREATE,
        ),
    ),
):

    return (
        CustomerService.register_customer(
            db=db,
            phone_number=customer.phone_number,
            full_name=customer.full_name,
        )
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_EDIT,
        ),
    ),
):

    return (
        CustomerService.update_customer(
            db=db,
            customer_id=customer_id,
            customer_data=customer,
        )
    )


@router.patch(
    "/{customer_id}/activate",
    response_model=CustomerResponse,
)
def activate_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_EDIT,
        ),
    ),
):

    return (
        CustomerService.activate_customer(
            db=db,
            customer_id=customer_id,
        )
    )


@router.patch(
    "/{customer_id}/deactivate",
    response_model=CustomerResponse,
)
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_EDIT,
        ),
    ),
):

    return (
        CustomerService.deactivate_customer(
            db=db,
            customer_id=customer_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        CustomerListItem,
    ],
)
def get_all_customers(

    search: str | None = None,

    sort_by: str = "customer_id",

    sort_order: str = "asc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_VIEW,
        ),
    ),

):

    return (

        CustomerService.get_all_customers(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

            sort_by=sort_by,

            sort_order=sort_order,

        )

    )


@router.get(
    "/id/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_VIEW,
        ),
    ),
):

    return (
        CustomerService.get_customer(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/phone/{phone_number}",
    response_model=CustomerResponse,
)
def get_customer_by_phone(
    phone_number: PhoneNumber,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.CUSTOMERS_VIEW,
        ),
    ),
):

    return (
        CustomerService.get_customer_by_phone(
            db=db,
            phone_number=phone_number,
        )
    )

