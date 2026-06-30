import {
    Box,
    CircularProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";

import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";
import ToggleOnOutlinedIcon from "@mui/icons-material/ToggleOnOutlined";
import ToggleOffOutlinedIcon from "@mui/icons-material/ToggleOffOutlined";

import BadgeChip from "../common/BadgeChip";
import EmptyState from "../common/EmptyState";
import ActionMenu from "../common/ActionMenu";

function PlansTable({

    plans = [],

    loading = false,

    onEdit,

    onToggleStatus,

    onDelete,

}) {

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

                    sx={{

                        mt: 1,

                    }}

                >

                    There are currently no internet plans available.

                </Typography>

            </Paper>

        );

    }

    return (

        <TableContainer

            component={Paper}

            elevation={0}

        >

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

                                ₦{Number(

                                    plan.price,

                                ).toLocaleString()}

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

                                    status={

                                        plan.is_active

                                            ? "active"

                                            : "inactive"

                                    }

                                />

                            </TableCell>

                            <TableCell align="right">

                                <ActionMenu

                                    row={plan}

                                    items={[

                                        {

                                            label: "Edit",

                                            icon: (

                                                <EditOutlinedIcon

                                                    fontSize="small"

                                                />

                                            ),

                                            onClick: onEdit,

                                        },

                                        {

                                            label: plan.is_active

                                                ? "Deactivate"

                                                : "Activate",

                                            icon: plan.is_active ? (

                                                <ToggleOffOutlinedIcon

                                                    fontSize="small"

                                                />

                                            ) : (

                                                <ToggleOnOutlinedIcon

                                                    fontSize="small"

                                                />

                                            ),

                                            onClick: onToggleStatus,

                                        },

                                        {

                                            divider: true,

                                            label: "Delete",

                                            color: "error.main",

                                            icon: (

                                                <DeleteOutlineOutlinedIcon

                                                    fontSize="small"

                                                />

                                            ),

                                            onClick: onDelete,

                                        },

                                    ]}

                                />

                            </TableCell>

                        </TableRow>

                    ))}

                </TableBody>

            </Table>

        </TableContainer>

    );

}

export default PlansTable;                                