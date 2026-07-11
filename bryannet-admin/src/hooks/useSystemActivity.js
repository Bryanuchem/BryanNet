import {

    useQuery,

} from "@tanstack/react-query";

import {

    getSystemActivity,

} from "../api/systemActivity";

export function useSystemActivity(

    filters,

) {

    return useQuery({

        queryKey: [

            "system-activity",

            filters,

        ],

        queryFn: () =>

            getSystemActivity(

                filters,

            ),

        placeholderData: (

            previousData,

        ) => previousData,

    });

}