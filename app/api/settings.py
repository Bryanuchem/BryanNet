from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.settings import (
    AuthenticationSettingsUpdate,
    BillingSettingsUpdate,
    BrandingSettingsUpdate,
    GeneralSettingsUpdate,
    IntegrationSettingsUpdate,
    NetworkSettingsUpdate,
    NotificationSettingsUpdate,
    SystemSettingsUpdate,
)

from app.services.setting_service import (
    SettingService,
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
)
def get_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_VIEW,
        ),
    ),   
        
):

    return (
        SettingService.get_all_settings(
            db,
        )
    )


# ==========================================================
# General
# ==========================================================

@router.get(
    "/general",
)
def get_general_settings(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_GENERAL,
        ),
    ),

):

    return (
        SettingService.get_category(
            db,
            "general",
        )
    )


# ==========================================================
# Authentication
# ==========================================================

@router.get(
    "/authentication",
)
def get_authentication_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_AUTHENTICATION,
        ),
    ),
        
):

    return (
        SettingService.get_category(
            db,
            "authentication",
        )
    )


# ==========================================================
# Notifications
# ==========================================================

@router.get(
    "/notifications",
)
def get_notification_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.SETTINGS_NOTIFICATIONS,
        ),
    ),

):

    return (
        SettingService.get_category(
            db,
            "notifications",
        )
    )


# ==========================================================
# Network
# ==========================================================

@router.get(
    "/network",
)
def get_network_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_NETWORK,
        ),
    ),    

):

    return (
        SettingService.get_category(
            db,
            "network",
        )
    )


# ==========================================================
# Billing
# ==========================================================

@router.get(
    "/billing",
)
def get_billing_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_BILLING,
        ),
    ),
    
):

    return (
        SettingService.get_category(
            db,
            "billing",
        )
    )


# ==========================================================
# Integrations
# ==========================================================

@router.get(
    "/integrations",
)
def get_integration_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
 
    _=Depends(
        require_permission(
            Permissions.SETTINGS_INTEGRATIONS,
        ),
    ),   
        
):

    return (
        SettingService.get_category(
            db,
            "integrations",
        )
    )


# ==========================================================
# Branding
# ==========================================================

@router.get(
    "/branding",
)
def get_branding_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_BRANDING,
        ),
    ),
    
):

    return (
        SettingService.get_category(
            db,
            "branding",
        )
    )


# ==========================================================
# System
# ==========================================================

@router.get(
    "/system",
)
def get_system_settings(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.SETTINGS_SYSTEM,
        ),
    ),
        
):

    return (
        SettingService.get_category(
            db,
            "system",
        )
    )


# ==========================================================
# Business Commands
# ==========================================================

# ==========================================================
# General
# ==========================================================

@router.put(
    "/general",
)
def update_general_settings(
    request: GeneralSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
_=Depends(
    require_permission(
        Permissions.SETTINGS_GENERAL,
    ),
),

):

    return (
        SettingService.update_category(
            db=db,
            category="general",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Authentication
# ==========================================================

@router.put(
    "/authentication",
)
def update_authentication_settings(
    request: AuthenticationSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
_=Depends(
    require_permission(
        Permissions.SETTINGS_AUTHENTICATION,
    ),
),    

):

    return (
        SettingService.update_category(
            db=db,
            category="authentication",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Notifications
# ==========================================================

@router.put(
    "/notifications",
)
def update_notification_settings(
    request: NotificationSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.SETTINGS_NOTIFICATIONS,
        ),
    ),

):

    return (
        SettingService.update_category(
            db=db,
            category="notifications",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Network
# ==========================================================

@router.put(
    "/network",
)
def update_network_settings(
    request: NetworkSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.SETTINGS_NETWORK,
        ),
    ),
    
):

    return (
        SettingService.update_category(
            db=db,
            category="network",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Billing
# ==========================================================

@router.put(
    "/billing",
)
def update_billing_settings(
    request: BillingSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.SETTINGS_BILLING,
        ),
    ),
    
):

    return (
        SettingService.update_category(
            db=db,
            category="billing",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Integrations
# ==========================================================

@router.put(
    "/integrations",
)
def update_integration_settings(
    request: IntegrationSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.SETTINGS_INTEGRATIONS,
        ),
    ),
    
):

    return (
        SettingService.update_category(
            db=db,
            category="integrations",
            values=request.model_dump(),
        )
    )


# ==========================================================
# Branding
# ==========================================================

@router.put(
    "/branding",
)
def update_branding_settings(
    request: BrandingSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.SETTINGS_BRANDING,
        ),
    ),
    
):

    return (
        SettingService.update_category(
            db=db,
            category="branding",
            values=request.model_dump(),
        )
    )


# ==========================================================
# System
# ==========================================================

@router.put(
    "/system",
)
def update_system_settings(
    request: SystemSettingsUpdate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.SETTINGS_SYSTEM,
        ),
    ),
    
):

    return (
        SettingService.update_category(
            db=db,
            category="system",
            values=request.model_dump(),
        )
    )