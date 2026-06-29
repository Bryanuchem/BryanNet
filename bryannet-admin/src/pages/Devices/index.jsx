import { useMemo, useState } from "react";

import {
    Alert,
    Box,
    CircularProgress,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import AppSnackbar from "../../components/common/AppSnackbar";

import DeviceTable from "../../components/devices/DeviceTable";
import DeviceDialog from "../../components/devices/DeviceDialog";
import DeviceDetailsDialog from "../../components/devices/DeviceDetailsDialog";

import {
    useDevices,
    useRegisterDevice,
    useRemoveDevice,
} from "../../hooks/useDevices";

import { useCustomers } from "../../hooks/useCustomers";

function Devices() {

    const {
        data: devices = [],
        isLoading,
        isError,
    } = useDevices();

    const {
        data: customers = [],
    } = useCustomers();

    const registerDeviceMutation =
        useRegisterDevice();

    const removeDeviceMutation =
        useRemoveDevice();

    const [registerDialogOpen, setRegisterDialogOpen] =
        useState(false);

    const [detailsDialogOpen, setDetailsDialogOpen] =
        useState(false);

    const [confirmDialogOpen, setConfirmDialogOpen] =
        useState(false);

    const [selectedDevice, setSelectedDevice] =
        useState(null);

    const [snackbar, setSnackbar] =
        useState({
            open: false,
            severity: "success",
            message: "",
        });

    const sortedCustomers = useMemo(() => {

        return [...customers].sort((a, b) => {

            const nameA =
                a.full_name ??
                `${a.first_name ?? ""} ${a.last_name ?? ""}`.trim();

            const nameB =
                b.full_name ??
                `${b.first_name ?? ""} ${b.last_name ?? ""}`.trim();

            return nameA.localeCompare(nameB);

        });

    }, [customers]);

    const handleOpenRegisterDialog = () => {
        setRegisterDialogOpen(true);
    };

    const handleCloseRegisterDialog = () => {
        setRegisterDialogOpen(false);
    };

    const handleOpenDetailsDialog = (
        device
    ) => {

        setSelectedDevice(device);

        setDetailsDialogOpen(true);
    };

    const handleCloseDetailsDialog = () => {

        setSelectedDevice(null);

        setDetailsDialogOpen(false);
    };

    const handleOpenRemoveDialog = (
        device
    ) => {

        setSelectedDevice(device);

        setConfirmDialogOpen(true);
    };

    const handleCloseRemoveDialog = () => {

        setSelectedDevice(null);

        setConfirmDialogOpen(false);
    };

    const handleCloseSnackbar = () => {

        setSnackbar((prev) => ({
            ...prev,
            open: false,
        }));
    };

    const handleRegisterDevice = async (
        formData
    ) => {

        try {

            await registerDeviceMutation.mutateAsync(
                formData
            );

            setSnackbar({
                open: true,
                severity: "success",
                message:
                    "Device registered successfully.",
            });

            handleCloseRegisterDialog();

        } catch (error) {

            setSnackbar({
                open: true,
                severity: "error",
                message:
                    error?.response?.data?.detail ??
                    "Failed to register device.",
            });

        }

    };

    const handleRemoveDevice = async () => {

        if (!selectedDevice) {
            return;
        }

        try {

            await removeDeviceMutation.mutateAsync(
                selectedDevice.device_id
            );

            setSnackbar({
                open: true,
                severity: "success",
                message:
                    "Device removed successfully.",
            });

            handleCloseRemoveDialog();

        } catch (error) {

            setSnackbar({
                open: true,
                severity: "error",
                message:
                    error?.response?.data?.detail ??
                    "Failed to remove device.",
            });

        }

    };

    if (isLoading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                py={8}
            >
                <CircularProgress />
            </Box>
        );
    }

    if (isError) {
        return (
            <Alert severity="error">
                Failed to load devices.
            </Alert>
        );
    }

    // Part 2 starts with the return statement.
    return (
        <>
            <PageHeader
                title="Devices"
                subtitle="Manage registered customer devices."
                actionLabel="Register Device"
                actionIcon={<AddIcon />}
                onAction={handleOpenRegisterDialog}
            />

            <DeviceTable
                devices={devices}
                onView={handleOpenDetailsDialog}
                onDelete={handleOpenRemoveDialog}
            />

            <DeviceDialog
                open={registerDialogOpen}
                customers={sortedCustomers}
                onClose={handleCloseRegisterDialog}
                onSubmit={handleRegisterDevice}
            />

            <DeviceDetailsDialog
                open={detailsDialogOpen}
                device={selectedDevice}
                onClose={handleCloseDetailsDialog}
            />

            <ConfirmDialog
                open={confirmDialogOpen}
                title="Remove Device"
                message={
                    selectedDevice
                        ? `Are you sure you want to remove "${selectedDevice.device_name}"?`
                        : ""
                }
                confirmText="Remove"
                confirmColor="error"
                onConfirm={handleRemoveDevice}
                onClose={handleCloseRemoveDialog}
            />

            <AppSnackbar
                open={snackbar.open}
                severity={snackbar.severity}
                message={snackbar.message}
                onClose={handleCloseSnackbar}
            />
        </>
    );

}

export default Devices;