import {

    useEffect,

    useMemo,

    useState,

} from "react";

import {

    Box,

    Chip,

    Avatar,

    Divider,

    Stack,

    Typography,

    TextField,

    Dialog,

    DialogTitle,

    DialogContent,

    DialogActions,

    Button,

} from "@mui/material";

import ShieldIcon from "@mui/icons-material/Shield"

import PermissionMatrix from "./PermissionMatrix";

import {

    usePermissions,

} from "../../../hooks/usePermissions";

import {

    useRolePermissions,

} from "../../../hooks/useRolePermissions";

import {

    useUpdateRolePermissions,

} from "../../../hooks/useUpdateRolePermissions";

import {

    useCreateRole,

} from "../../../hooks/useCreateRole";

import {

    useUpdateRole,

} from "../../../hooks/useUpdateRole";

export default function RoleDialog({

    open,

    role,

    onClose,

}) {

    const [

        roleName,

        setRoleName,

    ] = useState("");

    const [

        description,

        setDescription,

    ] = useState("");

    const [

        selectedPermissions,

        setSelectedPermissions,

    ] = useState([]);

    const {

        data: availablePermissions = [],

        isLoading: permissionsLoading,

    } = usePermissions();

    const {

        data: assignedPermissions = [],

        isLoading: rolePermissionsLoading,

    } = useRolePermissions(

        role?.role_id,

    );

    const createRole =

        useCreateRole();

    const updateRole =

        useUpdateRole();

    const updatePermissions =

        useUpdateRolePermissions({

            onSuccess: () =>

                onClose(),

        });

    const permissions = useMemo(

        () => {

            const selected =

                new Set(

                    selectedPermissions,

                );

            const groups = {};

            availablePermissions.forEach(

                (

                    permission,

                ) => {

                    if (

                        !groups[

                            permission.module

                        ]

                    ) {

                        groups[

                            permission.module

                        ] = {

                            id:

                                permission.module,

                            name:

                                permission.module,

                            description:

                                `${permission.module} permissions.`,

                            permissions: [],

                        };

                    }

                    groups[

                        permission.module

                    ].permissions.push({

                        id:

                            permission.permission_id,

                        name:

                            permission.action,

                        description:

                            permission.description,

                        enabled:

                            selected.has(

                                permission.permission_id,

                            ),

                    });

                },

            );

            return Object.values(

                groups,

            );

        },

        [

            availablePermissions,

            selectedPermissions,

        ],

    );

    useEffect(

        () => {

            if (

                !open

            ) {

                return;

            }

            setRoleName(

                role?.role_name ??

                    "",

            );

            setDescription(

                role?.description ??

                    "",

            );

            setSelectedPermissions(

                assignedPermissions.map(

                    (

                        permission,

                    ) =>

                        permission.permission_id,

                ),

            );

        },

        [

            open,

            role,

            assignedPermissions,

        ],

    );

    function handlePermissionChange({

        permissionId,

        checked,

    }) {

        setSelectedPermissions(

            (

                previous,

            ) => {

                if (

                    checked

                ) {

                    return [

                        ...previous,

                        permissionId,

                    ];

                }

                return previous.filter(

                    (

                        id,

                    ) =>

                        id !==

                        permissionId,

                );

            },

        );

    }

    async function handleSave() {

        try {

            let savedRole =

                role;

            if (

                role

            ) {

                savedRole =

                    await updateRole.mutateAsync({

                        roleId:

                            role.role_id,

                        data: {

                            role_name:

                                roleName,

                            description,

                        },

                    });

            } else {

                savedRole =

                    await createRole.mutateAsync({

                        role_name:

                            roleName,

                        description,

                        is_system_role:

                            false,

                    });

            }

            await updatePermissions.mutateAsync({

                roleId:

                    savedRole.role_id,

                permissionIds:

                    selectedPermissions,

            });

        } catch (

            error

        ) {

            console.error(

                error,

            );

        }

    }

    return (

        <Dialog

            open={open}

            onClose={onClose}

            fullWidth

            maxWidth="lg"

        >

            <DialogTitle>

                <Stack spacing={1}>

                    <Stack
                        direction="row"
                        spacing={2}
                        alignItems="center"
                    >

                        <Avatar
                            sx={{
                                bgcolor: "primary.main",
                            }}
                        >

                            <ShieldIcon />

                        </Avatar>

                        <Box>

                            <Typography variant="h5">

                                {role
                                    ? "Edit Role"
                                    : "Create Role"}

                            </Typography>

                            <Typography
                                variant="body2"
                                color="text.secondary"
                            >

                                {role
                                    ? "Manage administrator permissions and access levels across the BryanNet ISP Platform."
                                    : "Create a new administrator role and configure its permissions before assigning users."}

                            </Typography>

                        </Box>

                    </Stack>

                </Stack>

            </DialogTitle>

            <DialogContent dividers>

                <Stack spacing={4}>

                    <Box>

                        <Typography

                            variant="h6"

                            gutterBottom

                        >

                            Role Information

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                            sx={{

                                mb: 3,

                            }}

                        >

                            {role

                                ? "Update the role details and review its current configuration."

                                : "Create a new administrator role and assign the permissions it should have."}

                        </Typography>

                        <Stack spacing={3}>

                            <TextField

                                fullWidth

                                required

                                label="Role Name"

                                value={roleName}

                                onChange={(

                                    event,

                                ) =>

                                    setRoleName(

                                        event.target.value,

                                    )

                                }

                            />

                            <TextField

                                fullWidth

                                multiline

                                minRows={3}

                                label="Description"

                                value={description}

                                onChange={(

                                    event,

                                ) =>

                                    setDescription(

                                        event.target.value,

                                    )

                                }

                            />

                        </Stack>

                    </Box>

                    {role && (

                        <>

                            <Divider />

                            <Box>

                                <Typography

                                    variant="h6"

                                    gutterBottom

                                >

                                    Role Summary

                                </Typography>

                                <Typography

                                    variant="body2"

                                    color="text.secondary"

                                    sx={{

                                        mb: 3,

                                    }}

                                >

                                    Overview of this role before changing its permissions.

                                </Typography>

                                <Stack

                                    direction="row"

                                    spacing={1}

                                    flexWrap="wrap"

                                    useFlexGap

                                >

                                    <Chip

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

                                    <Chip

                                        color={

                                            role.is_system_role

                                                ? "primary"

                                                : "default"

                                        }

                                        variant={

                                            role.is_system_role

                                                ? "filled"

                                                : "outlined"

                                        }

                                        label={

                                            role.is_system_role

                                                ? "System Role"

                                                : "Custom Role"

                                        }

                                    />

                                    <Chip

                                        label={`${

                                            role.assigned_users ?? 0

                                        } Administrators`}

                                    />

                                    <Chip

                                        color="secondary"

                                        label={`${

                                            role.permission_count ?? 0

                                        } Permissions`}

                                    />

                                </Stack>

                            </Box>

                        </>

                    )}

                    <Divider />      

                    <Box>

                        <Typography

                            variant="h6"

                            gutterBottom

                        >

                            Permissions

                        </Typography>

                        <Typography

                            variant="body2"

                            color="text.secondary"

                            sx={{

                                mb: 3,

                            }}

                        >

                            Choose the actions administrators with this role can perform throughout the BryanNet ISP Platform.

                        </Typography>

                        {permissionsLoading ||

                        rolePermissionsLoading ? (

                            <Box

                                sx={{

                                    py: 8,

                                    textAlign: "center",

                                }}

                            >

                                <Typography

                                    variant="body1"

                                    color="text.secondary"

                                >

                                    Loading permissions...

                                </Typography>

                            </Box>

                        ) : (

                            <PermissionMatrix

                                permissions={permissions}

                                onPermissionChange={

                                    handlePermissionChange

                                }

                            />

                        )}

                    </Box>

                </Stack>

            </DialogContent>

            <DialogActions

                sx={{

                    px: 3,

                    py: 2,

                    justifyContent:

                        "space-between",

                }}

            >

                <Button

                    onClick={onClose}

                    disabled={

                        createRole.isPending ||

                        updateRole.isPending ||

                        updatePermissions.isPending

                    }

                >

                    Cancel

                </Button>

                <Button

                    variant="contained"

                    size="large"

                    onClick={handleSave}

                    disabled={

                        !roleName.trim() ||

                        permissionsLoading ||

                        rolePermissionsLoading ||

                        createRole.isPending ||

                        updateRole.isPending ||

                        updatePermissions.isPending

                    }

                >

                    {createRole.isPending ||

                    updateRole.isPending ||

                    updatePermissions.isPending

                        ? role

                            ? "Saving Changes..."

                            : "Creating Role..."

                        : role

                            ? "Save Changes"

                            : "Create Role"}

                </Button>

            </DialogActions>

        </Dialog>

    );

}                      