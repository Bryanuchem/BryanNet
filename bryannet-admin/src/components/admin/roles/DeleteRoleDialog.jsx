import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Stack,
  Typography,
} from "@mui/material";

export default function DeleteRoleDialog({
  open,
  role,
  onClose,
}) {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="xs"
    >
      <DialogTitle>
        Delete Role
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3}>
          <Typography>
            Are you sure you want to delete the role{" "}
            <strong>{role?.name ?? "this role"}</strong>?
          </Typography>

          <Alert severity="warning">
            This action cannot be undone. Any administrators currently assigned
            to this role will need to be reassigned before the role can be
            permanently removed.
          </Alert>
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Cancel
        </Button>

        <Button
          variant="contained"
          color="error"
          onClick={onClose}
        >
          Delete Role
        </Button>
      </DialogActions>
    </Dialog>
  );
}