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

import PhoneIcon from "@mui/icons-material/Phone";
import EmailIcon from "@mui/icons-material/Email";
import TelegramIcon from "@mui/icons-material/Telegram";
import AssignmentTurnedInIcon from "@mui/icons-material/AssignmentTurnedIn";
import BlockIcon from "@mui/icons-material/Block";
import ChecklistIcon from "@mui/icons-material/Checklist";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";
import AppSnackbar from "../common/AppSnackbar";

import {
    formatPhoneNumber,
} from "../../utils/customerFormatter";

function CustomerDetailsDrawer({
    open,
    customer,
    onClose,
}) {
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    if (!customer) return null;

    const fullName =
        customer.full_name?.trim() || "Unknown Customer";

    const phoneNumber =
        formatPhoneNumber(customer.phone_number);

    const registrationStep =
        customer.registration_step ??
         "START";

    const initials = fullName
        .split(" ")
        .filter(Boolean)
        .map((name) => name[0])
        .join("")
        .slice(0, 2)
        .toUpperCase();

    const copyPhoneNumber = async () => {
        try {
            if (customer.phone_number) {
                await navigator.clipboard.writeText(
                    customer.phone_number
                );

                setSnackbarOpen(true);
            }
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
                                    Customer Details
                                </Typography>

                                <Typography
                                    variant="h4"
                                    fontWeight={700}
                                >
                                    {fullName}
                                </Typography>

                                <Typography
                                    sx={{
                                        opacity: 0.85,
                                    }}
                                >
                                    Customer #{customer.customer_id}
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
                        <Card elevation={1}>
                            <CardContent>

                                <Typography
                                    variant="subtitle2"
                                    fontWeight={700}
                                    gutterBottom
                                >
                                    PERSONAL INFORMATION
                                </Typography>

                                <Divider sx={{ mb: 3 }} />

                                <Stack spacing={3}>

                                    <InfoField
                                        icon={<PhoneIcon />}
                                        label="Phone Number"
                                    >
                                        <Stack
                                            direction="row"
                                            spacing={1}
                                            alignItems="center"
                                        >
                                            <Typography fontWeight={500}>
                                                {phoneNumber}
                                            </Typography>

                                            {customer.phone_number && (
                                                <Tooltip title="Copy">
                                                    <IconButton
                                                        size="small"
                                                        onClick={copyPhoneNumber}
                                                    >
                                                        <ContentCopyIcon fontSize="small" />
                                                    </IconButton>
                                                </Tooltip>
                                            )}
                                        </Stack>
                                    </InfoField>

                                    <InfoField
                                        icon={<EmailIcon />}
                                        label="Email Address"
                                    >
                                        <Typography fontWeight={500}>
                                            {customer.email ?? "Not provided"}
                                        </Typography>
                                    </InfoField>

                                    <InfoField
                                        icon={<AssignmentTurnedInIcon />}
                                        label="Registration"
                                    >
                                        <BadgeChip
                                            label={
                                                customer.is_registered
                                                    ? "Registered"
                                                    : "Pending"
                                            }
                                            color={
                                                customer.is_registered
                                                    ? "success"
                                                    : "warning"
                                            }
                                        />
                                    </InfoField>

                                    <InfoField
                                        icon={<BlockIcon />}
                                        label="Status"
                                    >
                                        <BadgeChip
                                            label={
                                                customer.status === "active"
                                                    ? "Active"
                                                    : "Inactive"
                                            }
                                            color={
                                                customer.status === "active"
                                                    ? "success"
                                                    : "error"
                                            }
                                        />
                                    </InfoField>

                                    <InfoField
                                        icon={<TelegramIcon />}
                                        label="Telegram"
                                    >
                                        <BadgeChip
                                            label={
                                                customer.telegram_user_id
                                                    ? "Linked"
                                                    : "Not Linked"
                                            }
                                            color={
                                                customer.telegram_user_id
                                                    ? "info"
                                                    : "default"
                                            }
                                        />
                                    </InfoField>

                                    <InfoField
                                        icon={<ChecklistIcon />}
                                        label="Registration Step"
                                    >
                                        <BadgeChip
                                            variant="registrationStep"
                                            value={registrationStep}
                                        />
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
                            borderTop: "1px solid #E5E7EB",
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
                message="Phone number copied"
                onClose={() => setSnackbarOpen(false)}
            />
        </>
    );
}

export default CustomerDetailsDrawer;