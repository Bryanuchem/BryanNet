import { useMemo, useState } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import SearchBar from "../../components/common/SearchBar";
import AppSnackbar from "../../components/common/AppSnackbar";
import FilterToolbar from "../../components/common/FilterToolbar";
import ExportCsvButton from "../../components/common/ExportCsvButton";

import DeviceFilters from "../../components/devices/DeviceFilters";
import DeviceTable from "../../components/devices/DeviceTable";
import DeviceDialog from "../../components/devices/DeviceDialog";
import DeviceDetailsDrawer from "../../components/devices/DeviceDetailsDrawer";
import RenameDeviceDialog from "../../components/devices/RenameDeviceDialog";
import ReplaceDeviceDialog from "../../components/devices/ReplaceDeviceDialog";

import { useDevices } from "../../hooks/useDevices";

import { useRegisterDevice } from "../../hooks/useRegisterDevice";
import { useActivateDevice } from "../../hooks/useActivateDevice";
import { useDeactivateDevice } from "../../hooks/useDeactivateDevice";
import { useApproveDevice } from "../../hooks/useApproveDevice";
import { useBlockDevice } from "../../hooks/useBlockDevice";
import { useUnblockDevice } from "../../hooks/useUnblockDevice";
import { useRenameDevice } from "../../hooks/useRenameDevice";
import { useReplaceDevice } from "../../hooks/useReplaceDevice";

