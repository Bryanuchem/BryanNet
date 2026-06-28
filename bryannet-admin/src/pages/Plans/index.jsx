import { useEffect, useState } from "react";

import {
    Alert,
    Box,
    Button,
    Container,
    Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import {
    createPlan,
    deletePlan,
    getPlans,
    updatePlan,
    updatePlanStatus,
} from "../../api/plans";

import PlansTable from "../../components/plans/PlansTable";
import PlanDialog from "../../components/plans/PlanDialog";
import AppSnackbar from "../../components/common/AppSnackbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import SearchBar from "../../components/common/SearchBar";

const PlansPage = () => {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [searchTerm, setSearchTerm] = useState("");

    const [dialogOpen, setDialogOpen] = useState(false);
    const [selectedPlan, setSelectedPlan] = useState(null);

    const [confirmOpen, setConfirmOpen] = useState(false);
    const [confirmAction, setConfirmAction] = useState(null);

    const [planToToggle, setPlanToToggle] = useState(null);
    const [planToDelete, setPlanToDelete] = useState(null);

    const [snackbar, setSnackbar] = useState({
        open: false,
        message: "",
        severity: "success",
    });

    useEffect(() => {
        fetchPlans();
    }, []);

    const fetchPlans = async () => {
        try {
            setLoading(true);
            setError("");

            const data = await getPlans();
            setPlans(data);
        } catch (err) {
            console.error(err);

            setError(
                err.response?.data?.detail ||
                    "Failed to load plans."
            );

            setSnackbar({
                open: true,
                message:
                    err.response?.data?.detail ||
                    "Failed to load plans.",
                severity: "error",
            });
        } finally {
            setLoading(false);
        }
    };

    const handleOpenDialog = () => {
        setSelectedPlan(null);
        setDialogOpen(true);
    };

    const handleEditPlan = (plan) => {
        setSelectedPlan(plan);
        setDialogOpen(true);
    };

    const handleCloseDialog = () => {
        setDialogOpen(false);
        setSelectedPlan(null);
    };

    const handleSubmitPlan = async (formData) => {
        try {
            if (selectedPlan) {
                await updatePlan(
                    selectedPlan.plan_id,
                    formData
                );

                setSnackbar({
                    open: true,
                    message:
                        "Plan updated successfully.",
                    severity: "success",
                });
            } else {
                await createPlan(formData);

                setSnackbar({
                    open: true,
                    message:
                        "Plan created successfully.",
                    severity: "success",
                });
            }

            handleCloseDialog();
            await fetchPlans();
        } catch (err) {
            console.error(err);

            setSnackbar({
                open: true,
                message:
                    err.response?.data?.detail ||
                    "Operation failed.",
                severity: "error",
            });
        }
    };

    const handleToggleStatus = (plan) => {
        setPlanToToggle(plan);
        setPlanToDelete(null);
        setConfirmAction("toggle");
        setConfirmOpen(true);
    };

    const handleDelete = (plan) => {
        setPlanToDelete(plan);
        setPlanToToggle(null);
        setConfirmAction("delete");
        setConfirmOpen(true);
    };

    const handleConfirmToggleStatus = async () => {
        try {
            await updatePlanStatus(
                planToToggle.plan_id,
                !planToToggle.is_active
            );

            setSnackbar({
                open: true,
                message: planToToggle.is_active
                    ? "Plan deactivated successfully."
                    : "Plan activated successfully.",
                severity: "success",
            });

            handleCloseConfirm();

            await fetchPlans();
        } catch (err) {
            console.error(err);

            handleCloseConfirm();

            setSnackbar({
                open: true,
                message:
                    err.response?.data?.detail ||
                    "Failed to update plan status.",
                severity: "error",
            });
        }
    };

    const handleConfirmDelete = async () => {
        try {
            await deletePlan(
                planToDelete.plan_id
            );

            setSnackbar({
                open: true,
                message:
                    "Plan deleted successfully.",
                severity: "success",
            });

            handleCloseConfirm();

            await fetchPlans();
        } catch (err) {
            console.error(err);

            handleCloseConfirm();

            setSnackbar({
                open: true,
                message:
                    err.response?.data?.detail ||
                    "Failed to delete plan.",
                severity: "error",
            });
        }
    };

    const handleCloseConfirm = () => {
        setConfirmOpen(false);
        setConfirmAction(null);
        setPlanToToggle(null);
        setPlanToDelete(null);
    };

    const handleCloseSnackbar = () => {
        setSnackbar((prev) => ({
            ...prev,
            open: false,
        }));
    };

    const filteredPlans = plans.filter((plan) =>
        plan.plan_name
            .toLowerCase()
            .includes(searchTerm.toLowerCase())
    );

    return (
        <Container
            maxWidth={false}
            sx={{ py: 3 }}
        >
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                mb={3}
            >
                <Box>
                    <Typography
                        variant="h4"
                        fontWeight={600}
                    >
                        Plans
                    </Typography>

                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        View and manage all internet plans.
                    </Typography>
                </Box>
                
            <Box sx={{mt:3, mb: 3}}>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={handleOpenDialog}
                >
                    New Plan
                </Button>
            </Box>    
            </Box>

            {error && (
                <Alert
                    severity="error"
                    sx={{ mb: 2 }}
                >
                    {error}
                </Alert>
            )}

            <SearchBar
                value={searchTerm}
                onChange={(event) =>
                    setSearchTerm(event.target.value)
                }
                placeholder="Search plans..."
            />

            <PlansTable
                plans={filteredPlans}
                loading={loading}
                onEdit={handleEditPlan}
                onToggleStatus={handleToggleStatus}
                onDelete={handleDelete}
            />


            <PlanDialog
                open={dialogOpen}
                onClose={handleCloseDialog}
                onSubmit={handleSubmitPlan}
                plan={selectedPlan}
            />

            <ConfirmDialog
                open={confirmOpen}
                title={
                    confirmAction === "delete"
                        ? "Delete Plan"
                        : planToToggle?.is_active
                            ? "Deactivate Plan"
                            : "Activate Plan"
                }
                message={
                    confirmAction === "delete"
                        ? `Are you sure you want to delete "${planToDelete?.plan_name}"?`
                        : `Are you sure you want to ${
                              planToToggle?.is_active
                                  ? "deactivate"
                                  : "activate"
                          } "${planToToggle?.plan_name}"?`
                }
                confirmText={
                    confirmAction === "delete"
                        ? "Delete"
                        : planToToggle?.is_active
                            ? "Deactivate"
                            : "Activate"
                }
                confirmColor={
                    confirmAction === "delete"
                        ? "error"
                        : planToToggle?.is_active
                            ? "warning"
                            : "success"
                }
                onConfirm={
                    confirmAction === "delete"
                        ? handleConfirmDelete
                        : handleConfirmToggleStatus
                }
                onClose={handleCloseConfirm}
            />

            <AppSnackbar
                open={snackbar.open}
                onClose={handleCloseSnackbar}
                message={snackbar.message}
                severity={snackbar.severity}
            />
        </Container>
    );
};

export default PlansPage;