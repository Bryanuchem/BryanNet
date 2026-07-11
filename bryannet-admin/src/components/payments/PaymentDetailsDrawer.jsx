import {
    Box,
    Button,
    Card,
    CardContent,
    Divider,
    Drawer,
    Stack,
    Typography,
} from "@mui/material";

import Avatar from "@mui/material/Avatar";

import ReceiptLongRoundedIcon from "@mui/icons-material/ReceiptLongRounded";
import PersonIcon from "@mui/icons-material/Person";
import SellIcon from "@mui/icons-material/Sell";
import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";

import BadgeChip from "../common/BadgeChip";
import InfoField from "../common/InfoField";

function PaymentDetailsDrawer({

    open,

    payment,

    onClose,

}) {

    if (!payment) {

        return null;

    }

    const formatDate = (date) => {

        if (!date) {

            return "-";

        }

        return new Date(
            date,
        ).toLocaleString();

    };

    return (

        <Drawer
            anchor="right"
            open={open}
            onClose={onClose}
        >

            <Box
                sx={{

                    width: 450,

                    height: "100%",

                    bgcolor: "#F8FAFC",

                    display: "flex",

                    flexDirection: "column",

                }}
            >

                {/* Header */}

                <Box
                    sx={{

                        bgcolor: "primary.main",

                        color: "white",

                        p: 4,

                        display: "flex",

                        alignItems: "center",

                        gap: 3,

                    }}
                >

                    <Avatar
                        sx={{

                            width: 64,

                            height: 64,

                            bgcolor: "white",

                            color: "primary.main",

                            fontWeight: 700,

                            fontSize: 28,

                        }}
                    >

                        <ReceiptLongRoundedIcon
                            fontSize="large"
                        />

                    </Avatar>

                    <Box>

                        <Typography
                            variant="overline"
                        >

                            PAYMENT DETAILS

                        </Typography>

                        <Typography
                            variant="h5"
                            fontWeight={700}
                        >

                            {payment.payment_reference}

                        </Typography>

                        <Typography
                            sx={{
                                opacity: 0.9,
                            }}
                        >

                            {payment.customer_name}

                        </Typography>

                    </Box>

                </Box>

                {/* Content */}

                <Box
                    sx={{

                        flex: 1,

                        overflowY: "auto",

                        p: 3,

                    }}
                >

                    <Card elevation={1}>

                        <CardContent>

                            <Typography
                                variant="subtitle2"
                                fontWeight={700}
                                gutterBottom
                            >

                                PAYMENT INFORMATION

                            </Typography>

                            <Divider
                                sx={{
                                    mb: 3,
                                }}
                            />

                            <Stack
                                spacing={3}
                            >

                                <InfoField
                                    icon={<PaymentsRoundedIcon />}
                                    label="Amount"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        ₦

                                        {Number(

                                            payment.amount ?? 0,

                                        ).toLocaleString()}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Status"
                                >

                                    <BadgeChip
                                        status={
                                            payment.status?.toLowerCase()
                                        }
                                        label={
                                            payment.status
                                        }
                                    />

                                </InfoField>

                                <InfoField
                                    icon={<PaymentsRoundedIcon />}
                                    label="Provider"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.payment_provider}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<PaymentsRoundedIcon />}
                                    label="Channel"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.payment_channel}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<PaymentsRoundedIcon />}
                                    label="Method"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.payment_method || "-"}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<ReceiptLongRoundedIcon />}
                                    label="Reference"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.payment_reference}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<ReceiptLongRoundedIcon />}
                                    label="Gateway Reference"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.gateway_transaction_id || "-"}

                                    </Typography>

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                    <Card
                        elevation={1}
                        sx={{
                            mt: 3,
                        }}
                    >

                        <CardContent>

                            <Typography
                                variant="subtitle2"
                                fontWeight={700}
                                gutterBottom
                            >

                                CUSTOMER INFORMATION

                            </Typography>

                            <Divider
                                sx={{
                                    mb: 3,
                                }}
                            />

                            <Stack
                                spacing={3}
                            >

                                <InfoField
                                    icon={<PersonIcon />}
                                    label="Customer"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.customer_name}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<PersonIcon />}
                                    label="Customer ID"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.customer_id}

                                    </Typography>

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                    <Card
                        elevation={1}
                        sx={{
                            mt: 3,
                        }}
                    >

                        <CardContent>

                            <Typography
                                variant="subtitle2"
                                fontWeight={700}
                                gutterBottom
                            >

                                SUBSCRIPTION INFORMATION

                            </Typography>

                            <Divider
                                sx={{
                                    mb: 3,
                                }}
                            />

                            <Stack
                                spacing={3}
                            >

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Plan"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.plan_name || "-"}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Plan ID"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.plan_id}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<SellIcon />}
                                    label="Subscription ID"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {payment.subscription_id ?? "-"}

                                    </Typography>

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                    <Card
                        elevation={1}
                        sx={{
                            mt: 3,
                        }}
                    >

                        <CardContent>

                            <Typography
                                variant="subtitle2"
                                fontWeight={700}
                                gutterBottom
                            >

                                TIMELINE

                            </Typography>

                            <Divider
                                sx={{
                                    mb: 3,
                                }}
                            />

                            <Stack
                                spacing={3}
                            >

                                <InfoField
                                    icon={<CalendarTodayIcon />}
                                    label="Created"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {formatDate(
                                            payment.created_at,
                                        )}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<CalendarTodayIcon />}
                                    label="Updated"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {formatDate(
                                            payment.updated_at,
                                        )}

                                    </Typography>

                                </InfoField>

                                <InfoField
                                    icon={<CalendarTodayIcon />}
                                    label="Payment Date"
                                >

                                    <Typography
                                        fontWeight={500}
                                    >

                                        {formatDate(
                                            payment.payment_date,
                                        )}

                                    </Typography>

                                </InfoField>

                            </Stack>

                        </CardContent>

                    </Card>

                </Box>

                {/* Footer */}

                <Box
                    sx={{

                        p: 3,

                        bgcolor: "white",

                        borderTop:
                            "1px solid #E5E7EB",

                    }}
                >

                    <Button

                        fullWidth

                        variant="contained"

                        size="large"

                        onClick={onClose}

                    >

                        Close

                    </Button>

                </Box>

            </Box>

        </Drawer>

    );

}

export default PaymentDetailsDrawer;