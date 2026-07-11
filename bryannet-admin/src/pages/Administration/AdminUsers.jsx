import {
    useMemo,
    useState,
} from "react";

import {
    Button,
    Stack,
} from "@mui/material";

import { useRoles } from "../../hooks/useRoles";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";

import AdminUsersToolbar from "../../components/admin/admin-users/AdminUsersToolbar";
import AdminUsersTable from "../../components/admin/admin-users/AdminUsersTable";
import AdminUserForm from "../../components/admin/admin-users/AdminUserForm";
import AdminUserDetailsDrawer from "../../components/admin/admin-users/AdminUserDetailsDrawer";
import AdminUserActionDialog from "../../components/admin/admin-users/AdminUserActionDialog";
import ChangeRoleDialog from "../../components/admin/admin-users/ChangeRoleDialog";
import ResetPasswordDialog from "../../components/admin/admin-users/ResetPasswordDialog";

import {
    useAdminUsers,
} from "../../hooks/useAdminUsers";

import {
    useCreateAdminUser,
} from "../../hooks/useCreateAdminUser";

import {
    useUpdateAdminUser,
} from "../../hooks/useUpdateAdminUser";

import {
    useUpdateAdminActivation,
} from "../../hooks/useUpdateAdminActivation";

import {
    useChangeAdminRole,
} from "../../hooks/useChangeAdminRole";

import {
    useChangeAdminPassword,
} from "../../hooks/useChangeAdminPassword";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";

