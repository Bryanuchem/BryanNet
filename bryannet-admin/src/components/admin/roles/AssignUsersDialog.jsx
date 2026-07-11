import {

    useMemo,

    useState,

} from "react";

import {

    Avatar,

    Box,

    Button,

    Chip,

    Dialog,

    DialogActions,

    DialogContent,

    DialogTitle,

    Divider,

    List,

    ListItem,

    ListItemAvatar,

    ListItemText,

    MenuItem,

    Stack,

    TextField,

    Typography,

} from "@mui/material";

import SearchBar from "../../common/SearchBar";

import {

    useRoles,

} from "../../../hooks/useRoles";

import {

    useChangeAdminRole,

} from "../../../hooks/useChangeAdminRole";

import AppSnackbar from "../../common/AppSnackbar";

export default function AssignUsersDialog({

    open,

    role,

    administrators = [],

    onClose,

}) {

    const [

        search,

        setSearch,

    ] = useState("");

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

    } = useRoles();

    const changeRole =

        useChangeAdminRole({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Administrator role updated successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.detail ||

                        "Failed to update administrator role.",

                });

            },

        });

    const filteredUsers = useMemo(

        () => {

            const query =

                search

                    .trim()

                    .toLowerCase();

            const items =

                administrators.items ??

                administrators;

            if (

                !query

            ) {

                return items;

            }

            return items.filter(

                (

                    administrator,

                ) =>

                    administrator.username

                        ?.toLowerCase()

                        .includes(

                            query,

                        ) ||

                    administrator.email

                        ?.toLowerCase()

                        .includes(

                            query,

                        ),

            );

        },

        [

            administrators,

            search,

        ],

    );

    function handleRoleChange(

        adminUser,

        newRoleId,

    ) {

        if (

            Number(

                adminUser.role_id,

            ) === Number(

                newRoleId,

            )

        ) {

            return;

        }

        changeRole.mutate({

            adminUserId:

                adminUser.admin_user_id,

            roleId:

                Number(

                    newRoleId,

                ),

        });

    }

    return (

        <>

            <Dialog

                open={open}

                onClose={onClose}

                fullWidth

                maxWidth="md"

            >

                <DialogTitle>

                    Manage Administrators

                </DialogTitle>

                <DialogContent dividers>

                    <Stack spacing={3}>

                        <Stack spacing={1}>

                            <Typography>

                                Role

                            </Typography>

                            <Chip

                                color="primary"

                                label={

                                    role?.role_name ??

                                    "-"

                                }

                            />

                        </Stack>

                        <SearchBar

                            value={search}

                            onChange={(

                                event,

                            ) =>

                                setSearch(

                                    event.target.value,

                                )

                            }

                            placeholder="Search administrators..."

                        />

                        <Divider />

                        <List disablePadding>

                            {filteredUsers.map(

                                (

                                    administrator,

                                ) => (

                                    <ListItem

                                        key={

                                            administrator.admin_user_id

                                        }

                                        secondaryAction={

                                            <TextField

                                                select

                                                size="small"

                                                value={

                                                    administrator.role_id

                                                }

                                                onChange={(

                                                    event,

                                                ) =>

                                                    handleRoleChange(

                                                        administrator,

                                                        event.target.value,

                                                    )

                                                }

                                                sx={{

                                                    minWidth: 180,

                                                }}

                                            >

                                                {roles.map(

                                                    (

                                                        item,

                                                    ) => (

                                                        <MenuItem

                                                            key={

                                                                item.role_id

                                                            }

                                                            value={

                                                                item.role_id

                                                            }

                                                        >

                                                            {

                                                                item.role_name

                                                            }

                                                        </MenuItem>

                                                    ),

                                                )}

                                            </TextField>

                                        }

                                    >

                                        <ListItemAvatar>

                                            <Avatar>

                                                {administrator.username?.charAt(

                                                    0,

                                                )}

                                            </Avatar>

                                        </ListItemAvatar>

                                        <ListItemText

                                            primary={

                                                administrator.username

                                            }

                                            secondary={

                                                administrator.email

                                            }

                                        />

                                    </ListItem>

                                ),

                            )}

                            {filteredUsers.length === 0 && (

                                <Box

                                    sx={{

                                        py: 6,

                                        textAlign: "center",

                                    }}

                                >

                                    <Typography

                                        color="text.secondary"

                                    >

                                        No administrators found.

                                    </Typography>

                                </Box>

                            )}

                        </List>

                    </Stack>

                </DialogContent>

                <DialogActions>

                    <Button

                        onClick={onClose}

                    >

                        Close

                    </Button>

                </DialogActions>

            </Dialog>

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

        </>

    );

}