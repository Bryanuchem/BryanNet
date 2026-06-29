import {
    Button,
    DialogActions,
    Stack,
    Typography,
} from "@mui/material";

import ReceiptLongRoundedIcon from "@mui/icons-material/ReceiptLongRounded";

import FormDialog from "../common/FormDialog";
import SectionCard from "../common/SectionCard";
import EntityHeader from "../common/EntityHeader";
import DetailItem from "../common/DetailItem";
import BadgeChip from "../common/BadgeChip";

function PaymentDetailsDialog({

    open,

    payment,

    onClose,

}) {

    if (!payment) {

        return null;

    }

    return (

        <FormDialog

            open={open}

            onClose={onClose}

            maxWidth="md"

            title="Payment Details"

            subtitle="View payment information."

            icon={

                <ReceiptLongRoundedIcon

                    color="primary"

                    fontSize="large"

                />

            }

            showCancel={false}

            footer={

                <DialogActions
                    sx={{
                        width: "100%",
                        px: 0,
                    }}
                >

                    <Button
                        variant="contained"
                        onClick={onClose}
                    >

                        Close

                    </Button>

                </DialogActions>

            }

        >

            <EntityHeader

                title={

                    payment.payment_reference

                }

                subtitle={

                    payment.customer_name

                }

                status={

                    <BadgeChip

                        status={

                            payment.status

                        }

                    />

                }

            />

            <SectionCard

                title="Payment Information"

            >

                <Stack
                    spacing={2}
                >

                    <DetailItem

                        label="Amount"

                        value={`₦${Number(

                            payment.amount || 0,

                        ).toLocaleString()}`}

                    />

                    <DetailItem

                        label="Payment Channel"

                        value={

                            payment.payment_channel

                        }

                    />

                    <DetailItem

                        label="Payment Method"

                        value={

                            payment.payment_method ||

                            "-"

                        }

                    />

                    <DetailItem

                        label="Reference"

                        value={

                            payment.payment_reference

                        }

                    />

                    <DetailItem

                        label="Payment Date"

                        value={

                            payment.payment_date

                                ? new Date(

                                      payment.payment_date,

                                  ).toLocaleString()

                                : "-"

                        }

                    />

                </Stack>

            </SectionCard>

            <SectionCard
                title="Customer Information"
            >

                <Stack spacing={2}>

                    <DetailItem
                        label="Customer"
                        value={
                            payment.customer_name ||
                            "-"
                        }
                    />

                    <DetailItem
                        label="Customer ID"
                        value={
                            payment.customer_id ??
                            "-"
                        }
                    />

                    <DetailItem
                        label="Phone Number"
                        value={
                            payment.phone_number ||
                            "-"
                        }
                    />

                </Stack>

            </SectionCard>

            <SectionCard
                title="Subscription Information"
            >

                <Stack spacing={2}>

                    <DetailItem
                        label="Subscription ID"
                        value={
                            payment.subscription_id ??
                            "-"
                        }
                    />

                    <DetailItem
                        label="Plan"
                        value={
                            payment.plan_name ||
                            "-"
                        }
                    />

                    <DetailItem
                        label="Subscription Status"
                        value={
                            payment.subscription_status
                                ? (
                                    <BadgeChip
                                        status={
                                            payment.subscription_status
                                        }
                                    />
                                )
                                : "-"
                        }
                    />

                    <DetailItem
                        label="Expiry Date"
                        value={
                            payment.expiry_date
                                ? new Date(
                                      payment.expiry_date,
                                  ).toLocaleDateString()
                                : "-"
                        }
                    />

                </Stack>

            </SectionCard>

            <SectionCard
                title="Notes"
            >

                <Typography
                    variant="body2"
                    color={
                        payment.notes
                            ? "text.primary"
                            : "text.secondary"
                    }
                    sx={{
                        whiteSpace: "pre-wrap",
                    }}
                >

                    {payment.notes ||
                        "No notes were recorded for this payment."}

                </Typography>

            </SectionCard>

        </FormDialog>

    );

}

export default PaymentDetailsDialog;           