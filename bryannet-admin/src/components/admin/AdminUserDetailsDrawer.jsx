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
    MenuItem,
    Stack,
    TextField,
    Tooltip,
    Typography,
} from "@mui/material";

import PersonIcon from "@mui/icons-material/Person";
import AlternateEmailIcon from "@mui/icons-material/AlternateEmail";
import PhoneIcon from "@mui/icons-material/Phone";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import SecurityIcon from "@mui/icons-material/Security";
import KeyIcon from "@mui/icons-material/Key";
import DevicesIcon from "@mui/icons-material/Devices";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";
import AppSnackbar from "../common/AppSnackbar";

function AdminUserDetailsDrawer({
    open,
    administrator,
    drawerMode,
    onDrawerModeChange,
    onClose,
}) {
    const [snackbarOpen, setSnackbarOpen] =
        useState(false);

    const [formData, setFormData] =
        useState({});

    if (!administrator) return null;

    const initials = administrator.name
        ?.split(" ")
        .filter(Boolean)
        .map((part) => part[0])
        .join("")
        .slice(0, 2)
        .toUpperCase();

    const currentData =
        drawerMode === "details"
            ? administrator
            : {
                  ...administrator,
                  ...formData,
              };

    const handleChange = (event) => {
        const { name, value } = event.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const copyEmail = async () => {
        try {
            if (administrator.email) {
                await navigator.clipboard.writeText(
                    administrator.email
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
                                    {drawerMode ===
                                    "create"
                                        ? "New Administrator"
                                        : drawerMode ===
                                          "edit"
                                        ? "Edit Administrator"
                                        : "Administrator Details"}
                                </Typography>

                                <Typography
                                    variant="h4"
                                    fontWeight={700}
                                >
                                    {drawerMode ===
                                    "create"
                                        ? "New Administrator"
                                        : currentData.name}
                                </Typography>

                                <Typography
                                    sx={{
                                        opacity: 0.85,
                                    }}
                                >
                                    {drawerMode ===
                                    "create"
                                        ? "Create a new dashboard administrator"
                                        : currentData.role}
                                </Typography>
                            </Box>
                        </Stack>
                    </Box>

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
                                    ACCOUNT INFORMATION
                                </Typography>

                                <Divider sx={{ mb: 3 }} />

                                {drawerMode ===
                                "details" ? (
                                    <Stack
                                        spacing={3}
                                    >
                                        <InfoField
                                            icon={
                                                <PersonIcon />
                                            }
                                            label="Username"
                                        >
                                            <Typography fontWeight={500}>
                                                {
                                                    currentData.username
                                                }
                                            </Typography>
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <AlternateEmailIcon />
                                            }
                                            label="Email"
                                        >
                                            <Stack
                                                direction="row"
                                                spacing={1}
                                                alignItems="center"
                                            >
                                                <Typography fontWeight={500}>
                                                    {
                                                        currentData.email
                                                    }
                                                </Typography>

                                                <Tooltip title="Copy">
                                                    <IconButton
                                                        size="small"
                                                        onClick={
                                                            copyEmail
                                                        }
                                                    >
                                                        <ContentCopyIcon fontSize="small" />
                                                    </IconButton>
                                                </Tooltip>
                                            </Stack>
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <PhoneIcon />
                                            }
                                            label="Phone"
                                        >
                                            <Typography fontWeight={500}>
                                                {currentData.phone ??
                                                    "-"}
                                            </Typography>
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <AdminPanelSettingsIcon />
                                            }
                                            label="Role"
                                        >
                                            <Typography fontWeight={500}>
                                                {
                                                    currentData.role
                                                }
                                            </Typography>
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <SecurityIcon />
                                            }
                                            label="Status"
                                        >
                                            <BadgeChip
                                                label={
                                                    currentData.status
                                                }
                                                color={
                                                    currentData.status ===
                                                    "Active"
                                                        ? "success"
                                                        : "default"
                                                }
                                            />
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <CalendarTodayIcon />
                                            }
                                            label="Created"
                                        >
                                            <Typography fontWeight={500}>
                                                {currentData.created ??
                                                    "-"}
                                            </Typography>
                                        </InfoField>

                                        <InfoField
                                            icon={
                                                <AccessTimeIcon />
                                            }
                                            label="Last Login"
                                        >
                                            <Typography fontWeight={500}>
                                                {
                                                    currentData.lastLogin
                                                }
                                            </Typography>
                                        </InfoField>
                                    </Stack>
                                ) : (
                                    <Stack
                                        spacing={2}
                                    >
                                        <TextField
                                            label="Full Name"
                                            name="name"
                                            fullWidth
                                            value={
                                                formData.name ??
                                                currentData.name ??
                                                ""
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        />

                                        <TextField
                                            label="Username"
                                            name="username"
                                            fullWidth
                                            value={
                                                formData.username ??
                                                currentData.username ??
                                                ""
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        />

                                        <TextField
                                            label="Email"
                                            name="email"
                                            fullWidth
                                            value={
                                                formData.email ??
                                                currentData.email ??
                                                ""
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        />

                                        <TextField
                                            label="Phone"
                                            name="phone"
                                            fullWidth
                                            value={
                                                formData.phone ??
                                                currentData.phone ??
                                                ""
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        />

                                        <TextField
                                            select
                                            label="Role"
                                            name="role"
                                            fullWidth
                                            value={
                                                formData.role ??
                                                currentData.role ??
                                                ""
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        >
                                            <MenuItem value="Super Administrator">
                                                Super
                                                Administrator
                                            </MenuItem>

                                            <MenuItem value="Administrator">
                                                Administrator
                                            </MenuItem>

                                            <MenuItem value="Support">
                                                Support
                                            </MenuItem>
                                        </TextField>

                                        <TextField
                                            select
                                            label="Status"
                                            name="status"
                                            fullWidth
                                            value={
                                                formData.status ??
                                                currentData.status ??
                                                "Active"
                                            }
                                            onChange={
                                                handleChange
                                            }
                                        >
                                            <MenuItem value="Active">
                                                Active
                                            </MenuItem>

                                            <MenuItem value="Inactive">
                                                Inactive
                                            </MenuItem>
                                        </TextField>
                                    </Stack>
                                )}
                            </CardContent>
                        </Card>

                        <Card
                            elevation={1}
                            sx={{ mt: 3 }}
                        >
                            <CardContent>
                                <Typography
                                    variant="subtitle2"
                                    fontWeight={700}
                                    gutterBottom
                                >
                                    SECURITY
                                </Typography>

                                <Divider sx={{ mb: 3 }} />

                                <Stack spacing={3}>
                                    <InfoField
                                        icon={<KeyIcon />}
                                        label="Password Status"
                                    >
                                        <BadgeChip
                                            label="Temporary Password"
                                            color="warning"
                                        />
                                    </InfoField>

                                    <InfoField
                                        icon={<SecurityIcon />}
                                        label="Two-Factor Authentication"
                                    >
                                        <BadgeChip
                                            label="Disabled"
                                            color="default"
                                        />
                                    </InfoField>

                                    <InfoField
                                        icon={<DevicesIcon />}
                                        label="Active Sessions"
                                    >
                                        <Typography fontWeight={500}>
                                            1 Session
                                        </Typography>
                                    </InfoField>

                                    <InfoField
                                        icon={<AccessTimeIcon />}
                                        label="Last Password Reset"
                                    >
                                        <Typography fontWeight={500}>
                                            Never
                                        </Typography>
                                    </InfoField>
                                </Stack>
                            </CardContent>
                        </Card>
                    </Box>

                    <Box
                        sx={{
                            p: 3,
                            bgcolor: "white",
                            borderTop: "1px solid",
                            borderColor: "divider",
                        }}
                    >
                        {drawerMode ===
                        "details" ? (
                            <Stack
                                direction="row"
                                spacing={2}
                            >
                                <Button
                                    fullWidth
                                    variant="outlined"
                                    onClick={onClose}
                                >
                                    Close
                                </Button>

                                <Button
                                    fullWidth
                                    variant="contained"
                                    onClick={() =>
                                        onDrawerModeChange(
                                            "edit"
                                        )
                                    }
                                >
                                    Edit
                                </Button>
                            </Stack>
                        ) : drawerMode ===
                          "edit" ? (
                            <Stack
                                direction="row"
                                spacing={2}
                            >
                                <Button
                                    fullWidth
                                    variant="outlined"
                                    onClick={() => {
                                        setFormData(
                                            {}
                                        );
                                        onDrawerModeChange(
                                            "details"
                                        );
                                    }}
                                >
                                    Cancel
                                </Button>

                                <Button
                                    fullWidth
                                    variant="contained"
                                    onClick={() => {
                                        console.log(
                                            "Save Administrator",
                                            formData
                                        );

                                        setFormData(
                                            {}
                                        );

                                        onDrawerModeChange(
                                            "details"
                                        );
                                    }}
                                >
                                    Save Changes
                                </Button>
                            </Stack>
                        ) : (
                            <Stack
                                direction="row"
                                spacing={2}
                            >
                                <Button
                                    fullWidth
                                    variant="outlined"
                                    onClick={() => {
                                        setFormData(
                                            {}
                                        );
                                        onClose();
                                    }}
                                >
                                    Cancel
                                </Button>

                                <Button
                                    fullWidth
                                    variant="contained"
                                    onClick={() => {
                                        console.log(
                                            "Create Administrator",
                                            formData
                                        );

                                        setFormData(
                                            {}
                                        );

                                        onClose();
                                    }}
                                >
                                    Create Administrator
                                </Button>
                            </Stack>
                        )}
                    </Box>
                </Box>
            </Drawer>

            <AppSnackbar
                open={snackbarOpen}
                message="Email copied"
                onClose={() =>
                    setSnackbarOpen(false)
                }
            />
        </>
    );
}

export default AdminUserDetailsDrawer;                        