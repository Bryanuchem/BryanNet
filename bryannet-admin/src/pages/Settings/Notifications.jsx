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

import NotificationSettingsForm from "../../components/settings/notifications/NotificationSettingsForm";
import NotificationSettingsInfoCard from "../../components/settings/notifications/NotificationSettingsInfoCard";

import {

    useNotificationSettings,

    useUpdateNotificationSettings,

} from "../../hooks/useSettings";

const defaultSettings = {

    email_notifications: true,

    sms_notifications: false,

    payment_reminders: true,

    outage_alerts: true,

    low_balance_alerts: true,

};

export default function Notifications() {

    const {

        data,

        isLoading,

    } = useNotificationSettings();

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

        useUpdateNotificationSettings({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Notification settings updated successfully.",

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

                        "Failed to update notification settings.",

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

                title="Notification Settings"

                subtitle="Configure how BryanNet delivers billing, account and network notifications to customers."

            />

            <Stack spacing={3}>

                <NotificationSettingsInfoCard

                    settings={

                        settings

                    }

                />

                <NotificationSettingsForm

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