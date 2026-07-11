import {

    Alert,

    Button,

    Chip,

    Dialog,

    DialogActions,

    DialogContent,

    DialogTitle,

    Divider,

    Stack,

    Typography,

} from "@mui/material";

export default function DeleteRoleDialog({

    open,

    role,

    onClose,

    onDelete,

    loading = false,

}) {

    const assignedUsers =

        role?.assigned_users ?? 0;

    const permissionCount =

        role?.permission_count ?? 0;

    const canDelete =

        !role?.is_system_role &&

        assignedUsers === 0;

    return (

        <Dialog

            open={open}

            onClose={

                loading

                    ? undefined

                    : onClose

            }

            fullWidth

            maxWidth="sm"

        >

            <DialogTitle>

                Delete Role

            </DialogTitle>

            <DialogContent dividers>

                <Stack spacing={3}>

                    <Typography>

                        You're about to permanently delete this role. This action cannot be undone.

                    </Typography>

                    <Stack spacing={2}>

                        <Stack

                            direction="row"

                            justifyContent="space-between"

                            alignItems="center"

                        >

                            <Typography

                                color="text.secondary"

                            >

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

                        <Divider />

                        <Stack

                            direction="row"

                            justifyContent="space-between"

                            alignItems="center"

                        >

                            <Typography

                                color="text.secondary"

                            >

                                Assigned Administrators

                            </Typography>

                            <Typography

                                fontWeight={600}

                            >

                                {assignedUsers}

                            </Typography>

                        </Stack>

                        <Stack

                            direction="row"

                            justifyContent="space-between"

                            alignItems="center"

                        >

                            <Typography

                                color="text.secondary"

                            >

                                Permissions

                            </Typography>

                            <Typography

                                fontWeight={600}

                            >

                                {permissionCount}

                            </Typography>

                        </Stack>

                    </Stack>

                    {role?.is_system_role ? (

                        <Alert severity="error">

                            This is a system role and cannot be deleted.

                        </Alert>

                    ) : assignedUsers > 0 ? (

                        <Alert severity="warning">

                            Remove or reassign all administrators before deleting this role.

                        </Alert>

                    ) : (

                        <Alert severity="warning">

                            Deleting this role will permanently remove its permission assignments.

                        </Alert>

                    )}

                </Stack>

            </DialogContent>

            <DialogActions>

                <Button

                    onClick={onClose}

                    disabled={loading}

                >

                    Cancel

                </Button>

                <Button

                    variant="contained"

                    color="error"

                    disabled={

                        !canDelete ||

                        loading

                    }

                    onClick={onDelete}

                >

                    {loading

                        ? "Deleting Role..."

                        : "Delete Role"}

                </Button>

            </DialogActions>

        </Dialog>

    );

}