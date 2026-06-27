import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
} from "@mui/material";

import {
    formatPhoneNumber,
    formatStatus,
    formatRegistrationStatus,
    formatTelegramStatus,
} from "../../utils/customerFormatter";

import {
    CircularProgress,
    Box,
    Typography,
} from "@mui/material";

import IconButton from "@mui/material/IconButton";
import MoreVertIcon from "@mui/icons-material/MoreVert";

function CustomerTable({ 
    customers,
    loading,
    searchTerm,
    totalCustomers,

 }) {

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

    if (customers.length === 0) {
        return (
            <Box
                sx={{
                    textAlign: "center",
                    py: 6,
                }}
            >
                <Typography color="text.secondary">
                    {searchTerm
                        ? "No matching customers found."
                        : totalCustomers === 0
                        ? "No customers found."
                        : "No customers available."}
                </Typography>
            </Box>
        );
    }
        
    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Phone</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Registered</TableCell>
                        <TableCell>Telegram</TableCell>
                        <TableCell align="center">Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {customers.map((customer) => (
                        <TableRow key={customer.customer_id}>
                            <TableCell>{customer.full_name}</TableCell>

                            <TableCell>
                                {formatPhoneNumber(customer.phone_number)}
                            </TableCell>

                            <TableCell>
                                {formatStatus(customer.status)}
                            </TableCell>

                            <TableCell>
                                {formatRegistrationStatus(customer.is_registered)}
                            </TableCell>

                            <TableCell>
                                {formatTelegramStatus(customer.telegram_user_id)}
                            </TableCell>

                            <TableCell align="center">
                                <IconButton size="small">
                                    <MoreVertIcon fontSize="small" />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}

export default CustomerTable;