function AdminUsers() {

    // ==========================================================
    // Filters
    // ==========================================================

    const [

        search,

        setSearch,

    ] = useState("");

    const [

        role,

        setRole,

    ] = useState("");

    const [

        status,

        setStatus,

    ] = useState("");

    const {

        hasPermission,

    } = useCurrentPermissions();

    const filters = useMemo(

        () => ({

            search:
                search || undefined,

            role_id:
                role || undefined,

            is_active:

                status === ""

                    ? undefined

                    : status,

        }),

        [

            search,

            role,

            status,

        ],

    );

    // ==========================================================
    // Queries
    // ==========================================================

    const {

        data: administrators = [],

        isLoading,

        refetch,

    } = useAdminUsers(
        filters,
    );

    const {

        data: roles = [],

    } = useRoles();    

    // ==========================================================
    // Mutations
    // ==========================================================

    const createAdminUser =

        useCreateAdminUser();

    const updateAdminUser =

        useUpdateAdminUser();

    const updateAdminActivation =

        useUpdateAdminActivation();

    const changeAdminRole =

        useChangeAdminRole();

    const changeAdminPassword =

        useChangeAdminPassword();

    // ==========================================================
    // Drawer
    // ==========================================================

    const [

        drawerOpen,

        setDrawerOpen,

    ] = useState(false);

    const [

        selectedAdministrator,

        setSelectedAdministrator,

    ] = useState(null);

    // ==========================================================
    // Form Dialog
    // ==========================================================

    const [

        formOpen,

        setFormOpen,

    ] = useState(false);

    const [

        editingAdministrator,

        setEditingAdministrator,

    ] = useState(null);

    // ==========================================================
    // Activation Dialog
    // ==========================================================

    const [

        activationDialogOpen,

        setActivationDialogOpen,

    ] = useState(false);

    const [

        activationAdministrator,

        setActivationAdministrator,

    ] = useState(null);

    // ==========================================================
    // Role Dialog
    // ==========================================================

    const [

        roleDialogOpen,

        setRoleDialogOpen,

    ] = useState(false);

    const [

        roleAdministrator,

        setRoleAdministrator,

    ] = useState(null);

    const [

        selectedRole,

        setSelectedRole,

    ] = useState("");

    // ==========================================================
    // Password Dialog
    // ==========================================================

    const [

        passwordDialogOpen,

        setPasswordDialogOpen,

    ] = useState(false);

    const [

        passwordAdministrator,

        setPasswordAdministrator,

    ] = useState(null);

    // ==========================================================
    // Snackbar
    // ==========================================================

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        severity: "success",

        message: "",

    });

    // ==========================================================
    // Event Handlers
    // ==========================================================

    const handleView = (

        administrator,

    ) => {

        if (

            !hasPermission(

                "admin_users.view",

            )

        ) {

            return;

        }

        setSelectedAdministrator(

            administrator,

        );

        setDrawerOpen(

            true,

        );

    };

    const handleCreate = () => {

        if (

            !hasPermission(

                "admin_users.create",

            )

        ) {

            return;

        }

        setEditingAdministrator(

            null,

        );

        setFormOpen(

            true,

        );

    };

    const handleEdit = (

        administrator,

    ) => {

        if (

            !hasPermission(

                "admin_users.edit",

            )

        ) {

            return;

        }

        setEditingAdministrator(

            administrator,

        );

        setFormOpen(

            true,

        );

    };

    const handleToggleStatus = (

        administrator,

    ) => {

        const canToggle =

            administrator.is_active

                ? hasPermission(

                    "admin_users.deactivate",

                )

                : hasPermission(

                    "admin_users.activate",

                );

        if (

            !canToggle

        ) {

            return;

        }

        setActivationAdministrator(

            administrator,

        );

        setActivationDialogOpen(

            true,

        );

    };

    const handleOpenRoleDialog = (

        administrator,

    ) => {

        if (

            !hasPermission(

                "admin_users.change_role",

            )

        ) {

            return;

        }

        setRoleAdministrator(

            administrator,

        );

        setSelectedRole(

            administrator.role_id,

        );

        setRoleDialogOpen(

            true,

        );

    };

    const handleOpenPasswordDialog = (

        administrator,

    ) => {

        if (

            !hasPermission(

                "admin_users.reset_password",

            )

        ) {

            return;

        }

        setPasswordAdministrator(

            administrator,

        );

        setPasswordDialogOpen(

            true,

        );

    };

    const handleCloseDrawer = () => {

        setDrawerOpen(false);

        setSelectedAdministrator(
            null,
        );

    };

    const handleCloseForm = () => {

        setFormOpen(false);

        setEditingAdministrator(
            null,
        );

    };

    const handleCloseActivationDialog =
        () => {

            setActivationDialogOpen(
                false,
            );

            setActivationAdministrator(
                null,
            );

        };

    const handleCloseRoleDialog =
        () => {

            setRoleDialogOpen(
                false,
            );

            setRoleAdministrator(
                null,
            );

            setSelectedRole("");

        };

    const handleClosePasswordDialog =
        () => {

            setPasswordDialogOpen(
                false,
            );

            setPasswordAdministrator(
                null,
            );

        };

    // ==========================================================
    // Mutation Handlers
    // ==========================================================

    const handleSubmitAdministrator = async (

        administrator,

    ) => {

        if (

            editingAdministrator

                ? !hasPermission(

                    "admin_users.edit",

                )

                : !hasPermission(

                    "admin_users.create",

                )

        ) {

            return;

        }

        try {

            if (

                editingAdministrator

            ) {

                await updateAdminUser.mutateAsync({

                    adminUserId:

                        editingAdministrator.admin_user_id,

                    adminUser:

                        administrator,

                });

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Administrator updated successfully.",

                });

            } else {

                await createAdminUser.mutateAsync(

                    administrator,

                );

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Administrator created successfully.",

                });

            }

            handleCloseForm();

        } catch (error) {

            setSnackbar({

                open: true,

                severity: "error",

                message:

                    error.response?.data?.detail ??

                    "Unable to save administrator.",

            });

        }

    };

    const handleConfirmActivation = async () => {

        const canToggle =

            activationAdministrator?.is_active

                ? hasPermission(

                    "admin_users.deactivate",

                )

                : hasPermission(

                    "admin_users.activate",

                );

        if (

            !canToggle

        ) {

            return;

        }

        try {

            await updateAdminActivation.mutateAsync({

                adminUserId:

                    activationAdministrator.admin_user_id,

                isActive:

                    !activationAdministrator.is_active,

            });

            setSnackbar({

                open: true,

                severity: "success",

                message:

                    activationAdministrator.is_active

                        ? "Administrator deactivated successfully."

                        : "Administrator activated successfully.",

            });

            handleCloseActivationDialog();

        } catch (error) {

            setSnackbar({

                open: true,

                severity: "error",

                message:

                    error.response?.data?.detail ??

                    "Unable to update administrator.",

            });

        }

    };

    const handleSubmitRole = async () => {

        if (

            !hasPermission(

                "admin_users.change_role",

            )

        ) {

            return;

        }

        try {

            await changeAdminRole.mutateAsync({

                adminUserId:

                    roleAdministrator.admin_user_id,

                roleId:

                    selectedRole,

            });

            setSnackbar({

                open: true,

                severity: "success",

                message:

                    "Role updated successfully.",

            });

            handleCloseRoleDialog();

        } catch (error) {

            setSnackbar({

                open: true,

                severity: "error",

                message:

                    error.response?.data?.detail ??

                    "Unable to update role.",

            });

        }

    };

    const handleSubmitPassword = async (

        password,

    ) => {

        if (

            !hasPermission(

                "admin_users.reset_password",

            )

        ) {

            return;

        }

        try {

            await changeAdminPassword.mutateAsync({

                adminUserId:

                    passwordAdministrator.admin_user_id,

                password,

            });

            setSnackbar({

                open: true,

                severity: "success",

                message:

                    "Password reset successfully.",

            });

            handleClosePasswordDialog();

        } catch (error) {

            setSnackbar({

                open: true,

                severity: "error",

                message:

                    error.response?.data?.detail ??

                    "Unable to reset password.",

            });

        }

    };

    // ==========================================================
    // Temporary Role Options
    // ==========================================================

    const roleOptions = roles.map(

        (role) => ({

            value: role.role_id,

            label: role.role_name,

        }),

    );

    const handleCloseSnackbar = () => {

        setSnackbar(

            (previous) => ({

                ...previous,

                open: false,

            }),

        );

    };

    return (

        <>

            <PageHeader

                title="Admin Users"

                subtitle="Manage administrators who can access the BryanNet dashboard."

            />

            <Stack
                spacing={3}
            >

            {hasPermission(

                "admin_users.create",

            ) && (

                <Stack

                    direction="row"

                    justifyContent="space-between"

                    alignItems="center"

                >

                    <Button

                        variant="contained"

                        startIcon={<AddIcon />}

                        onClick={

                            handleCreate

                        }

                    >

                        Add Administrator

                    </Button>

                </Stack>

            )}

                <AdminUsersToolbar

                    search={search}

                    onSearchChange={(event) =>

                        setSearch(
                            event.target.value,
                        )

                    }

                    role={role}

                    onRoleChange={(event) =>

                        setRole(
                            event.target.value,
                        )

                    }

                    status={status}

                    onStatusChange={(event) =>

                        setStatus(
                            event.target.value,
                        )

                    }

                    roleOptions={roleOptions}

                    administrators={
                        administrators
                    }

                    onRefresh={refetch}

                    onClear={() => {

                        setSearch("");

                        setRole("");

                        setStatus("");

                    }}

                />

                <AdminUsersTable

                    administrators={
                        administrators
                    }

                    loading={
                        isLoading
                    }

                    onRowClick={
                        handleView
                    }

                    onView={
                        handleView
                    }

                    onEdit={
                        handleEdit
                    }

                    onChangeRole={
                        handleOpenRoleDialog
                    }

                    onResetPassword={
                        handleOpenPasswordDialog
                    }

                    onToggleStatus={
                        handleToggleStatus
                    }

                />

            </Stack>

            {hasPermission(

                "admin_users.view",

            ) && (

            <AdminUserDetailsDrawer

                open={
                    drawerOpen
                }

                administrator={
                    selectedAdministrator
                }

                onClose={
                    handleCloseDrawer
                }

            />
        )}

        {hasPermission(

            "admin_users.create",

        ) ||

        hasPermission(

            "admin_users.edit",

        ) ? (

            <AdminUserForm

                open={
                    formOpen
                }

                loading={

                    createAdminUser.isPending ||

                    updateAdminUser.isPending

                }

                administrator={
                    editingAdministrator
                }

                roles={roles}

                onClose={
                    handleCloseForm
                }

                onSubmit={
                    handleSubmitAdministrator
                }

            />
        ) : null}

        {(

            hasPermission(

                "admin_users.activate",

            ) ||

            hasPermission(

                "admin_users.deactivate",

            )

        ) && (

            <AdminUserActionDialog

                open={
                    activationDialogOpen
                }

                loading={
                    updateAdminActivation.isPending
                }

                administrator={
                    activationAdministrator
                }

                activate={
                    !activationAdministrator?.is_active
                }

                onClose={
                    handleCloseActivationDialog
                }

                onConfirm={
                    handleConfirmActivation
                }

            />
        )}

            {hasPermission(

                "admin_users.change_role",

            ) && (

            <ChangeRoleDialog

                open={
                    roleDialogOpen
                }

                loading={
                    changeAdminRole.isPending
                }

                administrator={
                    roleAdministrator
                }

                roles={roles}

                selectedRole={
                    selectedRole
                }

                onRoleChange={(event) =>

                    setSelectedRole(
                        event.target.value,
                    )

                }

                onClose={
                    handleCloseRoleDialog
                }

                onSubmit={
                    handleSubmitRole
                }

            />
        )}

        {hasPermission(

            "admin_users.reset_password",

        ) && (

            <ResetPasswordDialog

                open={
                    passwordDialogOpen
                }

                loading={
                    changeAdminPassword.isPending
                }

                administrator={
                    passwordAdministrator
                }

                onClose={
                    handleClosePasswordDialog
                }

                onSubmit={
                    handleSubmitPassword
                }

            />
        )}

            <AppSnackbar

                open={

                    snackbar.open

                }

                severity={

                    snackbar.severity

                }

                message={

                    snackbar.message

                }

                onClose={

                    handleCloseSnackbar

                }

            />

        </>

    );

}

export default AdminUsers;        