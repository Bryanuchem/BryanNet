import {

    useQuery,

} from "@tanstack/react-query";

import {

    getAdminSessions,

} from "../api/adminSessions";

export function useAdminSessions(

    filters,

) {

    return useQuery({

        queryKey: [

            "admin-sessions",

            filters,

        ],

        queryFn: () =>

            getAdminSessions(

                filters,

            ),

        placeholderData: (

            previousData,

        ) => previousData,

    });

}