import { useCustomers } from "../../hooks/useCustomers";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function Devices() {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const {
        data: devices = [],
        isLoading,
        isError,
        refetch,
    } = useDevices();

    const {
        data: customers = [],
    } = useCustomers();

    const registerDevice =
        useRegisterDevice();

    const activateDevice =
        useActivateDevice();

    const deactivateDevice =
        useDeactivateDevice();

    const approveDevice =
        useApproveDevice();

    const blockDevice =
        useBlockDevice();

    const unblockDevice =
        useUnblockDevice();

    const renameDevice =
        useRenameDevice();

    const replaceDevice =
        useReplaceDevice();

    const [
        searchTerm,
        setSearchTerm,
    ] = useState("");

    const [
        statusFilter,
        setStatusFilter,
    ] = useState("all");

    const [
        approvalFilter,
        setApprovalFilter,
    ] = useState("all");

    const [page, setPage] =
        useState(0);

    const [
        rowsPerPage,
        setRowsPerPage,
    ] = useState(10);

    const [
        selectedDevice,
        setSelectedDevice,
    ] = useState(null);

    const [
        registerDialogOpen,
        setRegisterDialogOpen,
    ] = useState(false);

    const [
        detailsDialogOpen,
        setDetailsDialogOpen,
    ] = useState(false);

    const [
        renameDialogOpen,
        setRenameDialogOpen,
    ] = useState(false);

    const [
        replaceDialogOpen,
        setReplaceDialogOpen,
    ] = useState(false);

    const [
        snackbar,
        setSnackbar,
    ] = useState({

        open: false,

        severity: "success",

        message: "",

    });

    const sortedCustomers =
        useMemo(() => {

            return [...customers].sort(
                (a, b) =>
                    (a.full_name ?? "")
                        .localeCompare(
                            b.full_name ?? "",
                        ),
            );

        }, [customers]);

    const filteredDevices =
        useMemo(() => {

            const query =
                searchTerm
                    .trim()
                    .toLowerCase();

            return devices.filter(
                (device) => {

                    const matchesSearch =

                        !query ||

                        device.customer_name
                            ?.toLowerCase()
                            .includes(query) ||

                        device.device_name
                            ?.toLowerCase()
                            .includes(query) ||

                        device.mac_address
                            ?.toLowerCase()
                            .includes(query);

                    const matchesStatus =

                        statusFilter === "all" ||

                        device.device_status ===
                        statusFilter;

                    const matchesApproval =

                        approvalFilter ===
                            "all" ||

                        (approvalFilter ===
                            "approved" &&
                            device.approved_by_customer) ||

                        (approvalFilter ===
                            "pending" &&
                            !device.approved_by_customer);

                    return (

                        matchesSearch &&

                        matchesStatus &&

                        matchesApproval

                    );

                },
            );

        }, [

            devices,

            searchTerm,

            statusFilter,

            approvalFilter,

        ]);

    const handleClearFilters =
        () => {

            setSearchTerm("");

            setStatusFilter("all");

            setApprovalFilter("all");

            setPage(0);

        };

    const handleOpenRegisterDialog =
        () => {

            if (

                !hasPermission(

                    "devices.create",

                )

            ) {

                return;

            }

            setRegisterDialogOpen(
                true,
            );

        };

    const handleCloseRegisterDialog =
        () => {

            setRegisterDialogOpen(
                false,
            );

        };

    const handleOpenDetailsDialog =
        (device) => {

            if (

                !hasPermission(

                    "devices.view",

                )

            ) {

                return;

            }

            setSelectedDevice(
                device,
            );

            setDetailsDialogOpen(
                true,
            );

        };

    const handleCloseDetailsDialog =
        () => {

            setSelectedDevice(
                null,
            );

            setDetailsDialogOpen(
                false,
            );

        };

    const handleOpenRenameDialog =
        (device) => {

            if (

                !hasPermission(

                    "devices.rename",

                )

            ) {

                return;

            }

            setSelectedDevice(
                device,
            );

            setRenameDialogOpen(
                true,
            );

        };

    const handleCloseRenameDialog =
        () => {

            setRenameDialogOpen(
                false,
            );

            setSelectedDevice(
                null,
            );

        };

    const handleOpenReplaceDialog =
        (device) => {

            if (

                !hasPermission(

                    "devices.replace",

                )

            ) {

                return;

            }

            setSelectedDevice(
                device,
            );

            setReplaceDialogOpen(
                true,
            );

        };

    const handleCloseReplaceDialog =
        () => {

            setReplaceDialogOpen(
                false,
            );

            setSelectedDevice(
                null,
            );

        };

    const showSuccess = (
        message,
    ) => {

        setSnackbar({

            open: true,

            severity: "success",

            message,

        });

    };

    const showError = (
        error,
        fallback,
    ) => {

        setSnackbar({

            open: true,

            severity: "error",

            message:
                error.response?.data
                    ?.detail ??
                fallback,

        });

    };

    const handleCloseSnackbar =
        () => {

            setSnackbar(
                (previous) => ({

                    ...previous,

                    open: false,

                }),
            );

        };

    const handleRegisterDevice =
        async (formData) => {

            if (

                !hasPermission(

                    "devices.create",

                )

            ) {

                return;

            }

            try {

                await registerDevice.mutateAsync(
                    formData,
                );

                showSuccess(
                    "Device registered successfully.",
                );

                handleCloseRegisterDialog();

            } catch (error) {

                showError(
                    error,
                    "Failed to register device.",
                );

            }

        };

    const handleToggleStatus =
        async (device) => {

            const canToggle =

                device.device_status === "active"

                    ? hasPermission(

                        "devices.deactivate",

                    )

                    : hasPermission(

                        "devices.activate",

                    );

            if (

                !canToggle

            ) {

                return;

            }

            try {

                if (

                    device.device_status === "active"

                ) {

                    await deactivateDevice.mutateAsync(

                        device.device_id,

                    );

                    showSuccess(

                        "Device deactivated successfully.",

                    );

                } else {

                    await activateDevice.mutateAsync(

                        device.device_id,

                    );

                    showSuccess(

                        "Device activated successfully.",

                    );

                }

            } catch (error) {

                showError(

                    error,

                    "Operation failed.",

                );

            }

        };

    const handleApproveDevice =
        async (device) => {

            if (

                !hasPermission(

                    "devices.approve",

                )

            ) {

                return;

            }

            try {

                await approveDevice.mutateAsync(

                    device.device_id,

                );

                showSuccess(

                    "Device approved successfully.",

                );

            } catch (error) {

                showError(

                    error,

                    "Failed to approve device.",

                );

            }

        };

    const handleBlockDevice =
        async (device) => {

            if (

                !hasPermission(

                    "devices.block",

                )

            ) {

                return;

            }

            try {

                await blockDevice.mutateAsync(

                    device.device_id,

                );

                showSuccess(

                    "Device blocked successfully.",

                );

            } catch (error) {

                showError(

                    error,

                    "Failed to block device.",

                );

            }

        };

    const handleUnblockDevice =
        async (device) => {

            if (

                !hasPermission(

                    "devices.unblock",

                )

            ) {

                return;

            }

            try {

                await unblockDevice.mutateAsync(

                    device.device_id,

                );

                showSuccess(

                    "Device unblocked successfully.",

                );

            } catch (error) {

                showError(

                    error,

                    "Failed to unblock device.",

                );

            }

        };

    const handleRenameDevice =
        async ({
            deviceId,
            deviceName,
        }) => {

            if (

                !hasPermission(

                    "devices.rename",

                )

            ) {

                return;

            }

            try {

                await renameDevice.mutateAsync({

                    deviceId,

                    deviceName,

                });

                showSuccess(

                    "Device renamed successfully.",

                );

                handleCloseRenameDialog();

            } catch (error) {

                showError(

                    error,

                    "Failed to rename device.",

                );

            }

        };

    const handleReplaceDevice =
        async (request) => {

            if (

                !hasPermission(

                    "devices.replace",

                )

            ) {

                return;

            }

            try {

                await replaceDevice.mutateAsync(

                    request,

                );

                showSuccess(

                    "Device replaced successfully.",

                );

                handleCloseReplaceDialog();

            } catch (error) {

                showError(

                    error,

                    "Failed to replace device.",

                );

            }

        };

    const handleChangePage = (
        event,
        newPage,
    ) => {

        setPage(
            newPage,
        );

    };

    const handleChangeRowsPerPage =
        (event) => {

            setRowsPerPage(

                parseInt(
                    event.target.value,
                    10,
                ),

            );

            setPage(0);

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

    return (

        <>

            <PageHeader
                title="Devices"
                subtitle="Manage registered customer devices."
            />

            {hasPermission(

                "devices.create",

            ) && (

                <Button

                    variant="contained"

                    startIcon={<AddIcon />}

                    onClick={

                        handleOpenRegisterDialog

                    }

                    sx={{

                        mb: 3,

                    }}

                >

                    Register Device

                </Button>

            )}

            <FilterToolbar>

                <SearchBar
                    value={searchTerm}
                    onChange={(event) => {

                        setSearchTerm(
                            event.target.value,
                        );

                        setPage(0);

                    }}
                    placeholder="Search customer, device or MAC address..."
                    sx={{
                        flex: 1,
                    }}
                />

                <DeviceFilters

                    status={statusFilter}

                    approval={approvalFilter}

                    onStatusChange={(
                        event,
                    ) => {

                        setStatusFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onApprovalChange={(
                        event,
                    ) => {

                        setApprovalFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onRefresh={refetch}

                    onClear={
                        handleClearFilters
                    }

                />

                <ExportCsvButton

                    filename="devices"

                    rows={filteredDevices}

                    columns={[

                        {

                            key: "customer_name",

                            label: "Customer",

                        },

                        {

                            key: "device_name",

                            label: "Device",

                        },

                        {

                            key: "mac_address",

                            label: "MAC Address",

                        },

                        {

                            key: "device_status",

                            label: "Status",

                        },

                        {

                            key: "approved_by_customer",

                            label: "Approved",

                            formatter: (
                                value,
                            ) =>
                                value
                                    ? "Yes"
                                    : "No",

                        },

                    ]}

                />

            </FilterToolbar>

            <DeviceTable

                devices={filteredDevices}

                loading={false}

                searchTerm={searchTerm}

                page={page}

                rowsPerPage={
                    rowsPerPage
                }

                onPageChange={
                    handleChangePage
                }

                onRowsPerPageChange={
                    handleChangeRowsPerPage
                }

                onRowClick={
                    handleOpenDetailsDialog
                }

                onToggleStatus={
                    handleToggleStatus
                }

                onApprove={
                    handleApproveDevice
                }

                onBlock={
                    handleBlockDevice
                }

                onUnblock={
                    handleUnblockDevice
                }

                onRename={
                    handleOpenRenameDialog
                }

                onReplace={
                    handleOpenReplaceDialog
                }

            />        

            {hasPermission(

                "devices.create",

            ) && (

                <DeviceDialog

                    open={registerDialogOpen}

                    customers={sortedCustomers}

                    onClose={handleCloseRegisterDialog}

                    onSubmit={handleRegisterDevice}

                />

            )}

            {hasPermission(

                "devices.view",

            ) && (

                <DeviceDetailsDrawer

                    open={detailsDialogOpen}

                    device={selectedDevice}

                    onClose={handleCloseDetailsDialog}

                />

            )}

            {hasPermission(

                "devices.rename",

            ) && (

                <RenameDeviceDialog

                    open={renameDialogOpen}

                    device={selectedDevice}

                    onClose={handleCloseRenameDialog}

                    onSubmit={handleRenameDevice}

                />

            )}

            {hasPermission(

                "devices.replace",

            ) && (

                <ReplaceDeviceDialog

                    open={replaceDialogOpen}

                    device={selectedDevice}

                    devices={devices.filter(

                        (candidate) =>

                            selectedDevice &&

                            candidate.customer_id ===

                                selectedDevice.customer_id,

                    )}

                    onClose={handleCloseReplaceDialog}

                    onSubmit={handleReplaceDevice}

                />

            )}

            <AppSnackbar
                open={snackbar.open}
                severity={
                    snackbar.severity
                }
                message={
                    snackbar.message
                }
                onClose={
                    handleCloseSnackbar
                }
            />

        </>

    );

}

export default Devices;            