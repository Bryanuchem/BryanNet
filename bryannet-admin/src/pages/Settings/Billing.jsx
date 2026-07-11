import {

    useEffect,

    useState,

} from "react";

import {

    Stack,

} from "@mui/material";

import PageHeader from "../../components/common/PageHeader";
import AppSnackbar from "../../components/common/AppSnackbar";

import SettingsPageActions from "../../components/settings/SettingsPageActions";

import BillingSettingsForm from "../../components/settings/billing/BillingSettingsForm";
import BillingSettingsInfoCard from "../../components/settings/billing/BillingSettingsInfoCard";

import {

    useBillingSettings,

    useUpdateBillingSettings,

} from "../../hooks/useSettings";

const defaultSettings = {

    default_payment_method: "",

    default_payment_channel: "",

    auto_suspend_overdue: true,

    suspend_after_days: 30,

    invoice_due_days: 7,

    tax_percentage: 0,

};

export default function Billing() {

    const {

        data,

        isLoading,

    } = useBillingSettings();

    const [

        settings,

        setSettings,

    ] = useState(

        defaultSettings,

    );

    const [

        snackbar,

        setSnackbar,

    ] = useState({

        open: false,

        message: "",

        severity: "success",

    });

    const updateSettings =

        useUpdateBillingSettings({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Billing settings updated successfully.",

                });

            },

            onError: (

                error,

            ) => {

                setSnackbar({

                    open: true,

                    severity: "error",

                    message:

                        error?.response?.data?.message ||

                        error?.response?.data?.detail ||

                        "Failed to update billing settings.",

                });

            },

        });

    useEffect(

        () => {

            if (

                data

            ) {

                setSettings({

                    ...defaultSettings,

                    ...data,

                });

            }

        },

        [

            data,

        ],

    );

    function handleChange(

        field,

        value,

    ) {

        setSettings(

            (

                previous,

            ) => ({

                ...previous,

                [

                    field

                ]: value,

            }),

        );

    }

    function handleSave() {

        updateSettings.mutate(

            settings,

        );

    }

    function handleReset() {

        if (

            data

        ) {

            setSettings({

                ...defaultSettings,

                ...data,

            });

        }

    }

    return (

        <>

            <PageHeader

                title="Billing Settings"

                subtitle="Configure default payment methods, invoicing policies and customer suspension rules for the BryanNet ISP Platform."

            />

            <Stack spacing={3}>

                <BillingSettingsInfoCard

                    settings={

                        settings

                    }

                />

                <BillingSettingsForm

                    settings={

                        settings

                    }

                    onChange={

                        handleChange

                    }

                    disabled={

                        isLoading ||

                        updateSettings.isPending

                    }

                />

                <SettingsPageActions

                    onSave={

                        handleSave

                    }

                    onReset={

                        handleReset

                    }

                    loading={

                        updateSettings.isPending

                    }

                />

            </Stack>

            <AppSnackbar

                open={

                    snackbar.open

                }

                severity={

                    snackbar.severity

                }

                message={

                    snackbar.message

                }

                onClose={() =>

                    setSnackbar(

                        (

                            previous,

                        ) => ({

                            ...previous,

                            open: false,

                        }),

                    )

                }

            />

        </>

    );

}