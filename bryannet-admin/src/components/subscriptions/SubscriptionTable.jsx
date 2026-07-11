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

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import CancelIcon from "@mui/icons-material/Cancel";
import BadgeChip from "../common/BadgeChip";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";

function SubscriptionTable({

    subscriptions,

    loading,

    page,

    rowsPerPage,

    total,

    onPageChange,

    onRowsPerPageChange,

    onRowClick,

    onCancel,

}) {

    const {

        hasPermission,

    } = useCurrentPermissions();

    const [

        anchorEl,

        setAnchorEl,

    ] = useState(null);

    const [
        selectedSubscription,
        setSelectedSubscription,
    ] = useState(null);

    const menuOpen =
        Boolean(anchorEl);

    const handleOpenMenu = (

        event,

        subscription,

    ) => {

        const canOpen =

            hasPermission(

                "subscriptions.view",

            ) ||

            hasPermission(

                "subscriptions.cancel",

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

        setSelectedSubscription(

            subscription,

        );

    };

    const handleCloseMenu =
        () => {

            setAnchorEl(null);

            setSelectedSubscription(
                null,
            );

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

    if (!subscriptions.length) {

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

                    No subscriptions found.

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
                                Customer
                            </TableCell>

                            <TableCell>
                                Plan
                            </TableCell>

                            <TableCell>
                                Status
                            </TableCell>

                            <TableCell>
                                Remaining
                            </TableCell>

                            <TableCell>
                                Started
                            </TableCell>

                            <TableCell>
                                Expires
                            </TableCell>

                            <TableCell
                                align="right"
                            >
                                Actions
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {subscriptions.map(
                            (
                                subscription,
                            ) => (

                                <TableRow

                                    hover

                                    key={

                                        subscription.subscription_id

                                    }

                                    onClick={() => {

                                        if (

                                            hasPermission(

                                                "subscriptions.view",

                                            )

                                        ) {

                                            onRowClick?.(

                                                subscription,

                                            );

                                        }

                                    }}

                                    sx={{

                                        cursor:

                                            hasPermission(

                                                "subscriptions.view",

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
                                                subscription.customer_name
                                            }

                                        </Typography>

                                    </TableCell>

                                    <TableCell>

                                        {
                                            subscription.plan_name
                                        }

                                    </TableCell>

                                    <TableCell>

                                        <BadgeChip
                                            status={

                                                subscription.status?.toLowerCase()

                                            }
                                            label={
                                                subscription.status
                                            }
                                        />

                                    </TableCell>

                                    <TableCell>

                                        {

                                            subscription.remaining_days

                                        }{" "}

                                        days

                                    </TableCell>

                                    <TableCell>

                                        {

                                            subscription.created_at

                                                ? new Date(

                                                      subscription.created_at,

                                                  ).toLocaleDateString()

                                                : "-"

                                        }

                                    </TableCell>

                                    <TableCell>

                                        {

                                            subscription.expiry_date

                                                ? new Date(

                                                      subscription.expiry_date,

                                                  ).toLocaleDateString()

                                                : "-"

                                        }

                                    </TableCell>

                                    <TableCell

                                        align="right"

                                        onClick={(event) =>

                                            event.stopPropagation()

                                        }

                                    >

                                        {(

                                            hasPermission(

                                                "subscriptions.view",

                                            ) ||

                                            hasPermission(

                                                "subscriptions.cancel",

                                            )

                                        ) && (

                                            <IconButton

                                                onClick={(event) =>

                                                    handleOpenMenu(

                                                        event,

                                                        subscription,

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

                    "subscriptions.view",

                ) && (

                    <MenuItem

                        onClick={() => {

                            onRowClick?.(

                                selectedSubscription,

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
                    "subscriptions.cancel",
                ) &&
                    selectedSubscription?.status?.toLowerCase() ===
                        "queued" && (
                        <MenuItem
                            onClick={() => {
                                onCancel?.(
                                    selectedSubscription.subscription_id,
                                );
                                handleCloseMenu();
                            }}
                        >
                            <CancelIcon
                                fontSize="small"
                                sx={{ mr: 1 }}
                            />
                            Cancel Queued Subscription
                        </MenuItem>
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

export default SubscriptionTable;                                    