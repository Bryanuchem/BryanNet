import {
    useEffect,
    useState,
} from "react";

import {
    useSearchParams,
} from "react-router-dom";

import {
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Stack,
    Typography,
} from "@mui/material";

import client from "../../api/client";

export default function PaymentSuccessPage() {

    const [
        searchParams,
    ] = useSearchParams();

    const reference = (
        searchParams.get(
            "reference",
        )
    );

    const [
        payment,
        setPayment,
    ] = useState(
        null,
    );

    const [
        loading,
        setLoading,
    ] = useState(
        true,
    );

    useEffect(() => {

        async function loadPayment() {

            try {

                const response = await client.get(

                    `/portal/payments/success/${reference}`,

                );

                setPayment(
                    response.data,
                );

            }

            finally {

                setLoading(
                    false,
                );

            }

        }

        if (
            reference
        ) {

            loadPayment();

        }

    }, [
        reference,
    ]);

    useEffect(() => {

        if (
            !payment
        ) {

            return;

        }

        const username = (
            import.meta.env
            .VITE_TELEGRAM_BOT_USERNAME
        );

        const timer = setTimeout(

            () => {

                window.location.href = (

                    `https://t.me/`

                    + username

                    + `?start=payment_`

                    + payment.payment_reference

                );

            },

            2000,

        );

        return () => clearTimeout(
            timer,
        );

    }, [
        payment,
    ]);

    if (
        loading
    ) {

        return (

            <Box
                display="flex"
                justifyContent="center"
                mt={8}
            >

                <CircularProgress />

            </Box>

        );

    }

    if (
        !payment
    ) {

        return (

            <Typography
                align="center"
                mt={8}
            >

                Payment not found.

            </Typography>

        );

    }

    const telegramUrl = (

        `https://t.me/`

        + import.meta.env
            .VITE_TELEGRAM_BOT_USERNAME

        + `?start=payment_`

        + payment.payment_reference

    );

    return (

        <Box
            display="flex"
            justifyContent="center"
            mt={8}
        >

            <Card
                sx={{
                    width: 480,
                    maxWidth: "100%",
                }}
            >

                <CardContent>

                    <Stack
                        spacing={3}
                    >

                        <Typography
                            variant="h4"
                            align="center"
                        >

                            ✅ Payment Successful

                        </Typography>

                        <Typography
                            align="center"
                        >

                            Your BryanNet subscription
                            has been activated.

                        </Typography>

                        <Box>

                            <Typography>

                                <strong>
                                    Plan
                                </strong>

                            </Typography>

                            <Typography>

                                {payment.plan_name}

                            </Typography>

                        </Box>

                        <Box>

                            <Typography>

                                <strong>
                                    Amount
                                </strong>

                            </Typography>

                            <Typography>

                                ₦{payment.amount}

                            </Typography>

                        </Box>

                        <Box>

                            <Typography>

                                <strong>
                                    Reference
                                </strong>

                            </Typography>

                            <Typography>

                                {payment.payment_reference}

                            </Typography>

                        </Box>

                        <Typography
                            align="center"
                            color="text.secondary"
                        >

                            Opening Telegram...

                        </Typography>

                        <Button

                            variant="contained"

                            size="large"

                            href={
                                telegramUrl
                            }

                        >

                            Open BryanNet on Telegram

                        </Button>

                    </Stack>

                </CardContent>

            </Card>

        </Box>

    );

}