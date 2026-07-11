import {
    useState,
} from "react";

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
    TablePagination,
    TableRow,
    Typography,
} from "@mui/material";

import MoreVertIcon from "@mui/icons-material/MoreVert";
import EditIcon from "@mui/icons-material/Edit";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import BlockIcon from "@mui/icons-material/Block";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";

import BadgeChip from "../common/BadgeChip";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";

function PlanTable({

    plans,

    loading,

    page,

    rowsPerPage,

    total,

    onPageChange,

    onRowsPerPageChange,

    onRowClick,

    onEdit,

    onToggleStatus,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [

        anchorEl,

        setAnchorEl,

    ] = useState(null);

    const [
        selectedPlan,
        setSelectedPlan,
    ] = useState(null);

    const menuOpen =
        Boolean(anchorEl);

    const handleOpenMenu = (

        event,

        plan,

    ) => {

        const canOpen =

            hasPermission(

                "plans.view",

            ) ||

            hasPermission(

                "plans.edit",

            ) ||

            hasPermission(

                plan.is_active

                    ? "plans.deactivate"

                    : "plans.activate",

            );

        if (

            !canOpen

        ) {

            return;

        }

        event.stopPropagation();

        setAnchorEl(

            event.currentTarget,

        );

        setSelectedPlan(

            plan,

        );

    };

    const handleCloseMenu = () => {

        setAnchorEl(null);

        setSelectedPlan(null);

    };

    if (loading) {

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

    if (!plans.length) {

        return (

            <Paper
                sx={{
                    p: 6,
                    textAlign: "center",
                }}
            >

                <Typography
                    color="text.secondary"
                >
                    No plans found.
                </Typography>

            </Paper>

        );

    }

    return (

        <Paper>

            <TableContainer>

                <Table>

                    <TableHead>

                        <TableRow>

                            <TableCell>
                                Plan
                            </TableCell>

                            <TableCell>
                                Price
                            </TableCell>

                            <TableCell>
                                Duration
                            </TableCell>

                            <TableCell>
                                Speed
                            </TableCell>

                            <TableCell>
                                Max Devices
                            </TableCell>

                            <TableCell>
                                Concurrent
                            </TableCell>

                            <TableCell>
                                Status
                            </TableCell>

                            <TableCell
                                align="right"
                            >
                                Actions
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {plans.map(
                            (
                                plan,
                            ) => (

                            <TableRow

                                hover

                                key={

                                    plan.plan_id

                                }

                                onClick={() => {

                                    if (

                                        hasPermission(

                                            "plans.view",

                                        )

                                    ) {

                                        onRowClick?.(

                                            plan,

                                        );

                                    }

                                }}

                                sx={{

                                    cursor:

                                        hasPermission(

                                            "plans.view",

                                        )

                                            ? "pointer"

                                            : "default",

                                    "&:nth-of-type(odd)": {

                                        bgcolor:

                                            "grey.50",

                                    },

                                }}

                            >

                                    <TableCell>

                                        <Typography
                                            fontWeight={
                                                600
                                            }
                                        >
                                            {
                                                plan.plan_name
                                            }
                                        </Typography>

                                    </TableCell>

                                    <TableCell>

                                        ₦
                                        {Number(
                                            plan.price,
                                        ).toLocaleString()}

                                    </TableCell>

                                    <TableCell>

                                        {
                                            plan.duration_days
                                        }{" "}
                                        days

                                    </TableCell>

                                    <TableCell>

                                        {
                                            plan.speed_limit_mbps
                                        }{" "}
                                        Mbps

                                    </TableCell>

                                    <TableCell>

                                        {
                                            plan.max_devices
                                        }

                                    </TableCell>

                                    <TableCell>

                                        {
                                            plan.concurrent_devices
                                        }

                                    </TableCell>

                                    <TableCell>

                                        <BadgeChip
                                            label={
                                                plan.is_active
                                                    ? "Active"
                                                    : "Inactive"
                                            }
                                            status={
                                                plan.is_active
                                                    ? "active"
                                                    : "inactive"
                                            }
                                        />

                                    </TableCell>

                                    <TableCell

                                        align="right"

                                        onClick={(event) =>

                                            event.stopPropagation()

                                        }

                                    >

                                        {(

                                            hasPermission(

                                                "plans.view",

                                            ) ||

                                            hasPermission(

                                                "plans.edit",

                                            ) ||

                                            hasPermission(

                                                plan.is_active

                                                    ? "plans.deactivate"

                                                    : "plans.activate",

                                            )

                                        ) && (

                                            <IconButton

                                                onClick={(event) =>

                                                    handleOpenMenu(

                                                        event,

                                                        plan,

                                                    )

                                                }

                                            >

                                                <MoreVertIcon />

                                            </IconButton>

                                        )}
                                    </TableCell>

                                </TableRow>

                            ),

                        )}

                    </TableBody>

                </Table>

            </TableContainer>

                <Menu

                    anchorEl={

                        anchorEl

                    }

                    open={

                        menuOpen

                    }

                    onClose={

                        handleCloseMenu

                    }

                >

                {hasPermission(

                    "plans.view",

                ) && (

                    <MenuItem

                        onClick={() => {

                            onRowClick?.(

                                selectedPlan,

                            );

                            handleCloseMenu();

                        }}

                    >

                        <VisibilityOutlinedIcon

                            fontSize="small"

                            sx={{

                                mr: 1,

                            }}

                        />

                        View Details

                    </MenuItem>

                )}

                    {hasPermission(

                        "plans.edit",

                    ) && (

                        <MenuItem

                            onClick={() => {

                                onEdit?.(

                                    selectedPlan,

                                );

                                handleCloseMenu();

                            }}

                        >

                            <EditIcon

                                fontSize="small"

                                sx={{

                                    mr: 1,

                                }}

                            />

                            Edit Plan

                        </MenuItem>

                    )}

                    {selectedPlan?.is_active ? (

                        hasPermission(

                            "plans.deactivate",

                        ) && (

                            <MenuItem

                                onClick={() => {

                                    onToggleStatus?.(

                                        selectedPlan,

                                    );

                                    handleCloseMenu();

                                }}

                            >

                                <BlockIcon

                                    fontSize="small"

                                    sx={{

                                        mr: 1,

                                    }}

                                />

                                Deactivate Plan

                            </MenuItem>

                        )

                    ) : (

                        hasPermission(

                            "plans.activate",

                        ) && (

                            <MenuItem

                                onClick={() => {

                                    onToggleStatus?.(

                                        selectedPlan,

                                    );

                                    handleCloseMenu();

                                }}

                            >

                                <CheckCircleIcon

                                    fontSize="small"

                                    sx={{

                                        mr: 1,

                                    }}

                                />

                                Activate Plan

                            </MenuItem>

                        )

                    )}

                </Menu>
            <TablePagination

                component="div"

                count={total}

                page={page}

                rowsPerPage={rowsPerPage}

                onPageChange={
                    onPageChange
                }

                onRowsPerPageChange={
                    onRowsPerPageChange
                }

                rowsPerPageOptions={[
                    10,
                    25,
                    50,
                ]}

            />

        </Paper>

    );

}

export default PlanTable;                                    