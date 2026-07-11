import { useState } from "react";

import {
    Box,
    Card,
    CardContent,
    Chip,
    Divider,
    IconButton,
    ListItemIcon,
    ListItemText,
    Menu,
    MenuItem,
    Stack,
    Typography,
} from "@mui/material";

import MoreVertIcon from "@mui/icons-material/MoreVert";
import EditIcon from "@mui/icons-material/Edit";
import GroupIcon from "@mui/icons-material/Group";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import DeleteIcon from "@mui/icons-material/Delete";
import SecurityIcon from "@mui/icons-material/Security";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import SupportAgentIcon from "@mui/icons-material/SupportAgent";
import EngineeringIcon from "@mui/icons-material/Engineering";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import RouterIcon from "@mui/icons-material/Router";
import AssessmentIcon from "@mui/icons-material/Assessment";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import Inventory2Icon from "@mui/icons-material/Inventory2";
import HeadsetMicIcon from "@mui/icons-material/HeadsetMic";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import PauseCircleIcon from "@mui/icons-material/PauseCircle";
import Avatar from "@mui/material/Avatar";

import PermissionGate from "../../permissions/PermissionGate";

import RoleDetailsDialog from "./RoleDetailsDialog";

import {

    useCurrentPermissions,

} from "../../../hooks/useCurrentPermissions";

