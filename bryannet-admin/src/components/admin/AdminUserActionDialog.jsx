import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Typography,
} from "@mui/material";

const dialogConfig = {
    delete: {
        title: "Delete Administrator",
        description:
            "Are you sure you want to permanently delete this administrator? This action cannot be undone.",
        confirmText: "Delete",
        color: "error",
    },

    activate: {
        title: "Activate Administrator",
        description:
            "This administrator will regain access to the BryanNet Admin Dashboard.",
        confirmText: "Activate",
        color: "success",
    },

    deactivate: {
        title: "Deactivate Administrator",
        description:
            "This administrator will no longer be able to access the BryanNet Admin Dashboard until reactivated.",
        confirmText: "Deactivate",
        color: "warning",
    },

    resetPassword: {
        title: "Reset Password",
        description:
            "A temporary password will be generated for this administrator. They will be required to change it after logging in.",
        confirmText: "Reset Password",
        color: "primary",
    },
};

export default function AdminUserActionDialog({
    open,
    type,
    administrator,
    loading = false,
    onClose,
    onConfirm,
}) {
    if (!type) return null;

    const config = dialogConfig[type];

    if (!config) return null;

    return (
        <Dialog
            open={open}
            onClose={loading ? undefined : onClose}
            fullWidth
            maxWidth="xs"
        >
            <DialogTitle>
                {config.title}
            </DialogTitle>

            <DialogContent dividers>
                <Typography
                    variant="body1"
                    gutterBottom
                >
                    {config.description}
                </Typography>

                {administrator && (
                    <Typography
                        variant="subtitle2"
                        color="text.secondary"
                        sx={{ mt: 2 }}
                    >
                        Administrator:
                        <br />
                        <strong>
                            {administrator.name}
                        </strong>
                    </Typography>
                )}
            </DialogContent>

            <DialogActions>
                <Button
                    disabled={loading}
                    onClick={onClose}
                >
                    Cancel
                </Button>

                <Button
                    variant="contained"
                    color={config.color}
                    disabled={loading}
                    onClick={() =>
                        onConfirm?.(
                            administrator,
                            type
                        )
                    }
                >
                    {config.confirmText}
                </Button>
            </DialogActions>
        </Dialog>
    );
}