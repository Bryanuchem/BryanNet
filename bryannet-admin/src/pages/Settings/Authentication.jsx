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

import AuthenticationSettingsForm from "../../components/settings/authentication/AuthenticationSettingsForm";
import AuthenticationSettingsInfoCard from "../../components/settings/authentication/AuthenticationSettingsInfoCard";

import {

    useAuthenticationSettings,

    useUpdateAuthenticationSettings,

} from "../../hooks/useSettings";

const defaultSettings = {

    registration_enabled: false,

    session_timeout_minutes: 30,

    max_login_attempts: 5,

    password_min_length: 8,

    require_special_characters: true,

    require_uppercase: true,

    require_numbers: true,

    two_factor_auth_enabled: false,

};

export default function Authentication() {

    const {

        data,

        isLoading,

    } = useAuthenticationSettings();

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

        useUpdateAuthenticationSettings({

            onSuccess: () => {

                setSnackbar({

                    open: true,

                    severity: "success",

                    message:

                        "Authentication settings updated successfully.",

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

                        "Failed to update authentication settings.",

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

                title="Authentication Settings"

                subtitle="Configure administrator authentication, password policies and session security for the BryanNet ISP Platform."

            />

            <Stack spacing={3}>

                <AuthenticationSettingsInfoCard

                    settings={

                        settings

                    }

                />

                <AuthenticationSettingsForm

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