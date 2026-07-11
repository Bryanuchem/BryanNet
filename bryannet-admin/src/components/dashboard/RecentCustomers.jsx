import {
    Button,
    Chip,
    Skeleton,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Typography,
} from "@mui/material";

import DashboardSection from "../common/DashboardSection";

import { useCustomers } from "../../hooks/useCustomers";

import { useNavigate } from "react-router-dom";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

function RecentCustomers() {

    const navigate = useNavigate();

    const {

        hasPermission,

    } = useCurrentPermissions();

    const {
        data: customers = [],
        isLoading,
    } = useCustomers();

    const recentCustomers = [...customers]
        .sort(
            (a, b) =>
                b.customer_id - a.customer_id
        )
        .slice(0, 5);

    return (

        <DashboardSection

            title="Recent Customers"

            action={

                hasPermission(

                    "customers.view",

                ) && (

                    <Button

                        size="small"

                        variant="text"

                        onClick={() =>

                            navigate(

                                "/customers",

                            )

                        }

                    >

                        View All

                    </Button>

                )

            }

        >

            <TableContainer>

                <Table size="small">

                    <TableHead>

                        <TableRow>

                            <TableCell>
                                Customer
                            </TableCell>

                            <TableCell>
                                Phone Number
                            </TableCell>

                            <TableCell align="center">
                                Status
                            </TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {isLoading ? (

                            [...Array(5)].map((_, index) => (

                                <TableRow key={index}>

                                    <TableCell colSpan={3}>

                                        <Skeleton height={40} />

                                    </TableCell>

                                </TableRow>

                            ))

                        ) : recentCustomers.length === 0 ? (

                            <TableRow>

                                <TableCell
                                    colSpan={3}
                                    align="center"
                                >

                                    <Typography
                                        color="text.secondary"
                                        sx={{ py: 3 }}
                                    >
                                        No customers found.
                                    </Typography>

                                </TableCell>

                            </TableRow>

                        ) : (

                            recentCustomers.map(
                                (customer) => (

                                    <TableRow
                                        key={
                                            customer.customer_id
                                        }
                                        hover
                                    >

                                        <TableCell>
                                            {customer.full_name}
                                        </TableCell>

                                        <TableCell>
                                            {customer.phone_number}
                                        </TableCell>

                                        <TableCell
                                            align="center"
                                        >

                                            <Chip
                                                size="small"
                                                label={
                                                    customer.is_registered
                                                        ? "Registered"
                                                        : "Pending"
                                                }
                                                color={
                                                    customer.is_registered
                                                        ? "success"
                                                        : "warning"
                                                }
                                            />

                                        </TableCell>

                                    </TableRow>

                                )

                            )

                        )}

                    </TableBody>

                </Table>

            </TableContainer>

        </DashboardSection>

    );

}

export default RecentCustomers;