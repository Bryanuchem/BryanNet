import { useMemo, useState } from "react";

import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Alert,
    Box,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Grid,
    Stack,
    TextField,
    Typography,
    Button,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import SearchIcon from "@mui/icons-material/Search";
import SecurityIcon from "@mui/icons-material/Security";
import GroupIcon from "@mui/icons-material/Group";
import AppsIcon from "@mui/icons-material/Apps";

import { useRolePermissions } from "../../../hooks/useRolePermissions";

export default function RoleDetailsDialog({

    open,

    role,

    onClose,

}) {

    const [

        search,

        setSearch,

    ] = useState("");

    const {

        data: permissions = [],

        isLoading,

        isError,

    } = useRolePermissions(

        role?.role_id,

    );

    // ==========================================================
    // Helpers
    // ==========================================================

    function normalize(

        value = "",

    ) {

        return value

            .toLowerCase()

            .replace(

                /\b\w/g,

                (character) =>

                    character.toUpperCase(),

            );

    }

    const groupedPermissions = useMemo(() => {

        const grouped = {};

        permissions.forEach(

            (permission) => {

                const module = normalize(

                    permission.module,

                );

                const action = normalize(

                    permission.action,

                );

                if (

                    search.trim() &&

                    !module
                        .toLowerCase()
                        .includes(

                            search.toLowerCase(),

                        ) &&

                    !action
                        .toLowerCase()
                        .includes(

                            search.toLowerCase(),

                        )

                ) {

                    return;

                }

                if (

                    !grouped[module]

                ) {

                    grouped[module] = [];

                }

                grouped[module].push({

                    ...permission,

                    module,

                    action,

                });

            },

        );

        Object.keys(

            grouped,

        ).forEach(

            (module) => {

                grouped[module].sort(

                    (

                        a,

                        b,

                    ) =>

                        a.action.localeCompare(

                            b.action,

                        ),

                );

            },

        );

        return Object.entries(

            grouped,

        ).sort(

            (

                a,

                b,

            ) =>

                a[0].localeCompare(

                    b[0],

                ),

        );

    }, [

        permissions,

        search,

    ]);

    const moduleCount = useMemo(

        () =>

            new Set(

                permissions.map(

                    (permission) =>

                        normalize(

                            permission.module,

                        ),

                ),

            ).size,

        [

            permissions,

        ],

    );

    // ==========================================================
    // Render
    // ==========================================================

    return (

        <Dialog

            open={open}

            onClose={onClose}

            maxWidth="lg"

            fullWidth

        >

            <DialogTitle>

                <Stack

                    spacing={2}

                >

                    <Stack

                        direction="row"

                        justifyContent="space-between"

                        alignItems="center"

                    >

                        <Box>

                            <Typography

                                variant="h5"

                                fontWeight={700}

                            >

                                Role Profile

                            </Typography>

                            <Typography

                                variant="body2"

                                color="text.secondary"

                            >

                                View role details and assigned permissions.

                            </Typography>

                        </Box>

                        <Chip

                            color="primary"

                            label={`${

                                role?.permission_count ?? 0

                            } Permissions`}

                        />

                    </Stack>

                    <Divider />

                    <Stack

                        spacing={1}

                    >

                        <Typography

                            variant="h5"

                            fontWeight={700}

                        >

                            {

                                role?.role_name

                            }

                        </Typography>

                        <Typography

                            color="text.secondary"

                        >

                            {

                                role?.description ||

                                "No description provided."

                            }

                        </Typography>

                        <Stack

                            direction="row"

                            spacing={1}

                            flexWrap="wrap"

                        >

                            <Chip

                                color={

                                    role?.is_active

                                        ? "success"

                                        : "default"

                                }

                                label={

                                    role?.is_active

                                        ? "Active"

                                        : "Inactive"

                                }

                            />

                            <Chip

                                color={

                                    role?.is_system_role

                                        ? "primary"

                                        : "default"

                                }

                                label={

                                    role?.is_system_role

                                        ? "System Role"

                                        : "Custom Role"

                                }

                            />

                        </Stack>

                    </Stack>

                </Stack>

            </DialogTitle>

            <DialogContent dividers>

                {isLoading && (

                    <Box

                        py={10}

                        display="flex"

                        justifyContent="center"

                    >

                        <CircularProgress />

                    </Box>

                )}

                {isError && (

                    <Alert

                        severity="error"

                    >

                        Failed to load role permissions.

                    </Alert>

                )}

                {!isLoading &&

                    !isError && (

                        <Stack

                            spacing={3}

                        >

                            <Grid

                                container

                                spacing={2}

                            >

                                <Grid item xs={12} md={4}>

                                    <Card>

                                        <CardContent>

                                            <Stack

                                                spacing={1}

                                                alignItems="center"

                                            >

                                                <GroupIcon

                                                    color="primary"

                                                />

                                                <Typography

                                                    variant="h4"

                                                >

                                                    {

                                                        role?.assigned_users ??

                                                        0

                                                    }

                                                </Typography>

                                                <Typography

                                                    color="text.secondary"

                                                >

                                                    Assigned Users

                                                </Typography>

                                            </Stack>

                                        </CardContent>

                                    </Card>

                                </Grid>

                                <Grid

                                    size={4}

                                >

                                    <Card>

                                        <CardContent>

                                            <Stack

                                                spacing={1}

                                                alignItems="center"

                                            >

                                                <SecurityIcon

                                                    color="primary"

                                                />

                                                <Typography

                                                    variant="h4"

                                                >

                                                    {

                                                        role?.permission_count ??

                                                        0

                                                    }

                                                </Typography>

                                                <Typography

                                                    color="text.secondary"

                                                >

                                                    Permissions

                                                </Typography>

                                            </Stack>

                                        </CardContent>

                                    </Card>

                                </Grid>

                                <Grid

                                    size={4}

                                >

                                    <Card>

                                        <CardContent>

                                            <Stack

                                                spacing={1}

                                                alignItems="center"

                                            >

                                                <AppsIcon

                                                    color="primary"

                                                />

                                                <Typography

                                                    variant="h4"

                                                >

                                                    {

                                                        moduleCount

                                                    }

                                                </Typography>

                                                <Typography

                                                    color="text.secondary"

                                                >

                                                    Modules

                                                </Typography>

                                            </Stack>

                                        </CardContent>

                                    </Card>

                                </Grid>

                            </Grid>

                            <TextField

                                fullWidth

                                value={search}

                                onChange={(event) =>

                                    setSearch(

                                        event.target.value,

                                    )

                                }

                                placeholder="Search permissions..."

                                InputProps={{

                                    startAdornment: (

                                        <SearchIcon

                                            sx={{

                                                mr: 1,

                                                color:

                                                    "text.secondary",

                                            }}

                                        />

                                    ),

                                }}

                            />

                            {groupedPermissions.length === 0 ? (

                                <Alert

                                    severity="info"

                                >

                                    No permissions matched your search.

                                </Alert>

                            ) : (

                                <Stack

                                    spacing={2}

                                >

                                    {groupedPermissions.map(

                                        ([

                                            module,

                                            modulePermissions,

                                        ]) => (

                                            <Accordion

                                                key={module}

                                                defaultExpanded

                                                disableGutters

                                                elevation={0}

                                                sx={{

                                                    border: (theme) =>

                                                        `1px solid ${theme.palette.divider}`,

                                                    borderRadius: "12px !important",

                                                    overflow: "hidden",

                                                    "&::before": {

                                                        display: "none",

                                                    },

                                                }}

                                            >

                                                <AccordionSummary

                                                    expandIcon={

                                                        <ExpandMoreIcon />

                                                    }

                                                >

                                                    <Stack

                                                        direction="row"

                                                        justifyContent="space-between"

                                                        alignItems="center"

                                                        width="100%"

                                                        pr={2}

                                                    >

                                                        <Typography

                                                            fontWeight={600}

                                                        >

                                                            {module}

                                                        </Typography>

                                                        <Chip

                                                            size="small"

                                                            color="primary"

                                                            label={`${

                                                                modulePermissions.length

                                                            } Permission${

                                                                modulePermissions.length !== 1

                                                                    ? "s"

                                                                    : ""

                                                            }`}

                                                        />

                                                    </Stack>

                                                </AccordionSummary>

                                                <AccordionDetails>

                                                    <Stack

                                                        direction="row"

                                                        spacing={1}

                                                        useFlexGap

                                                        flexWrap="wrap"

                                                    >

                                                        {modulePermissions.map(

                                                            (

                                                                permission,

                                                            ) => (

                                                                <Chip

                                                                    key={

                                                                        permission.permission_id

                                                                    }

                                                                    label={

                                                                        permission.action

                                                                    }

                                                                    variant="outlined"

                                                                    color="primary"

                                                                    sx={{

                                                                        borderRadius: 2,

                                                                    }}

                                                                />

                                                            ),

                                                        )}

                                                    </Stack>

                                                </AccordionDetails>

                                            </Accordion>

                                        ),

                                    )}

                                </Stack>

                            )}

                        </Stack>

                    )}

            </DialogContent>

            <DialogActions

                sx={{

                    px: 3,

                    py: 2,

                }}

            >

                <Button

                    variant="outlined"

                    onClick={onClose}

                >

                    Close

                </Button>

            </DialogActions>

        </Dialog>

    );

}