import { useState } from "react";

import {
    Box,
    CircularProgress,
    IconButton,
    Menu,
    MenuItem,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Tooltip,
    Typography,
} from "@mui/material";

import MoreVertIcon from "@mui/icons-material/MoreVert";

import BadgeChip from "../common/BadgeChip";

const PlansTable = ({
    plans = [],
    loading = false,
    onEdit,
    onToggleStatus,
    onDelete,
}) => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [selectedPlan, setSelectedPlan] = useState(null);

    const menuOpen = Boolean(anchorEl);

    const handleMenuOpen = (event, plan) => {
        setAnchorEl(event.currentTarget);
        setSelectedPlan(plan);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
        setSelectedPlan(null);
    };

    const handleEdit = () => {
        if (selectedPlan && onEdit) {
            onEdit(selectedPlan);
        }

        handleMenuClose();
    };

    if (loading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                py={6}
            >
                <CircularProgress />
            </Box>
        );
    }

    if (plans.length === 0) {
        return (
            <Paper
                sx={{
                    p: 4,
                    textAlign: "center",
                }}
            >
                <Typography variant="h6">
                    No Plans Found
                </Typography>

                <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 1 }}
                >
                    There are currently no internet plans available.
                </Typography>
            </Paper>
        );
    }

    return (
        <>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>
                                <strong>Name</strong>
                            </TableCell>

                            <TableCell>
                                <strong>Speed</strong>
                            </TableCell>

                            <TableCell>
                                <strong>Price</strong>
                            </TableCell>

                            <TableCell>
                                <strong>Duration</strong>
                            </TableCell>

                            <TableCell align="center">
                                <strong>Max Devices</strong>
                            </TableCell>

                            <TableCell align="center">
                                <strong>Concurrent</strong>
                            </TableCell>

                            <TableCell align="center">
                                <strong>Status</strong>
                            </TableCell>

                            <TableCell align="right">
                                <strong>Actions</strong>
                            </TableCell>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {plans.map((plan) => (
                            <TableRow
                                key={plan.plan_id}
                                hover
                            >
                                <TableCell>
                                    {plan.plan_name}
                                </TableCell>

                                <TableCell>
                                    {plan.speed_limit_mbps} Mbps
                                </TableCell>

                                <TableCell>
                                    ₦{Number(plan.price).toLocaleString()}
                                </TableCell>

                                <TableCell>
                                    {plan.duration_days} Days
                                </TableCell>

                                <TableCell align="center">
                                    {plan.max_devices}
                                </TableCell>

                                <TableCell align="center">
                                    {plan.concurrent_devices}
                                </TableCell>

                                <TableCell align="center">
                                    <BadgeChip
                                        variant="status"
                                        value={
                                            plan.is_active
                                                ? "ACTIVE"
                                                : "INACTIVE"
                                        }
                                    />
                                </TableCell>

                                <TableCell align="right">
                                    <Tooltip title="Actions">
                                        <IconButton
                                            onClick={(event) =>
                                                handleMenuOpen(event, plan)
                                            }
                                        >
                                            <MoreVertIcon />
                                        </IconButton>
                                    </Tooltip>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

                <Menu
                    anchorEl={anchorEl}
                    open={menuOpen}
                    onClose={handleMenuClose}
                >
                    <MenuItem onClick={handleEdit}>
                        Edit
                    </MenuItem>

                    <MenuItem
                        onClick={() => {
                            if (selectedPlan && onToggleStatus) {
                                onToggleStatus(selectedPlan);
                            }

                            handleMenuClose();
                        }}
                    >
                        {selectedPlan?.is_active
                            ? "Deactivate"
                            : "Activate"}
                    </MenuItem>

                    <MenuItem
                        onClick={() => {
                            if (selectedPlan && onDelete) {
                                onDelete(selectedPlan);
                            }

                            handleMenuClose();
                        }}
                    >
                        Delete
                    </MenuItem>
                </Menu>        </>
    );
};

export default PlansTable;