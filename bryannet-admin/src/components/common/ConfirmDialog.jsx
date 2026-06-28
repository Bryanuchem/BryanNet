import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from "@mui/material";

function ConfirmDialog({
    open,
    title,
    message,
    confirmText = "Confirm",
    cancelText = "Cancel",
    confirmColor = "primary",
    loading = false,
    onConfirm,
    onClose,
}) {
    return (
        <Dialog
            open={open}
            onClose={loading ? undefined : onClose}
            maxWidth="xs"
            fullWidth
        >
            <DialogTitle>
                {title}
            </DialogTitle>

            <DialogContent>
                <DialogContentText>
                    {message}
                </DialogContentText>
            </DialogContent>

            <DialogActions>
                <Button
                    onClick={onClose}
                    disabled={loading}
                >
                    {cancelText}
                </Button>

                <Button
                    variant="contained"
                    color={confirmColor}
                    onClick={onConfirm}
                    disabled={loading}
                >
                    {loading ? "Please wait..." : confirmText}
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default ConfirmDialog;