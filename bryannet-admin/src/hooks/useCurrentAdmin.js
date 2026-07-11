import {

    useQuery,

} from "@tanstack/react-query";

import authService from "../api/auth";

export function useCurrentAdmin() {

    return useQuery({

        queryKey: [

            "current-admin",

        ],

        queryFn:

            authService.getCurrentAdmin,

    });

}