import {
    useState,
} from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

import AddIcon from "@mui/icons-material/Add";

import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";

import FilterToolbar from "../../components/common/FilterToolbar";

import SearchBar from "../../components/common/SearchBar";
import ExportCsvButton from "../../components/common/ExportCsvButton";

import PlanFilters from "../../components/plans/PlanFilters";
import PlanTable from "../../components/plans/PlanTable";
import PlanDialog from "../../components/plans/PlanDialog";
import PlanDetailsDrawer from "../../components/plans/PlanDetailsDrawer";

import {
    usePlans,
} from "../../hooks/usePlans";

import {
    useCreatePlan,
} from "../../hooks/useCreatePlan";

import {
    useUpdatePlan,
} from "../../hooks/useUpdatePlan";

import {
    useActivatePlan,
} from "../../hooks/useActivatePlan";

import {
    useDeactivatePlan,
} from "../../hooks/useDeactivatePlan";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";



function Plans() {

    const [
        page,
        setPage,
    ] = useState(0);

    const [
        rowsPerPage,
        setRowsPerPage,
    ] = useState(10);

    const [
        searchTerm,
        setSearchTerm,
    ] = useState("");

    const [
        activeFilter,
        setActiveFilter,
    ] = useState("all");

    const {
        data,
        isLoading,
        error,
        refetch,
    } = usePlans({

        page: page + 1,

        pageSize: rowsPerPage,

        search: searchTerm,

        isActive:

            activeFilter === "all"

                ? undefined

                : activeFilter === "active",

    });

    const plans =
        data?.items ?? [];

    const total =
        data?.total ?? 0;

    const createPlan =
        useCreatePlan();

    const updatePlan =
        useUpdatePlan();

    const activatePlan =
        useActivatePlan();

    const deactivatePlan =
        useDeactivatePlan();

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [

        selectedPlan,

        setSelectedPlan,

    ] = useState(null);

    const [
        dialogOpen,
        setDialogOpen,
    ] = useState(false);

    const [
        drawerOpen,
        setDrawerOpen,
    ] = useState(false);

    const [
        snackbar,
        setSnackbar,
    ] = useState({

        open: false,

        message: "",

        severity: "success",

    });

    const filteredPlans = plans;

    const handleChangePage = (
        event,
        newPage,
    ) => {

        setPage(newPage);

    };

    const handleChangeRowsPerPage = (
        event,
    ) => {

        setRowsPerPage(

            parseInt(
                event.target.value,
                10,
            ),

        );

        setPage(0);

    };

    const handleOpenDialog = () => {

        if (

            !hasPermission(

                "plans.create",

            )

        ) {

            return;

        }

        setSelectedPlan(

            null,

        );

        setDialogOpen(

            true,

        );

    };

    const handleEditPlan = (

        plan,

    ) => {

        if (

            !hasPermission(

                "plans.edit",

            )

        ) {

            return;

        }

        setSelectedPlan(

            plan,

        );

        setDialogOpen(

            true,

        );

    };

    const handleCloseDialog = () => {

        setDialogOpen(false);

        setSelectedPlan(null);

    };

    const handleOpenDrawer = (

        plan,

    ) => {

        if (

            !hasPermission(

                "plans.view",

            )

        ) {

            return;

        }

        setSelectedPlan(

            plan,

        );

        setDrawerOpen(

            true,

        );

    };

    const handleCloseDrawer = () => {

        setDrawerOpen(false);

        setSelectedPlan(null);

    };

    const handleSubmitPlan =
        async (formData) => {

            try {

                if (

                    selectedPlan

                ) {

                    if (

                        !hasPermission(

                            "plans.edit",

                        )

                    ) {

                        return;

                    }

                    await updatePlan.mutateAsync({

                        planId:

                            selectedPlan.plan_id,

                        planData:

                            formData,

                    });

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:

                            "Plan updated successfully.",

                    });

                } else {

                    if (

                        !hasPermission(

                            "plans.create",

                        )

                    ) {

                        return;

                    }

                    await createPlan.mutateAsync(

                        formData,

                    );

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:

                            "Plan created successfully.",

                    });

                }

                handleCloseDialog();

            } catch (err) {

                console.error(err);

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        err.response?.data?.detail ??

                        "Operation failed.",

                });

            }

        };

    const handleToggleStatus =
        async (plan) => {

            try {

                if (

                    plan.is_active

                ) {

                    if (

                        !hasPermission(

                            "plans.deactivate",

                        )

                    ) {

                        return;

                    }

                    await deactivatePlan.mutateAsync(

                        plan.plan_id,

                    );

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:

                            "Plan deactivated successfully.",

                    });

                } else {

                    if (

                        !hasPermission(

                            "plans.activate",

                        )

                    ) {

                        return;

                    }

                    await activatePlan.mutateAsync(

                        plan.plan_id,

                    );

                    setSnackbar({

                        open: true,

                        severity: "success",

                        message:

                            "Plan activated successfully.",

                    });

                }

            } catch (err) {

                console.error(err);

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        err.response?.data?.detail ??

                        "Operation failed.",

                });

            }

        };

    const handleClearFilters =
        () => {

            setSearchTerm("");

            setActiveFilter(
                "all",
            );

            setPage(0);

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

    if (error) {

        return (

            <>

                <PageHeader
                    title="Plans"
                    subtitle="Manage subscription plans."
                />

                <p>
                    Failed to load plans.
                </p>

            </>

        );

    }

    return (

        <>

            <PageHeader
                title="Plans"
                subtitle="Manage subscription plans."
            />

            {hasPermission(

                "plans.create",

            ) && (

                <Box

                    sx={{

                        mt: 3,

                        mb: 2,

                    }}

                >

                    <Button

                        variant="contained"

                        startIcon={<AddIcon />}

                        onClick={

                            handleOpenDialog

                        }

                    >

                        New Plan

                    </Button>

                </Box>

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
                    placeholder="Search by plan name..."
                    sx={{
                        flex: 1,
                    }}
                />

                <PlanFilters

                    active={
                        activeFilter
                    }

                    onActiveChange={(
                        event,
                    ) => {

                        setActiveFilter(
                            event.target.value,
                        );

                        setPage(0);

                    }}

                    onRefresh={
                        refetch
                    }

                    onClear={
                        handleClearFilters
                    }

                />

                <ExportCsvButton

                    filename="plans"

                    rows={
                        filteredPlans
                    }

                    columns={[

                        {
                            key: "plan_name",
                            label: "Plan",
                        },

                        {
                            key: "price",
                            label: "Price",
                        },

                        {
                            key: "duration_days",
                            label: "Duration (Days)",
                        },

                        {
                            key: "speed_limit_mbps",
                            label: "Speed (Mbps)",
                        },

                        {
                            key: "max_devices",
                            label: "Max Devices",
                        },

                        {
                            key: "concurrent_devices",
                            label: "Concurrent Devices",
                        },

                        {
                            key: "is_active",
                            label: "Status",

                            formatter: (
                                value,
                            ) =>
                                value
                                    ? "Active"
                                    : "Inactive",

                        },

                    ]}

                />

            </FilterToolbar>

            <PlanTable
                plans={filteredPlans}
                loading={isLoading}
                page={page}
                rowsPerPage={rowsPerPage}
                total={total}
                onPageChange={
                    handleChangePage
                }
                onRowsPerPageChange={
                    handleChangeRowsPerPage
                }
                onRowClick={
                    handleOpenDrawer
                }
                onEdit={
                    handleEditPlan
                }
                onToggleStatus={
                    handleToggleStatus
                }
            />

            <PlanDialog
                open={dialogOpen}
                onClose={
                    handleCloseDialog
                }
                onSubmit={
                    handleSubmitPlan
                }
                plan={selectedPlan}
            />

            {hasPermission(

                "plans.view",

            ) && (

                <PlanDetailsDrawer

                    open={

                        drawerOpen

                    }

                    plan={

                        selectedPlan

                    }

                    onClose={

                        handleCloseDrawer

                    }

                />

            )}

            <AppSnackbar
                open={snackbar.open}
                onClose={
                    handleCloseSnackbar
                }
                message={
                    snackbar.message
                }
                severity={
                    snackbar.severity
                }
            />

        </>

    );

}

export default Plans;                    