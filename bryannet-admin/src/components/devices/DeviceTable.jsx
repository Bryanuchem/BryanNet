import {
    Box,
    Chip,
    CircularProgress,
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

import VisibilityIcon from "@mui/icons-material/Visibility";
import AutorenewIcon from "@mui/icons-material/Autorenew";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import BlockIcon from "@mui/icons-material/Block";
import LockOpenIcon from "@mui/icons-material/LockOpen";
import ToggleOffIcon from "@mui/icons-material/ToggleOff";
import ToggleOnIcon from "@mui/icons-material/ToggleOn";

import EmptyState from "../common/EmptyState";
import BadgeChip from "../common/BadgeChip";
import ActionMenu from "../common/ActionMenu";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function DeviceTable({

    devices,

    loading = false,

    searchTerm,

    page,

    rowsPerPage,

    onPageChange,

    onRowsPerPageChange,

    onRowClick,

    onToggleStatus,

    onApprove,

    onBlock,

    onUnblock,

    onRename,

    onReplace,

}) {
    const {

        hasPermission,

    } = useCurrentPermissions();

    if (loading) {


        return (

            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    py: 6,
                }}
            >

                <CircularProgress />

            </Box>

        );

    }

    if (devices.length === 0) {

        if (searchTerm) {

            return (

                <EmptyState
                    title="No matching devices"
                    description="Try searching with a different customer, device name or MAC address."
                />

            );

        }

        return (

            <EmptyState
                title="No devices yet"
                description="Registered customer devices will appear here."
            />

        );

    }

    return (

        <Paper>

            <TableContainer
                sx={{
                    maxHeight: 650,
                }}
            >

                <Table stickyHeader>

                    <TableHead>

                        <TableRow>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Customer
                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Device
                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                MAC Address
                            </TableCell>

                            <TableCell
                                align="center"
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Status
                            </TableCell>

                            <TableCell
                                align="center"
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Approved
                            </TableCell>

                            <TableCell
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Last Seen
                            </TableCell>

                            <TableCell
                                align="center"
                                sx={{
                                    fontWeight: 700,
                                }}
                            >
                                Actions
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {devices

                            .slice(

                                page * rowsPerPage,

                                page * rowsPerPage + rowsPerPage,

                            )

                            .map((device) => (

                                <TableRow

                                    key={device.device_id}

                                    hover

                                    onClick={() => {

                                        if (

                                            hasPermission(

                                                "devices.view",

                                            )

                                        ) {

                                            onRowClick(

                                                device,

                                            );

                                        }

                                    }}

                                    sx={{

                                        height: 60,

                                        "&:nth-of-type(odd)": {
                                            bgcolor: "#FAFAFA",
                                        },

                                        "&:hover": {
                                            bgcolor: "#F1F5F9",
                                            cursor:

                                                hasPermission(

                                                    "devices.view",

                                                )

                                                    ? "pointer"

                                                    : "default",
                                        },

                                    }}

                                >

                                    <TableCell>

                                        {device.customer_name}

                                    </TableCell>

                                    <TableCell>

                                        {device.device_name}

                                    </TableCell>

                                    <TableCell>

                                        <Typography
                                            fontFamily="monospace"
                                        >

                                            {device.mac_address}

                                        </Typography>

                                    </TableCell>

                                    <TableCell
                                        align="center"
                                    >

                                        <BadgeChip
                                            label={
                                                device.device_status
                                            }
                                            color={

                                                device.device_status === "active"

                                                    ? "success"

                                                    : device.device_status === "inactive"

                                                        ? "warning"

                                                        : "error"

                                            }
                                        />

                                    </TableCell>

                                    <TableCell
                                        align="center"
                                    >

                                        <Chip
                                            size="small"
                                            label={
                                                device.approved_by_customer
                                                    ? "Approved"
                                                    : "Pending"
                                            }
                                            color={
                                                device.approved_by_customer
                                                    ? "success"
                                                    : "warning"
                                            }
                                        />

                                    </TableCell>

                                    <TableCell>

                                        {device.last_seen
                                            ? new Date(
                                                device.last_seen,
                                            ).toLocaleString()
                                            : "Never"}

                                    </TableCell>

                                    <TableCell

                                        align="center"

                                        onClick={(event) =>
                                            event.stopPropagation()
                                        }

                                    >

                                    {(() => {

                                        const actions = [];

                                        if (

                                            hasPermission(

                                                "devices.view",

                                            )

                                        ) {

                                            actions.push({

                                                label: "View Details",

                                                icon: (

                                                    <VisibilityIcon

                                                        fontSize="small"

                                                    />

                                                ),

                                                onClick: () =>

                                                    onRowClick(

                                                        device,

                                                    ),

                                            });

                                        }

                                        if (

                                            hasPermission(

                                                "devices.replace",

                                            )

                                        ) {

                                            actions.push({

                                                label: "Replace Device",

                                                icon: (

                                                    <AutorenewIcon

                                                        fontSize="small"

                                                    />

                                                ),

                                                onClick: () =>

                                                    onReplace(

                                                        device,

                                                    ),

                                            });

                                        }

                                        if (

                                            hasPermission(

                                                "devices.rename",

                                            )

                                        ) {

                                            actions.push({

                                                label: "Rename Device",

                                                icon: (

                                                    <AutorenewIcon

                                                        fontSize="small"

                                                    />

                                                ),

                                                onClick: () =>

                                                    onRename(

                                                        device,

                                                    ),

                                            });

                                        }

                                        if (

                                            !device.approved_by_customer &&

                                            hasPermission(

                                                "devices.approve",

                                            )

                                        ) {

                                            actions.push({

                                                label: "Approve Device",

                                                icon: (

                                                    <CheckCircleIcon

                                                        fontSize="small"

                                                    />

                                                ),

                                                onClick: () =>

                                                    onApprove(

                                                        device,

                                                    ),

                                            });

                                        }

                                        if (

                                            device.device_status === "active"

                                        ) {

                                            if (

                                                hasPermission(

                                                    "devices.deactivate",

                                                )

                                            ) {

                                                actions.push({

                                                    label: "Deactivate Device",

                                                    icon: (

                                                        <ToggleOffIcon

                                                            fontSize="small"

                                                        />

                                                    ),

                                                    onClick: () =>

                                                        onToggleStatus(

                                                            device,

                                                        ),

                                                });

                                            }

                                            if (

                                                hasPermission(

                                                    "devices.block",

                                                )

                                            ) {

                                                actions.push({

                                                    label: "Block Device",

                                                    icon: (

                                                        <BlockIcon

                                                            fontSize="small"

                                                        />

                                                    ),

                                                    onClick: () =>

                                                        onBlock(

                                                            device,

                                                        ),

                                                });

                                            }

                                        }

                                        if (

                                            device.device_status === "inactive"

                                        ) {

                                            if (

                                                hasPermission(

                                                    "devices.activate",

                                                )

                                            ) {

                                                actions.push({

                                                    label: "Activate Device",

                                                    icon: (

                                                        <ToggleOnIcon

                                                            fontSize="small"

                                                        />

                                                    ),

                                                    onClick: () =>

                                                        onToggleStatus(

                                                            device,

                                                        ),

                                                });

                                            }

                                            if (

                                                device.device_status === "blocked" &&

                                                hasPermission(

                                                    "devices.unblock",

                                                )

                                            ) {

                                                actions.push({

                                                    label: "Unblock Device",

                                                    icon: (

                                                        <LockOpenIcon

                                                            fontSize="small"

                                                        />

                                                    ),

                                                    onClick: () =>

                                                        onUnblock(

                                                            device,

                                                        ),

                                                });

                                            }
                                        }

                                        return actions.length > 0 ? (

                                            <ActionMenu

                                                items={actions}

                                            />

                                        ) : null;

                                    })()}

                                    </TableCell>

                                </TableRow>

                            ))}

                    </TableBody>

                </Table>

            </TableContainer>

            <TablePagination

                component="div"

                count={devices.length}

                page={page}

                rowsPerPage={rowsPerPage}

                onPageChange={onPageChange}

                onRowsPerPageChange={
                    onRowsPerPageChange
                }

                rowsPerPageOptions={[
                    5,
                    10,
                    25,
                ]}

            />

        </Paper>

    );

}

export default DeviceTable;