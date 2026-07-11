import {

    useMemo,

    useState,

} from "react";

import {

    Box,

    Button,

    Grid,

    Stack,

    Typography,

} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import SearchBar from "../../components/common/SearchBar";
import AppSnackbar from "../../components/common/AppSnackbar";

import RoleCard from "../../components/admin/roles/RoleCard";
import RoleDialog from "../../components/admin/roles/RoleDialog";
import AssignUsersDialog from "../../components/admin/roles/AssignUsersDialog";
import DeleteRoleDialog from "../../components/admin/roles/DeleteRoleDialog";
import RoleActivationDialog from "../../components/admin/roles/RoleActivationDialog"
import PermissionGate from "../../components/permissions/PermissionGate";

import {

    useRoles,

} from "../../hooks/useRoles";

import {

    useAdminUsers,

} from "../../hooks/useAdminUsers";

import {

    useUpdateRoleActivation,

} from "../../hooks/useUpdateRoleActivation";

import {

    useDuplicateRole,

} from "../../hooks/useDuplicateRole";

import {

    useDeleteRole,

} from "../../hooks/useDeleteRole";

export default function RolesPermissions() {

    const [

        search,

        setSearch,

    ] = useState("");

    const [

        selectedRole,

        setSelectedRole,

    ] = useState(null);

    const [

        dialogType,

        setDialogType,

    ] = useState(null);

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        message: "",

        severity: "success",

    });

    const {

        data: roles = [],

        isLoading,

        isError,

        refetch,

    } = useRoles();

    const {

        data: administrators = {

            items: [],

        },

    } = useAdminUsers();

    const updateRoleActivation =

        useUpdateRoleActivation({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Role updated successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.message ||

                        error?.response?.data?.detail ||

                        "Failed to update role.",

                });

            },

        });

    const duplicateRole =

        useDuplicateRole({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Role duplicated successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.message ||

                        error?.response?.data?.detail ||

                        "Failed to duplicate role.",

                });

            },

        });

    const deleteRole =

        useDeleteRole({

            onSuccess: (

                response,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        response?.message ||

                        "Role deleted successfully.",

                });

                handleCloseDialogs();

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.message ||

                        error?.response?.data?.detail ||

                        "Failed to delete role.",

                });

            },

        });

    const filteredRoles = useMemo(

        () => {

            const query =

                search

                    .trim()

                    .toLowerCase();

            if (

                !query

            ) {

                return roles;

            }

            return roles.filter(

                (

                    role,

                ) =>

                    role.role_name

                        ?.toLowerCase()

                        .includes(

                            query,

                        ) ||

                    role.description

                        ?.toLowerCase()

                        .includes(

                            query,

                        ),

            );

        },

        [

            roles,

            search,

        ],

    );

    function openDialog(

        type,

        role = null,

    ) {

        setSelectedRole(

            role,

        );

        setDialogType(

            type,

        );

    }

    function handleCreateRole() {

        openDialog(

            "role",

        );

    }

    function handleEditRole(

        role,

    ) {

        openDialog(

            "role",

            role,

        );

    }

    function handleAssignUsers(

        role,

    ) {

        openDialog(

            "assign-users",

            role,

        );

    }

    function handleDuplicateRole(

        role,

    ) {

        duplicateRole.mutate(

            role.role_id,

        );

    }

    function handleDeleteRole(

        role,

    ) {

        openDialog(

            "delete",

            role,

        );

    }

    function handleCloseDialogs() {

        setDialogType(

            null,

        );

        setSelectedRole(

            null,

        );

        refetch();

    }

    function handleActivation(

        role,

    ) {

        setSelectedRole(

            role,

        );

        setDialogType(

            "activation",

        );

    }

    function handleConfirmActivation() {

        if (

            !selectedRole

        ) {

            return;

        }

        updateRoleActivation.mutate(

            {

                roleId:

                    selectedRole.role_id,

                isActive:

                    !selectedRole.is_active,

            },

            {

                onSuccess: () => {

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:

                            selectedRole.is_active

                                ? "Role deactivated successfully."

                                : "Role activated successfully.",

                    });

                    handleCloseDialogs();

                },

            },

        );

    }

    function handleDelete() {

        if (

            !selectedRole

        ) {

            return;

        }

        deleteRole.mutate(

            selectedRole.role_id,

        );

    }

    return (

        <Box>

            <PageHeader

                title="Roles & Permissions"

                subtitle="Create administrator roles and manage permissions across the BryanNet ISP Platform."

            />

            <Stack spacing={3}>

                <PermissionGate

                    permission="roles.create"

                >

                    <Button

                        variant="contained"

                        startIcon={<AddIcon />}

                        onClick={handleCreateRole}

                        sx={{

                            alignSelf: "flex-start",

                        }}

                    >

                        Create Role

                    </Button>
                </PermissionGate>

                <SearchBar

                    value={search}

                    onChange={(

                        event,

                    ) =>

                        setSearch(

                            event.target.value,

                        )

                    }

                    placeholder="Search roles..."

                />

                <Grid

                    container

                    spacing={3}

                >

                    {filteredRoles.map(

                        (

                            role,

                        ) => (

                            <Grid

                                key={

                                    role.role_id

                                }

                                size={{

                                    xs: 12,

                                    md: 6,

                                    lg: 4,

                                }}

                            >

                                <RoleCard

                                    role={

                                        role

                                    }

                                    onEdit={() =>

                                        handleEditRole(

                                            role,

                                        )

                                    }

                                    onAssignUsers={() =>

                                        handleAssignUsers(

                                            role,

                                        )

                                    }

                                    onDuplicate={() =>

                                        handleDuplicateRole(

                                            role,

                                        )

                                    }

                                    onDelete={() =>

                                        handleDeleteRole(

                                            role,

                                        )

                                    }

                                    onToggleActivation={() =>

                                        handleActivation(

                                            role,

                                        )

                                    }

                                />

                            </Grid>

                        ),

                    )}

                </Grid>

                {isLoading && (

                    <Box

                        sx={{

                            py: 8,

                            textAlign: "center",

                        }}

                    >

                        <Typography

                            color="text.secondary"

                        >

                            Loading roles...

                        </Typography>

                    </Box>

                )}

                {!isLoading &&

                    !isError &&

                    filteredRoles.length === 0 && (

                        <Box

                            sx={{

                                py: 8,

                                textAlign: "center",

                            }}

                        >

                            <Typography

                                variant="h6"

                                gutterBottom

                            >

                                No roles found

                            </Typography>

                            <Typography

                                color="text.secondary"

                            >

                                Try adjusting your search or create a new role.

                            </Typography>

                        </Box>

                    )}

                {isError && (

                    <Box

                        sx={{

                            py: 8,

                            textAlign: "center",

                        }}

                    >

                        <Typography

                            color="error"

                            variant="h6"

                            gutterBottom

                        >

                            Failed to load roles

                        </Typography>

                        <Typography

                            color="text.secondary"

                        >

                            Please refresh the page and try again.

                        </Typography>

                    </Box>

                )}

            </Stack> 

            <RoleDialog

                open={

                    dialogType ===

                    "role"

                }

                role={

                    selectedRole

                }

                onClose={

                    handleCloseDialogs

                }

            />

            <RoleActivationDialog

                open={

                    dialogType ===

                    "activation"

                }

                role={

                    selectedRole

                }

                loading={

                    updateRoleActivation.isPending

                }

                onClose={

                    handleCloseDialogs

                }

                onConfirm={

                    handleConfirmActivation

                }

            />

            <AssignUsersDialog

                open={

                    dialogType ===

                    "assign-users"

                }

                role={

                    selectedRole

                }

                administrators={

                    administrators

                }

                onClose={

                    handleCloseDialogs

                }

            />

            <DeleteRoleDialog

                open={

                    dialogType ===

                    "delete"

                }

                role={

                    selectedRole

                }

                loading={

                    deleteRole.isPending

                }

                onClose={

                    handleCloseDialogs

                }

                onDelete={

                    handleDelete

                }

            />

            <AppSnackbar

                open={

                    snackbar.open

                }

                message={

                    snackbar.message

                }

                severity={

                    snackbar.severity

                }

                onClose={() =>

                    setSnackbar(

                        (

                            previous,

                        ) => ({

                            ...previous,

                            open: false,

                        }),

                    )

                }

            />

        </Box>

    );

}                   