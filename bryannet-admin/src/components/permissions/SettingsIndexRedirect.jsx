import {
    Navigate,
} from "react-router-dom";

import {
    useCurrentPermissions,
} from "../../hooks/useCurrentPermissions";

export default function SettingsIndexRedirect() {

    const {

        hasPermission,

    } = useCurrentPermissions();

    if (

        hasPermission(

            "settings.general",

        )

    ) {

        return (

            <Navigate

                to="general"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.authentication",

        )

    ) {

        return (

            <Navigate

                to="authentication"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.notifications",

        )

    ) {

        return (

            <Navigate

                to="notifications"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.network",

        )

    ) {

        return (

            <Navigate

                to="network"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.billing",

        )

    ) {

        return (

            <Navigate

                to="billing"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.integrations",

        )

    ) {

        return (

            <Navigate

                to="integrations"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.branding",

        )

    ) {

        return (

            <Navigate

                to="branding"

                replace

            />

        );

    }

    if (

        hasPermission(

            "settings.system",

        )

    ) {

        return (

            <Navigate

                to="system"

                replace

            />

        );

    }

    return (

        <Navigate

            to="/unauthorized"

            replace

        />

    );

}