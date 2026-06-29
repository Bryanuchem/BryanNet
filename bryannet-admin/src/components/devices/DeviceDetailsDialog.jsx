import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Stack,
} from "@mui/material";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";

function DeviceDetailsDialog({
    open,
    device,
    onClose,
}) {

    if (!device) {
        return null;
    }

    return (
        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >
            <DialogTitle>
                Device Details
            </DialogTitle>

            <DialogContent>

                <Stack
                    spacing={2.5}
                    sx={{ mt: 1 }}
                >

                    <InfoField
                        label="Device Name"
                        value={device.device_name}
                    />

                    <InfoField
                        label="Customer"
                        value={device.customer_name}
                    />

                    <InfoField
                        label="MAC Address"
                        value={device.mac_address}
                    />

                    <InfoField
                        label="Status"
                    >
                        <BadgeChip
                            variant="status"
                            value={device.device_status}
                        />
                    </InfoField>

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
    );
}

export default DeviceDetailsDialog;