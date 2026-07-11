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

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import PauseCircleIcon from "@mui/icons-material/PauseCircle";

export default function RoleActivationDialog({

    open,

    role,

    onClose,

    onConfirm,

    loading = false,

}) {

    const activating =

        !role?.is_active;

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

                {activating

                    ? "Activate Role"

                    : "Deactivate Role"}

            </DialogTitle>

            <DialogContent dividers>

                <Stack spacing={3}>

                    <Typography>

                        {activating

                            ? "You're about to activate this administrator role. Administrators assigned to this role will regain access to the BryanNet dashboard."

                            : "You're about to deactivate this administrator role. Administrators assigned to this role will no longer be able to sign in until the role is activated again."}

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

                                Status

                            </Typography>

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

                        </Stack>

                        {role?.is_system_role && (

                            <Stack

                                direction="row"

                                justifyContent="space-between"

                                alignItems="center"

                            >

                                <Typography

                                    color="text.secondary"

                                >

                                    Type

                                </Typography>

                                <Chip

                                    color="primary"

                                    label="System Role"

                                />

                            </Stack>

                        )}

                    </Stack>

                    {activating ? (

                        <Alert

                            severity="success"

                            icon={

                                <CheckCircleIcon />

                            }

                        >

                            This role will become available for use immediately after activation.

                        </Alert>

                    ) : (

                        <Alert

                            severity="warning"

                            icon={

                                <PauseCircleIcon />

                            }

                        >

                            Administrators assigned to this role will be unable to access the platform until it is activated again.

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

                    color={

                        activating

                            ? "success"

                            : "warning"

                    }

                    onClick={onConfirm}

                    disabled={loading}

                >

                    {loading

                        ? activating

                            ? "Activating..."

                            : "Deactivating..."

                        : activating

                            ? "Activate Role"

                            : "Deactivate Role"}

                </Button>

            </DialogActions>

        </Dialog>

    );

}