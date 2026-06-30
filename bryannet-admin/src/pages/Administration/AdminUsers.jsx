import { useState } from "react";

import {
    Box,
    Button,
    MenuItem,
    Paper,
    Stack,
    TextField,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import RefreshIcon from "@mui/icons-material/Refresh";

import PageHeader from "../../components/common/PageHeader";

import AdminUsersTable from "../../components/admin/AdminUsersTable";
import AdminUserDetailsDrawer from "../../components/admin/AdminUserDetailsDrawer";
import AdminUserActionDialog from "../../components/admin/AdminUserActionDialog";

export function AdminUsers() {
    const [drawerOpen, setDrawerOpen] =
        useState(false);

    const [drawerMode, setDrawerMode] =
        useState("details");

    const [selectedAdministrator, setSelectedAdministrator] =
        useState(null);

    const [actionDialogOpen, setActionDialogOpen] =
        useState(false);

    const [actionType, setActionType] =
        useState(null);

    const handleCloseDrawer = () => {
        setDrawerOpen(false);
        setDrawerMode("details");
        setSelectedAdministrator(null);
    };

    const handleViewAdministrator = (
        administrator
    ) => {
        setSelectedAdministrator(administrator);
        setDrawerMode("details");
        setDrawerOpen(true);
    };

    const handleCreateAdministrator = () => {
        setSelectedAdministrator({
            name: "",
            username: "",
            email: "",
            phone: "",
            role: "",
            status: "Active",
            created: "",
            lastLogin: "Never",
        });

        setDrawerMode("create");
        setDrawerOpen(true);
    };

    const handleEditAdministrator = (
        administrator
    ) => {
        setSelectedAdministrator(administrator);
        setDrawerMode("edit");
        setDrawerOpen(true);
    };

    const openActionDialog = (
        administrator,
        type
    ) => {
        setSelectedAdministrator(administrator);
        setActionType(type);
        setActionDialogOpen(true);
    };

    const handleCloseActionDialog = () => {
        setActionDialogOpen(false);
        setActionType(null);
    };

    const handleActionConfirm = (
        administrator,
        action
    ) => {
        console.log(action, administrator);

        handleCloseActionDialog();
    };

    return (
        <>
            <PageHeader
                title="Admin Users"
                subtitle="Manage administrators who can access the BryanNet dashboard."
            />

            <Button
                variant="contained"
                startIcon={<AddIcon />}
                sx={{ mb: 3 }}
                onClick={
                    handleCreateAdministrator
                }
            >
                Add Administrator
            </Button>

            <Box
                display="flex"
                flexDirection="column"
                gap={3}
            >
                <Paper
                    elevation={0}
                    sx={{
                        p: 3,
                        border: 1,
                        borderColor: "divider",
                        borderRadius: 2,
                    }}
                >
                    <Stack spacing={3}>
                        <TextField
                            fullWidth
                            placeholder="Search administrators..."
                            size="small"
                        />

                        <Stack
                            direction={{
                                xs: "column",
                                md: "row",
                            }}
                            spacing={2}
                            justifyContent="space-between"
                            alignItems={{
                                xs: "stretch",
                                md: "center",
                            }}
                        >
                            <Stack
                                direction={{
                                    xs: "column",
                                    sm: "row",
                                }}
                                spacing={2}
                            >
                                <TextField
                                    select
                                    label="Role"
                                    defaultValue="all"
                                    size="small"
                                    sx={{
                                        minWidth: 180,
                                    }}
                                >
                                    <MenuItem value="all">
                                        All
                                    </MenuItem>

                                    <MenuItem value="Super Administrator">
                                        Super Administrator
                                    </MenuItem>

                                    <MenuItem value="Administrator">
                                        Administrator
                                    </MenuItem>

                                    <MenuItem value="Support">
                                        Support
                                    </MenuItem>
                                </TextField>

                                <TextField
                                    select
                                    label="Status"
                                    defaultValue="all"
                                    size="small"
                                    sx={{
                                        minWidth: 180,
                                    }}
                                >
                                    <MenuItem value="all">
                                        All
                                    </MenuItem>

                                    <MenuItem value="Active">
                                        Active
                                    </MenuItem>

                                    <MenuItem value="Inactive">
                                        Inactive
                                    </MenuItem>
                                </TextField>
                            </Stack>

                            <Button
                                variant="outlined"
                                startIcon={<RefreshIcon />}
                            >
                                Refresh
                            </Button>
                        </Stack>
                    </Stack>
                </Paper>

                <AdminUsersTable
                    onViewAdministrator={
                        handleViewAdministrator
                    }
                    onEditAdministrator={
                        handleEditAdministrator
                    }
                    onDeleteAdministrator={(
                        administrator
                    ) =>
                        openActionDialog(
                            administrator,
                            "delete"
                        )
                    }
                    onToggleAdministrator={(
                        administrator
                    ) =>
                        openActionDialog(
                            administrator,
                            administrator.status ===
                                "Active"
                                ? "deactivate"
                                : "activate"
                        )
                    }
                    onResetPassword={(
                        administrator
                    ) =>
                        openActionDialog(
                            administrator,
                            "resetPassword"
                        )
                    }
                />
            </Box>

            <AdminUserDetailsDrawer
                open={drawerOpen}
                administrator={
                    selectedAdministrator
                }
                drawerMode={drawerMode}
                onDrawerModeChange={
                    setDrawerMode
                }
                onClose={
                    handleCloseDrawer
                }
            />

            <AdminUserActionDialog
                open={actionDialogOpen}
                type={actionType}
                administrator={
                    selectedAdministrator
                }
                onClose={
                    handleCloseActionDialog
                }
                onConfirm={
                    handleActionConfirm
                }
            />
        </>
    );
}

export default AdminUsers;                