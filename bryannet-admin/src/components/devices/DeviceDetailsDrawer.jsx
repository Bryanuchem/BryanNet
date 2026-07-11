import { useState } from "react";

import {
    Avatar,
    Box,
    Button,
    Card,
    CardContent,
    Divider,
    Drawer,
    IconButton,
    Stack,
    Tooltip,
    Typography,
} from "@mui/material";

import MemoryIcon from "@mui/icons-material/Memory";
import PersonIcon from "@mui/icons-material/Person";
import WifiIcon from "@mui/icons-material/Wifi";
import ShieldIcon from "@mui/icons-material/Shield";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";
import AppSnackbar from "../common/AppSnackbar";

function DeviceDetailsDrawer({

    open,

    device,

    onClose,

}) {

    const [
        snackbarOpen,
        setSnackbarOpen,
    ] = useState(false);

    if (!device) {
        return null;
    }

    const deviceName =
        device.device_name?.trim() ||
        "Unnamed Device";

    const customerName =
        device.customer_name?.trim() ||
        "Unknown Customer";

    const initials = deviceName

        .split(" ")

        .filter(Boolean)

        .map((word) => word[0])

        .join("")

        .slice(0, 2)

        .toUpperCase();

    const copyMacAddress = async () => {

        try {

            await navigator.clipboard.writeText(
                device.mac_address,
            );

            setSnackbarOpen(true);

        } catch (error) {

            console.error(error);

        }

    };

    return (

        <>

            <Drawer
                anchor="right"
                open={open}
                onClose={onClose}
            >

                <Box
                    sx={{
                        width: 450,
                        height: "100%",
                        bgcolor: "#F8FAFC",
                        display: "flex",
                        flexDirection: "column",
                    }}
                >

                    {/* Header */}

                    <Box
                        sx={{
                            bgcolor: "primary.main",
                            color: "white",
                            p: 4,
                        }}
                    >

                        <Stack
                            direction="row"
                            spacing={2}
                            alignItems="center"
                        >

                            <Avatar
                                sx={{
                                    width: 72,
                                    height: 72,
                                    fontSize: 28,
                                    bgcolor: "white",
                                    color: "primary.main",
                                    fontWeight: 700,
                                }}
                            >
                                {initials}
                            </Avatar>

                            <Box>

                                <Typography variant="overline">
                                    Device Details
                                </Typography>

                                <Typography
                                    variant="h4"
                                    fontWeight={700}
                                >
                                    {deviceName}
                                </Typography>

                                <Typography
                                    sx={{
                                        opacity: 0.85,
                                    }}
                                >
                                    Device #{device.device_id}
                                </Typography>

                            </Box>

                        </Stack>

                    </Box>

                    {/* Content */}

                    <Box
                        sx={{
                            flex: 1,
                            overflowY: "auto",
                            p: 3,
                        }}
                    >

                        {/* Device Information */}

                        <Card elevation={1}>

                            <CardContent>

                                <Typography
                                    variant="subtitle2"
                                    fontWeight={700}
                                    gutterBottom
                                >
                                    DEVICE INFORMATION
                                </Typography>

                                <Divider sx={{ mb: 3 }} />

                                <Stack spacing={3}>

                                    <InfoField
                                        icon={<MemoryIcon />}
                                        label="Device Name"
                                    >
                                        <Typography fontWeight={500}>
                                            {deviceName}
                                        </Typography>
                                    </InfoField>

                                    <InfoField
                                        icon={<WifiIcon />}
                                        label="MAC Address"
                                    >

                                        <Stack
                                            direction="row"
                                            spacing={1}
                                            alignItems="center"
                                        >

                                            <Typography fontWeight={500}>
                                                {device.mac_address}
                                            </Typography>

                                            <Tooltip title="Copy">

                                                <IconButton
                                                    size="small"
                                                    onClick={
                                                        copyMacAddress
                                                    }
                                                >

                                                    <ContentCopyIcon fontSize="small" />

                                                </IconButton>

                                            </Tooltip>

                                        </Stack>

                                    </InfoField>

                                    <InfoField
                                        icon={<ShieldIcon />}
                                        label="Device Status"
                                    >

                                    <BadgeChip
                                        status={
                                            device.device_status
                                        }
                                    />

                                    </InfoField>

                                    <InfoField
                                        icon={<ShieldIcon />}
                                        label="Customer Approval"
                                    >

                                        <BadgeChip
                                            label={
                                                device.approved_by_customer
                                                    ? "Approved"
                                                    : "Pending"
                                            }
                                            color={
                                                device.approved_by_customer
                                                    ? "success"
                                                    : "warning"
                                            }
                                        />

                                    </InfoField>

                                    <InfoField
                                        icon={<AccessTimeIcon />}
                                        label="First Seen"
                                    >
                                        <Typography fontWeight={500}>
                                            {device.first_seen
                                                ? new Date(
                                                    device.first_seen,
                                                ).toLocaleString()
                                                : "Never"}
                                        </Typography>
                                    </InfoField>

                                    <InfoField
                                        icon={<AccessTimeIcon />}
                                        label="Last Seen"
                                    >
                                        <Typography fontWeight={500}>
                                            {device.last_seen
                                                ? new Date(
                                                    device.last_seen,
                                                ).toLocaleString()
                                                : "Never"}
                                        </Typography>
                                    </InfoField>

                                </Stack>

                            </CardContent>

                        </Card>

                        {/* Customer Information */}

                        <Card
                            elevation={1}
                            sx={{
                                mt: 3,
                            }}
                        >

                            <CardContent>

                                <Typography
                                    variant="subtitle2"
                                    fontWeight={700}
                                    gutterBottom
                                >
                                    CUSTOMER INFORMATION
                                </Typography>

                                <Divider sx={{ mb: 3 }} />

                                <Stack spacing={3}>

                                    <InfoField
                                        icon={<PersonIcon />}
                                        label="Customer"
                                    >
                                        <Typography fontWeight={500}>
                                            {customerName}
                                        </Typography>
                                    </InfoField>

                                    <InfoField
                                        icon={<PersonIcon />}
                                        label="Customer ID"
                                    >
                                        <Typography fontWeight={500}>
                                            #{device.customer_id}
                                        </Typography>
                                    </InfoField>

                                </Stack>

                            </CardContent>

                        </Card>

                    </Box>

                    {/* Footer */}

                    <Box
                        sx={{
                            p: 3,
                            bgcolor: "white",
                            borderTop:
                                "1px solid #E5E7EB",
                        }}
                    >

                        <Button
                            fullWidth
                            variant="contained"
                            size="large"
                            onClick={onClose}
                        >
                            Close
                        </Button>

                    </Box>

                </Box>

            </Drawer>

            <AppSnackbar
                open={snackbarOpen}
                message="MAC address copied"
                onClose={() =>
                    setSnackbarOpen(false)
                }
            />

        </>

    );

}

export default DeviceDetailsDrawer;                                    