export default function RoleCard({

    role,

    onEdit,

    onAssignUsers,

    onDuplicate,

    onDelete,

    onToggleActivation,

}) {

    const [

        anchorEl,

        setAnchorEl,

    ] = useState(null);

    const [
        detailsOpen,

        setDetailsOpen,

    ] = useState(false)

    const menuOpen = Boolean(

        anchorEl,

    );

    const {

        hasPermission,

    } = useCurrentPermissions();

    const canViewRole =
        hasPermission(
            "permissions.view"
        );

    const appearance =

        getRoleAppearance(

            role.role_name,

        );    

    function getRoleAppearance(

        roleName = "",

    ) {

        const name =

            roleName.toLowerCase();

        if (

            name.includes("super")

        ) {

            return {

                icon: <AdminPanelSettingsIcon />,

                color: "error.main",

            };

        }

        if (

            name.includes("administrator")

        ) {

            return {

                icon: <ManageAccountsIcon />,

                color: "primary.main",

            };

        }

        if (

            name.includes("support")

        ) {

            return {

                icon: <SupportAgentIcon />,

                color: "success.main",

            };

        }

        if (

            name.includes("technician")

        ) {

            return {

                icon: <EngineeringIcon />,

                color: "warning.main",

            };

        }

        if (

            name.includes("finance")

        ) {

            return {

                icon: <AccountBalanceIcon />,

                color: "secondary.main",

            };

        }

        if (

            name.includes("sales")

        ) {

            return {

                icon: <PointOfSaleIcon />,

                color: "info.main",

            };

        }

        if (

            name.includes("network")

        ) {

            return {

                icon: <RouterIcon />,

                color: "primary.dark",

            };

        }

        if (

            name.includes("report")

        ) {

            return {

                icon: <AssessmentIcon />,

                color: "success.dark",

            };

        }

        if (

            name.includes("automation")

        ) {

            return {

                icon: <SmartToyIcon />,

                color: "secondary.dark",

            };

        }

        if (

            name.includes("inventory")

        ) {

            return {

                icon: <Inventory2Icon />,

                color: "warning.dark",

            };

        }

        if (

            name.includes("customer")

        ) {

            return {

                icon: <HeadsetMicIcon />,

                color: "info.dark",

            };

        }

        return {

            icon: <SecurityIcon />,

            color: "grey.700",

        };

    }

    function handleOpenMenu(

        event,

    ) {

        event.stopPropagation();

        setAnchorEl(

            event.currentTarget,

        );

    }

    function handleCloseMenu() {

        setAnchorEl(

            null,

        );

    }

    function handleEdit() {

        handleCloseMenu();

        onEdit?.();

    }

    function handleAssignUsers() {

        handleCloseMenu();

        onAssignUsers?.();

    }

    function handleDuplicate() {

        handleCloseMenu();

        onDuplicate?.();

    }

    function handleDelete() {

        handleCloseMenu();

        onDelete?.();

    }

    function handleActivation() {

        handleCloseMenu();

        onToggleActivation?.();

    }

    function handleOpenDetails() {

        setDetailsOpen(

            true,

        );

    }

    function handleCloseDetails() {

        setDetailsOpen(

            false,

        );

    }

    return (

        <>

            <Card

                elevation={0}

                onClick={
                    canViewRole

                    ? handleOpenDetails
                    : undefined

                }

                sx={{

                    height: "100%",

                    border: (theme) =>

                        `1px solid ${theme.palette.divider}`,

                    borderRadius: 3,

                    cursor: "pointer",

                    transition: "0.2s",

                    "&:hover": {

                        boxShadow: 3,

                        transform: "translateY(-2px)",

                    },

                }}

            >

                <CardContent>

                    <Stack spacing={2}>

                        <Stack

                            direction="row"

                            justifyContent="space-between"

                            alignItems="flex-start"

                        >

                            <Stack spacing={1}>

                                <Stack

                                    direction="row"

                                    spacing={1}

                                    alignItems="center"

                                    flexWrap="wrap"

                                >

                                    <Avatar

                                        sx={{

                                            width: 42,

                                            height: 42,

                                            bgcolor:

                                                appearance.color,

                                        }}

                                    >

                                        {appearance.icon}

                                    </Avatar>

                                    <Typography variant="h6">

                                        {role.role_name}

                                    </Typography>

                                    {role.is_system_role && (

                                        <Chip

                                            size="small"

                                            color="primary"

                                            label="System"

                                        />

                                    )}

                                </Stack>

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                >

                                    {role.description ||

                                        "No description provided."}

                                </Typography>

                            </Stack>

                            <IconButton

                                onClick={(event) => {

                                    event.stopPropagation();

                                    handleOpenMenu(event);

                                }}

                            >

                                <MoreVertIcon />

                            </IconButton>

                        </Stack>

                        <Divider />

                        <Stack spacing={1.5}>

                            <Box

                                display="flex"

                                justifyContent="space-between"

                                alignItems="center"

                            >

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                >

                                    Status

                                </Typography>

                                <Chip

                                    size="small"

                                    color={

                                        role.is_active

                                            ? "success"

                                            : "default"

                                    }

                                    label={

                                        role.is_active

                                            ? "Active"

                                            : "Inactive"

                                    }

                                />

                            </Box>

                            <Box

                                display="flex"

                                justifyContent="space-between"

                                alignItems="center"

                            >

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                >

                                    Administrators

                                </Typography>

                                <Chip

                                    size="small"

                                    label={`${

                                        role.assigned_users ?? 0

                                    } assigned`}

                                />

                            </Box>

                            <Box

                                display="flex"

                                justifyContent="space-between"

                                alignItems="center"

                            >

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                >

                                    Permissions

                                </Typography>

                                <Chip

                                    size="small"

                                    color="primary"

                                    label={`${

                                        role.permission_count ?? 0

                                    } assigned`}

                                />

                            </Box>

                        </Stack>

                    </Stack>

                </CardContent>

            </Card>

            <Menu

                anchorEl={anchorEl}

                open={menuOpen}

                onClose={handleCloseMenu}

            >

                <PermissionGate

                    permission="roles.edit"

                >

                    <MenuItem

                        onClick={handleEdit}

                    >

                        <ListItemIcon>

                            <EditIcon

                                fontSize="small"

                            />

                        </ListItemIcon>

                        <ListItemText>

                            Edit Role

                        </ListItemText>

                    </MenuItem>

                </PermissionGate>

                <PermissionGate

                    permission="admin_users.change_role"

                >

                    <MenuItem

                        onClick={handleAssignUsers}

                    >

                        <ListItemIcon>

                            <GroupIcon

                                fontSize="small"

                            />

                        </ListItemIcon>

                        <ListItemText>

                            Assign Users

                        </ListItemText>

                    </MenuItem>

                </PermissionGate>

                <PermissionGate

                    permission="roles.duplicate"

                >

                    <MenuItem

                        onClick={

                            handleDuplicate

                        }

                    >

                        <ListItemIcon>

                            <ContentCopyIcon

                                fontSize="small"

                            />

                        </ListItemIcon>

                        <ListItemText>

                            Duplicate Role

                        </ListItemText>

                    </MenuItem>

                </PermissionGate>

                <Divider />

                    <MenuItem

                        disabled={

                            role.is_system_role ||

                            (

                                role.is_active

                                    ? !hasPermission(

                                        "roles.deactivate",

                                    )

                                    : !hasPermission(

                                        "roles.activate",

                                    )

                            )

}

                        onClick={handleActivation}

                    >

                    <ListItemIcon>

                        {role.is_active ? (

                            <PauseCircleIcon

                                fontSize="small"

                                color="warning"

                            />

                        ) : (

                            <CheckCircleIcon

                                fontSize="small"

                                color="success"

                            />

                        )}

                    </ListItemIcon>

                    <ListItemText>

                        {role.is_active

                            ? "Deactivate Role"

                            : "Activate Role"}

                    </ListItemText>

                </MenuItem>

                <Divider />

                <PermissionGate

                    permission="roles.delete"

                >

                    <MenuItem

                        disabled={

                            role.is_system_role

                        }

                        onClick={

                            handleDelete

                        }

                        sx={{

                            color: "error.main",

                        }}

                    >

                        <ListItemIcon>

                            <DeleteIcon

                                fontSize="small"

                                color="error"

                            />

                        </ListItemIcon>

                        <ListItemText>

                            Delete Role

                        </ListItemText>

                    </MenuItem>

                </PermissionGate>

            </Menu>

        {canViewRole && (

            <RoleDetailsDialog

                open={

                    detailsOpen

                }

                role={role}

                onClose={

                    handleCloseDetails

                }

            />
        )}

        </>

    );

}