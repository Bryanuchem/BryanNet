import {
    Box,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";

import BadgeChip from "../common/BadgeChip";
import EmptyState from "../common/EmptyState";
import ActionMenu from "../common/ActionMenu";

function DeviceTable({
    devices = [],
    onView,
    onDelete,
}) {

    if (!devices.length) {
        return (
            <EmptyState
                title="No Devices Found"
                description="No registered devices are available."
            />
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
                            Device
                        </TableCell>

                        <TableCell>
                            MAC Address
                        </TableCell>

                        <TableCell>
                            Customer
                        </TableCell>

                        <TableCell>
                            Status
                        </TableCell>

                        <TableCell align="right">
                            Actions
                        </TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {devices.map((device) => (

                        <TableRow
                            key={device.device_id}
                            hover
                        >

                            <TableCell>

                                <Box>

                                    <Typography
                                        fontWeight={600}
                                    >
                                        {device.device_name}
                                    </Typography>

                                </Box>

                            </TableCell>

                            <TableCell>
                                {device.mac_address}
                            </TableCell>

                            <TableCell>
                                {device.customer_name}
                            </TableCell>

                            <TableCell>

                                <BadgeChip
                                    variant="status"
                                    value={device.device_status}
                                />

                            </TableCell>

                            <TableCell align="right">

                                <ActionMenu
                                    items={[
                                        {
                                            label: "View",
                                            icon: (
                                                <VisibilityOutlinedIcon
                                                    fontSize="small"
                                                />
                                            ),
                                            onClick: () =>
                                                onView(device),
                                        },
                                        {
                                            label: "Remove",
                                            icon: (
                                                <DeleteOutlineOutlinedIcon
                                                    fontSize="small"
                                                />
                                            ),
                                            onClick: () =>
                                                onDelete(device),
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

export default DeviceTable;